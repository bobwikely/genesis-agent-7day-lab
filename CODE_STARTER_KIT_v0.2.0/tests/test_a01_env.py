"""A1/A2 - Day0 environment and baseline.  These MUST pass on an untouched kit.

TASK IDS COVERED HERE (so a grep-based audit can trace them):
  * GA7-D0-02  environment / baseline record   -> EnvironmentTests.*
  * GA7-D1-02  stop-condition config (max_steps clamping) + log fields
                                               -> EnvironmentTests.test_max_steps_is_clamped
                                               -> LogInfrastructureTests.*
(`GA7-D0-01` is a document deliverable and has no code landing by design.)
"""
import sys
import tempfile
import unittest
from pathlib import Path

from agent.config import AgentConfig
from agent.runlog import REQUIRED_FIELDS, RunLogger, read_jsonl

ROOT = Path(__file__).resolve().parent.parent


class EnvironmentTests(unittest.TestCase):
    def test_python_is_39_or_newer(self):
        # GA7-D0-02
        self.assertGreaterEqual(sys.version_info[:2], (3, 9), "Python >= 3.9 required")

    def test_sample_data_exists_and_is_readable(self):
        # GA7-D0-02
        p = ROOT / "data" / "notes.txt"
        self.assertTrue(p.is_file(), "data/notes.txt missing")
        self.assertGreater(p.stat().st_size, 0, "data/notes.txt is empty")

    def test_default_provider_is_offline_mock(self):
        # GA7-D0-02
        cfg = AgentConfig.from_env()
        self.assertEqual(cfg.provider, "mock", "default must be mock so the kit runs offline")

    def test_max_steps_is_clamped(self):
        # GA7-D1-02
        cfg = AgentConfig(max_steps=999).clamped()
        self.assertLessEqual(cfg.max_steps, 20)


class LogInfrastructureTests(unittest.TestCase):
    def test_logger_writes_all_required_fields(self):
        # GA7-D1-02
        with tempfile.TemporaryDirectory() as td:
            lg = RunLogger(td, "t-env")
            lg.event("task", "started", detail="hello")
            lg.final("completed")
            recs = read_jsonl(lg.jsonl_path)
            self.assertGreaterEqual(len(recs), 2)
            for r in recs:
                for f in REQUIRED_FIELDS:
                    self.assertIn(f, r)
                self.assertEqual(r["task_id"], "t-env")

    def test_step_numbers_are_monotonic(self):
        # GA7-D1-02
        with tempfile.TemporaryDirectory() as td:
            lg = RunLogger(td, "t-mon")
            for _ in range(3):
                lg.event("x", "ok")
            steps = [r["step"] for r in read_jsonl(lg.jsonl_path)]
            self.assertEqual(steps, [1, 2, 3])
