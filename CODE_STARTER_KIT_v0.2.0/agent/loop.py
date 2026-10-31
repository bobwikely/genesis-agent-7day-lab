"""The agent loop.  [YOUR JOB - GA7-D1-01 / D1-02 / D4 / D5]

Five stages, every iteration:
    OBSERVE   the task and the history you feed back
    DECIDE    ask the provider for a Decision
    ACT       run the chosen tool (only if the decision validates)
    OBSERVE   record the tool result
    TERMINATE or continue

Hard requirements:
  * a step ceiling that actually stops the loop
  * a bounded number of tool errors before giving up
  * an empty task is rejected before anything runs
  * every stage writes a structured log line
"""
from __future__ import annotations

from dataclasses import dataclass, field

MAX_TOOL_ERRORS = 3

# Allowed values of RunResult.status. Do not invent new ones.
STATUS_COMPLETED = "completed"
STATUS_MAX_STEPS = "max_steps"
STATUS_PROVIDER_ERROR = "provider_error"
STATUS_TOOL_ERROR_LIMIT = "tool_error_limit"
STATUS_INPUT_REJECTED = "input_rejected"


@dataclass
class RunResult:
    task_id: str
    status: str
    steps: int
    answer: str | None = None
    reason: str = ""
    history: list = field(default_factory=list)


class AgentLoop:
    def __init__(self, provider, registry, logger, config):
        self.provider = provider
        self.registry = registry
        self.logger = logger
        self.config = config

    def run(self, task, task_id):
        """Drive the agent until it finishes or must stop.

        Return a RunResult whose status is one of the STATUS_* constants.
        Log at least: task start, each decision, each tool result, final stop.
        Append each tool result to history so the next decide() can see it.
        """
        raise NotImplementedError(
            "GA7-D1-01: implement AgentLoop.run() (observe/decide/act/observe/terminate)")
