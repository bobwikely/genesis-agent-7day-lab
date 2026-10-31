"""Structured decision produced by a provider.  [YOUR JOB - GA7-D2-02]

A model returns arbitrary text. This module is the gate that turns it into
something the loop is allowed to act on. Anything invalid must be REJECTED,
never executed.
"""
from __future__ import annotations

from dataclasses import dataclass, field


class DecisionError(ValueError):
    """Payload is not a usable decision."""


@dataclass
class Decision:
    kind: str                                  # "tool" | "final"
    tool: str | None = None
    arguments: dict = field(default_factory=dict)
    answer: str | None = None
    thought: str = ""

    @staticmethod
    def from_payload(payload):
        """Validate a raw payload (already parsed from JSON) into a Decision.

        MUST reject:
          * non-dict payload
          * action other than "tool" / "final"
          * action=="tool" with missing/empty tool name
          * action=="tool" with arguments that is not a dict
          * action=="final" with missing/blank answer
        Each rejection raises DecisionError with a message naming the field.
        """
        raise NotImplementedError(
            "GA7-D2-02: implement Decision.from_payload() with field-level rejection")
