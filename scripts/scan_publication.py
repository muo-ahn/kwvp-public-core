"""Heuristic publication scan; findings require human review, clean is not proof."""
import argparse
import re
import sys
from pathlib import Path

PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "home path": re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+/"),
    "environment file": re.compile(r"^\.env(?:\..*)?$"),
    "credential token": re.compile(r"\b(?:sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b"),
}
SKIP = {".git", ".ruff_cache", "__pycache__", ".venv", "build", "dist"}


def scan(root):
    root = Path(root)
    findings = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP or part.endswith(".egg-info") for part in rel.parts):
            continue
        if path.is_symlink():
            findings.append((str(rel), "symlink"))
            continue
        if not path.is_file():
            continue
        if PATTERNS["environment file"].match(path.name):
            findings.append((str(rel), "environment file"))
            continue
        if path.name.lower().endswith(".pem"):
            findings.append((str(rel), "private key file"))
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            findings.append((str(rel), "unreadable or binary"))
            continue
        for label, pattern in PATTERNS.items():
            if label != "environment file" and pattern.search(content):
                findings.append((str(rel), label))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root")
    args = parser.parse_args()
    for path, label in scan(args.root):
        print("{}: {}".format(path, label))
    return int(bool(scan(args.root)))


if __name__ == "__main__":
    sys.exit(main())
