"""Deterministic synthetic knowledge pipeline; no semantic inference is performed."""
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path

STOP_WORDS = {
    "core", "system", "wiki", "page", "test", "tests", "code", "codes",
    "agent", "agents", "claude", "session", "sessions", "review", "reviews",
    "task", "tasks", "work", "file", "files", "data", "info", "context",
    "pattern", "patterns", "decision", "decisions", "concept", "concepts",
    "rule", "rules", "guide", "guides", "doc", "docs", "user", "users",
}
KINDS = {"Decision", "Resolution", "Failure", "Anomaly"}
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,79}$")


def char_bigrams(s):
    """Return the set of character bigrams."""
    s = s.lower()
    return {s[i:i+2] for i in range(len(s)-1)} if len(s) >= 2 else {s} if s else set()


def char_bigram_jaccard(a, b):
    """Return character-bigram Jaccard similarity, or zero for two empty strings."""
    left, right = char_bigrams(a), char_bigrams(b)
    return len(left & right) / len(left | right) if left or right else 0.0


def score_page(page, prompt_lower, prompt_words):
    """Score tag and title matches with the original keyword weighting."""
    score = 0
    for tag in page["tags"]:
        tl = tag.lower()
        if not tl or tl in STOP_WORDS:
            continue
        if tl in prompt_lower:
            score += 4
    title_words = re.split(r"[\s\-_]+", page["title"].lower())
    for word in title_words:
        if len(word) >= 5 and word not in STOP_WORDS and word in prompt_words:
            score += 2
    for word in prompt_words:
        if len(word) >= 6 and word not in STOP_WORDS and word in page["title"].lower():
            score += 1
    return score


def is_suppressed(total, helped, noise, harmed, min_n=8, zero_min_n=4, helped_floor=.30, noise_ceil=.20):
    """Apply the two original suppression rules without stochastic retesting."""
    values = (total, helped, noise, harmed)
    if any(type(x) is not int or x < 0 for x in values) or helped + noise + harmed > total:
        raise ValueError("invalid counts")
    if type(min_n) is not int or type(zero_min_n) is not int or min_n < 1 or zero_min_n < 1 or not 0 <= helped_floor <= 1 or not 0 <= noise_ceil <= 1:
        raise ValueError("invalid thresholds")
    return (helped == 0 and total >= zero_min_n) or (total >= min_n and (helped / total < helped_floor or (noise + harmed) / total > noise_ceil))


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def checked_id(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise ValueError("invalid identifier")
    return value


def validate_event(row):
    if not isinstance(row, dict) or set(row) != {"schema_version", "id", "session_id", "kind", "text", "tags"}:
        raise ValueError("invalid event fields")
    if row["schema_version"] != 1 or type(row["schema_version"]) is not int or row["kind"] not in KINDS:
        raise ValueError("invalid event version or kind")
    checked_id(row["id"])
    checked_id(row["session_id"])
    if not isinstance(row["text"], str) or not row["text"].strip() or len(row["text"]) > 10000:
        raise ValueError("invalid event text")
    if not isinstance(row["tags"], list) or len(row["tags"]) > 30 or any(not isinstance(t, str) or not t or len(t) > 100 for t in row["tags"]):
        raise ValueError("invalid tags")
    return row


def read_jsonl(path, validator):
    rows = []
    with open(path, encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            try:
                rows.append(validator(json.loads(line)))
            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError("invalid row {}: {}".format(number, exc)) from exc
    return rows


def state_path(directory):
    directory = Path(directory)
    if directory.is_symlink():
        raise ValueError("state directory cannot be a symlink")
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "state.json"
    if path.is_symlink():
        raise ValueError("state file cannot be a symlink")
    return path


def load(directory):
    path = state_path(directory)
    if not path.exists():
        return {"events": [], "drafts": [], "approved": []}
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def save(directory, state):
    path = state_path(directory)
    fd, temp = tempfile.mkstemp(prefix=".state-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(canonical(state) + "\n")
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def ingest(state, events):
    existing = {row["id"]: row for row in state["events"]}
    for row in events:
        validate_event(row)
        old = existing.get(row["id"])
        if old is not None and old != row:
            raise ValueError("event id collision: " + row["id"])
        existing[row["id"]] = row
    updated = sorted(existing.values(), key=lambda row: row["id"])
    if updated != state["events"]:
        state["drafts"] = []
    state["events"] = updated


def refine(state):
    drafts = []
    for event in state["events"]:
        match = next((d for d in drafts if d["kind"] == event["kind"] and char_bigram_jaccard(d["text"], event["text"]) >= .9), None)
        if match:
            match["source_ids"].append(event["id"])
            match["tags"] = sorted(set(match["tags"] + event["tags"]))
        else:
            drafts.append({"kind": event["kind"], "text": event["text"], "tags": sorted(set(event["tags"])), "source_ids": [event["id"]]})
    state["drafts"] = [{**d, "hash": digest(d)} for d in drafts]
    return state["drafts"]


def promote(state, draft_hash):
    if not isinstance(draft_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", draft_hash):
        raise ValueError("invalid draft hash")
    matches = [d for d in state["drafts"] if d["hash"] == draft_hash and digest({k: v for k, v in d.items() if k != "hash"}) == draft_hash]
    if len(matches) != 1:
        raise ValueError("reviewed draft hash is not current")
    if not any(d["hash"] == draft_hash for d in state["approved"]):
        state["approved"].append(matches[0].copy())


def recall(state, query):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must not be empty")
    words = set(re.split(r"[\s\-_]+", query.lower()))
    ranked = []
    for d in state["approved"]:
        if digest({k: v for k, v in d.items() if k != "hash"}) != d.get("hash"):
            raise ValueError("approved content failed integrity check")
        score = score_page({"title": d["text"], "tags": d["tags"]}, query.lower(), words)
        if score:
            ranked.append({"score": score, "draft": d})
    return sorted(ranked, key=lambda x: (-x["score"], x["draft"]["hash"]))


def lexical_carryover(reference, response, negative_control):
    """Compare lexical overlap with a reference and an unrelated control.

    This is descriptive overlap, not a causal utility estimate.
    """
    if any(not isinstance(value, str) or not value.strip() for value in (reference, response, negative_control)):
        raise ValueError("carryover texts must be nonempty strings")
    observed = char_bigram_jaccard(reference, response)
    control = char_bigram_jaccard(reference, negative_control)
    return {"observed_overlap": observed, "negative_control_overlap": control, "difference": observed - control, "causal_utility_established": False}


def validate_judgment(row):
    fields = {"schema_version", "rubric_version", "id", "session_id", "channel", "condition", "judgment"}
    if not isinstance(row, dict) or set(row) != fields or type(row["schema_version"]) is not int or row["schema_version"] != 1:
        raise ValueError("invalid judgment fields or version")
    if row["rubric_version"] != "fixture-v1":
        raise ValueError("unsupported rubric version")
    checked_id(row["id"])
    checked_id(row["session_id"])
    checked_id(row["channel"])
    labels = {"on": {"helped", "neutral", "noise", "harmed", "unknown", "unclear"}, "holdout": {"rederived", "not_rederived", "unknown", "unclear"}}
    if row["condition"] not in labels or row["judgment"] not in labels[row["condition"]]:
        raise ValueError("invalid judgment")
    return row


def evaluate(rows):
    seen = set()
    sessions = {}
    out = {}
    for row in rows:
        validate_judgment(row)
        if row["id"] in seen:
            raise ValueError("duplicate judgment id")
        seen.add(row["id"])
        session_key = (row["channel"], row["session_id"])
        if session_key in sessions and sessions[session_key] != row["condition"]:
            raise ValueError("session assigned to both conditions")
        sessions[session_key] = row["condition"]
    for channel in sorted({r["channel"] for r in rows}):
        out[channel] = {}
        for condition in ("on", "holdout"):
            subset = [r for r in rows if r["channel"] == channel and r["condition"] == condition]
            counts = {v: sum(r["judgment"] == v for r in subset) for v in sorted({"helped", "neutral", "noise", "harmed", "unknown", "unclear"} if condition == "on" else {"rederived", "not_rederived", "unknown", "unclear"})}
            n = len(subset)
            out[channel][condition] = {"sessions": len({r["session_id"] for r in subset}), "judgments": n, "counts": counts, "rates": {k: v / n if n else None for k, v in counts.items()}}
    return {"schema_version": 1, "rubric_version": "fixture-v1", "channels": out, "interpretation": "Descriptive fixture judgments; carryover is possible and causal utility is not established."}
