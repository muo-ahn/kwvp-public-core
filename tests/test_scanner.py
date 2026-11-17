import importlib.util
import tempfile
import unittest
from unittest import mock
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "scripts" / "scan_publication.py"
spec = importlib.util.spec_from_file_location("scanner", path)
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)


class ScannerTests(unittest.TestCase):
    def test_forbidden_names_are_not_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = [root / (".en" + "v"), root / ("certificate." + "pem")]
            # Mock the traversal and metadata; the policy forbids creating these files.
            with mock.patch.object(Path, "rglob", return_value=paths), \
                 mock.patch.object(Path, "is_symlink", return_value=False), \
                 mock.patch.object(Path, "is_file", return_value=True), \
                 mock.patch.object(Path, "read_text", side_effect=AssertionError("forbidden read")):
                self.assertEqual({label for _, label in scanner.scan(root)}, {"environment file", "private key file"})

    def test_finds_risky_material(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "example.txt").write_text("/" + "Users/alice/private\n" + "-----BEGIN " + "PRIVATE KEY-----")
            self.assertTrue(scanner.PATTERNS["environment file"].match(".en" + "v"))
            labels = {label for _, label in scanner.scan(root)}
            self.assertEqual(labels, {"home path", "private key"})


if __name__ == "__main__":
    unittest.main()
