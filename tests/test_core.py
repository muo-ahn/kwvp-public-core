import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from kwvp_core import core

ROOT = Path(__file__).resolve().parents[1]


class PipelineTests(unittest.TestCase):
    def test_algorithms(self):
        self.assertEqual(core.char_bigram_jaccard("", ""), 0)
        self.assertEqual(core.char_bigram_jaccard("ABC", "abc"), 1)
        self.assertEqual(core.score_page({"tags": ["rollout", "core"], "title": "staged rollout"}, "staged rollout", {"staged", "rollout"}), 10)
        self.assertTrue(core.is_suppressed(4, 0, 0, 0))
        self.assertFalse(core.is_suppressed(4, 1, 0, 0))
        self.assertTrue(core.is_suppressed(8, 5, 1, 1))
        with self.assertRaises(ValueError):
            core.is_suppressed(1, 2, 0, 0)

    def test_review_recall_and_provenance(self):
        state = {"events": [], "drafts": [], "approved": []}
        events = core.read_jsonl(ROOT / "examples/events.jsonl", core.validate_event)
        core.ingest(state, events)
        core.ingest(state, events)
        drafts = core.refine(state)
        draft = next(d for d in drafts if d["kind"] == "Decision")
        self.assertEqual(draft["source_ids"], ["e1", "e2"])
        self.assertEqual(core.recall(state, "rollout"), [])
        core.promote(state, draft["hash"])
        core.promote(state, draft["hash"])
        self.assertEqual(len(core.recall(state, "rollout")), 1)
        self.assertEqual(core.recall(state, "xylophone"), [])
        draft["text"] = "tampered"
        with self.assertRaises(ValueError):
            core.promote(state, draft["hash"])

    def test_stale_and_tampered_approval(self):
        state = {"events": [], "drafts": [], "approved": []}
        events = core.read_jsonl(ROOT / "examples/events.jsonl", core.validate_event)
        core.ingest(state, events[:1])
        draft = core.refine(state)[0]
        old_hash = draft["hash"]
        core.promote(state, old_hash)
        core.ingest(state, events[1:])
        with self.assertRaises(ValueError):
            core.promote(state, old_hash)
        self.assertTrue(core.recall(state, "rollout"))
        core.refine(state)
        self.assertNotEqual(state["drafts"][0]["hash"], old_hash)
        state["approved"][0]["text"] = "changed after approval"
        with self.assertRaises(ValueError):
            core.recall(state, "rollout")

    def test_carryover_control(self):
        result = core.lexical_carryover("staged rollout", "staged rollout", "xylophone")
        self.assertGreater(result["difference"], 0)
        self.assertFalse(result["causal_utility_established"])

    def test_evaluation(self):
        rows = core.read_jsonl(ROOT / "examples/judgments.jsonl", core.validate_judgment)
        self.assertEqual(core.evaluate(rows), json.loads((ROOT / "examples/evaluation-expected.json").read_text()))
        report = core.evaluate(rows)["channels"]["fixture"]
        self.assertEqual(report["on"]["sessions"], 1)
        self.assertEqual(report["on"]["judgments"], 2)
        self.assertEqual(report["holdout"]["counts"]["unknown"], 1)
        empty = core.evaluate(rows[:2])["channels"]["fixture"]["holdout"]
        self.assertIsNone(empty["rates"]["rederived"])
        with self.assertRaises(ValueError):
            core.evaluate(rows + [rows[0]])
        with self.assertRaises(ValueError):
            core.validate_judgment(dict(rows[0], rubric_version="fixture-v2"))
        with self.assertRaises(ValueError):
            core.validate_judgment(dict(rows[0], condition="holdout"))
        bad = dict(rows[0], condition="holdout", judgment="unknown", id="different")
        with self.assertRaises(ValueError):
            core.evaluate(rows + [bad])

    def test_rejection_and_symlink(self):
        event = {"schema_version": 1, "id": "../escape", "session_id": "s", "kind": "Decision", "text": "x", "tags": []}
        with self.assertRaises(ValueError):
            core.validate_event(event)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "state.json").symlink_to(root / "other")
            with self.assertRaises(ValueError):
                core.load(root)
            invalid = root / "invalid.jsonl"
            invalid.write_text('{"bad": true}\n')
            with self.assertRaises(ValueError):
                core.read_jsonl(invalid, core.validate_event)

    def test_cli_evaluate_does_not_create_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "not-created"
            cmd = [sys.executable, "-m", "kwvp_core.cli", "--state", str(state), "evaluate", str(ROOT / "examples/judgments.jsonl")]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(result.stdout), json.loads((ROOT / "examples/evaluation-expected.json").read_text()))
            self.assertFalse(state.exists())

    def test_cli_demo_stops_before_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            cmd = [sys.executable, "-m", "kwvp_core.cli", "--state", tmp]
            demo = subprocess.run(cmd + ["demo"], capture_output=True, text=True, check=True)
            draft = json.loads(demo.stdout)[0]
            self.assertEqual(json.loads(subprocess.check_output(cmd + ["recall", "rollout"])), [])
            subprocess.run(cmd + ["promote", draft["hash"]], check=True, capture_output=True)
            self.assertEqual(len(json.loads(subprocess.check_output(cmd + ["recall", "rollout"]))), 1)


if __name__ == "__main__":
    unittest.main()
