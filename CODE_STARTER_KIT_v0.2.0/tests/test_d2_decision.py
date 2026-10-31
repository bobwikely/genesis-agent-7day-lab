"""GA7-D2-02 - structured decision validation."""
import unittest

from agent.decision import Decision, DecisionError
from tests._harness import todo


class DecisionTests(unittest.TestCase):
    @todo("GA7-D2-02")
    def test_accepts_tool_decision(self):
        d = Decision.from_payload({"action": "tool", "tool": "calculator",
                                   "arguments": {"expression": "1+1"}})
        self.assertEqual((d.kind, d.tool), ("tool", "calculator"))

    @todo("GA7-D2-02")
    def test_accepts_final_decision(self):
        d = Decision.from_payload({"action": "final", "answer": "42"})
        self.assertEqual((d.kind, d.answer), ("final", "42"))

    @todo("GA7-D2-02")
    def test_rejects_non_dict(self):
        for bad in ([1, 2], "text", 7, None):
            with self.assertRaises(DecisionError):
                Decision.from_payload(bad)

    @todo("GA7-D2-02")
    def test_rejects_unknown_action(self):
        with self.assertRaises(DecisionError):
            Decision.from_payload({"action": "delete_all"})

    @todo("GA7-D2-02")
    def test_rejects_tool_without_name(self):
        with self.assertRaises(DecisionError):
            Decision.from_payload({"action": "tool", "arguments": {}})

    @todo("GA7-D2-02")
    def test_rejects_non_dict_arguments(self):
        with self.assertRaises(DecisionError):
            Decision.from_payload({"action": "tool", "tool": "calculator", "arguments": "1+1"})

    @todo("GA7-D2-02")
    def test_rejects_blank_final_answer(self):
        with self.assertRaises(DecisionError):
            Decision.from_payload({"action": "final", "answer": "   "})
