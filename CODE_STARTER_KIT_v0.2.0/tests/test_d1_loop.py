"""GA7-D1-01 / D1-02 - main loop and stop conditions."""
import unittest

from agent.config import AgentConfig
from agent.loop import AgentLoop
from agent.runlog import RunLogger
from tests._harness import RecordingProvider, TempWorkspace, todo


def make(ws, script, max_steps=6, td=None):
    cfg = AgentConfig(provider="mock", max_steps=max_steps,
                      workspace=str(ws), log_dir=str(td or ws))
    return AgentLoop(RecordingProvider(script), __import__("agent.tools", fromlist=["x"]).build_registry(ws),
                     RunLogger(td or ws, "t"), cfg)


class LoopTests(unittest.TestCase):
    @todo("GA7-D1-01")
    def test_final_decision_completes(self):
        with TempWorkspace() as t:
            r = make(t.ws, [{"action": "final", "answer": "done"}], td=t.root).run("x", "t")
            self.assertEqual(r.status, "completed")
            self.assertEqual(r.answer, "done")

    @todo("GA7-D1-01")
    def test_empty_task_is_rejected_before_any_call(self):
        with TempWorkspace() as t:
            loop = make(t.ws, [{"action": "final", "answer": "x"}], td=t.root)
            r = loop.run("   ", "t")
            self.assertEqual(r.status, "input_rejected")
            self.assertEqual(loop.provider.calls, [])

    @todo("GA7-D1-02")
    def test_max_steps_stops_the_loop(self):
        with TempWorkspace() as t:
            script = [{"action": "final", "answer": "never reached"}]
            loop = make(t.ws, script, max_steps=2, td=t.root)
            loop.provider._script = [{"action": "tool", "tool": "calculator",
                                      "arguments": {"expression": "1+1"}}] * 5
            r = loop.run("loop", "t")
            self.assertEqual(r.status, "max_steps")
            self.assertEqual(r.steps, 2)
