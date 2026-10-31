"""Log-directory boundary tests (regression for the v0.1.1 finding).

v0.1.1 let the CLI hand a user string straight to RunLogger, so
``--log-dir ../../foo`` could write outside the project.
"""
import tempfile
import unittest
from pathlib import Path

from agent.runlog import DEFAULT_LOG_DIR, RunLogger, resolve_log_dir, read_jsonl


class ResolveLogDirTests(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.root = Path(self._td.name)

    def tearDown(self):
        self._td.cleanup()

    def test_empty_defaults_to_logs(self):
        self.assertEqual(resolve_log_dir("", self.root), (self.root / DEFAULT_LOG_DIR).resolve())

    def test_none_defaults_to_logs(self):
        self.assertEqual(resolve_log_dir(None, self.root), (self.root / DEFAULT_LOG_DIR).resolve())

    def test_plain_subdir_is_inside(self):
        target = resolve_log_dir("out/runs", self.root)
        self.assertTrue(str(target).startswith(str(self.root.resolve())))

    def test_parent_traversal_is_rejected(self):
        for bad in ("../outside", "a/../../outside", "..\\outside"):
            with self.assertRaises(ValueError):
                resolve_log_dir(bad, self.root)

    def test_absolute_paths_are_rejected(self):
        for bad in ("/etc", "C:\\Windows\\Temp", "C:relative"):
            with self.assertRaises(ValueError):
                resolve_log_dir(bad, self.root)

    def test_unc_paths_are_rejected(self):
        for bad in ("\\\\localhost\\share", "//localhost/share"):
            with self.assertRaises(ValueError):
                resolve_log_dir(bad, self.root)

    def test_logger_still_accepts_a_validated_path(self):
        target = resolve_log_dir("logs", self.root)
        lg = RunLogger(target, "t-bound")
        lg.event("task", "started")
        lg.final("completed")
        self.assertEqual(len(read_jsonl(lg.jsonl_path)), 2)
        self.assertTrue(str(lg.jsonl_path).startswith(str(self.root.resolve())))


if __name__ == "__main__":
    unittest.main()
