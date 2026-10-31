"""GA7-D5-01 - error visibility and bounded failure."""
import unittest

from agent.config import AgentConfig
from agent.loop import AgentLoop
from agent.providers import ProviderError
from agent.runlog import RunLogger
from agent.tools import build_registry
from tests._harness import RecordingProvider, TempWorkspace, read_log, todo


class ErrorTests(unittest.TestCase):
    @todo("GA7-D5-01")
    def test_provider_failure_is_reported_not_crashed(self):
        with TempWorkspace() as t:
            cfg = AgentConfig(max_steps=3, workspace=str(t.ws), log_dir=str(t.root))
            r = AgentLoop(RecordingProvider([]), build_registry(t.ws),
                          RunLogger(t.root, "t"), cfg).run("x", "t")
            self.assertEqual(r.status, "provider_error")

    @todo("GA7-D5-01")
    def test_tool_errors_are_bounded(self):
        with TempWorkspace() as t:
            bad = {"action": "tool", "tool": "shell", "arguments": {}}
            cfg = AgentConfig(max_steps=6, workspace=str(t.ws), log_dir=str(t.root))
            r = AgentLoop(RecordingProvider([bad, dict(bad), dict(bad), dict(bad)]),
                          build_registry(t.ws), RunLogger(t.root, "t"), cfg).run("x", "t")
            self.assertEqual(r.status, "tool_error_limit")

    @todo("GA7-D5-01")
    def test_errors_are_visible_in_the_log(self):
        with TempWorkspace() as t:
            bad = {"action": "tool", "tool": "shell", "arguments": {}}
            cfg = AgentConfig(max_steps=3, workspace=str(t.ws), log_dir=str(t.root))
            lg = RunLogger(t.root, "t")
            AgentLoop(RecordingProvider([bad, dict(bad), dict(bad)]),
                      build_registry(t.ws), lg, cfg).run("x", "t")
            recs = read_log(lg.jsonl_path)
            self.assertTrue(any(r["status"] == "error" for r in recs), "no error record in log")
