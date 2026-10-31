"""GA7-D4-01 / D4-02 - tool result feedback and multi-step dependency."""
import unittest

from agent.config import AgentConfig
from agent.loop import AgentLoop
from agent.runlog import RunLogger
from agent.tools import build_registry
from tests._harness import RecordingProvider, TempWorkspace, todo


class FeedbackTests(unittest.TestCase):
    @todo("GA7-D4-01")
    def test_second_decide_sees_first_result(self):
        with TempWorkspace() as t:
            script = [
                {"action": "tool", "tool": "calculator", "arguments": {"expression": "6*7"}},
                {"action": "final", "answer": "42"},
            ]
            prov = RecordingProvider(script)
            cfg = AgentConfig(max_steps=4, workspace=str(t.ws), log_dir=str(t.root))
            r = AgentLoop(prov, build_registry(t.ws), RunLogger(t.root, "t"), cfg).run("calc", "t")
            self.assertEqual(r.status, "completed")
            self.assertGreaterEqual(len(prov.calls), 2)
            second_history = prov.calls[1]["history"]
            self.assertTrue(second_history, "history passed to the 2nd decide() was empty")
            self.assertIn("42", str(second_history))

    @todo("GA7-D4-02")
    def test_result_is_recorded_in_history(self):
        with TempWorkspace() as t:
            script = [
                {"action": "tool", "tool": "calculator", "arguments": {"expression": "2+2"}},
                {"action": "final", "answer": "4"},
            ]
            cfg = AgentConfig(max_steps=4, workspace=str(t.ws), log_dir=str(t.root))
            r = AgentLoop(RecordingProvider(script), build_registry(t.ws),
                          RunLogger(t.root, "t"), cfg).run("calc", "t")
            self.assertTrue(any("4" in str(h) for h in r.history), "tool result missing from history")
