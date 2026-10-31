"""Configuration. Env-driven, no secrets ever stored here.  [PROVIDED]"""
from __future__ import annotations

import os
from dataclasses import dataclass

MOCK = "mock"
OLLAMA = "ollama"

DEFAULT_MAX_STEPS = 6
HARD_MAX_STEPS = 20
MAX_TASK_CHARS = 2000


@dataclass(frozen=True)
class AgentConfig:
    provider: str = MOCK
    base_url: str = "http://127.0.0.1:11434"
    model: str = ""
    timeout: float = 120.0
    max_steps: int = DEFAULT_MAX_STEPS
    workspace: str = "data"
    log_dir: str = "logs"

    @staticmethod
    def from_env():
        return AgentConfig(
            provider=os.environ.get("GA7_PROVIDER", MOCK).strip().lower(),
            base_url=os.environ.get("GA7_OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
            model=os.environ.get("GA7_OLLAMA_MODEL", ""),
            timeout=float(os.environ.get("GA7_TIMEOUT", "120")),
            max_steps=int(os.environ.get("GA7_MAX_STEPS", str(DEFAULT_MAX_STEPS))),
            workspace=os.environ.get("GA7_WORKSPACE", "data"),
            log_dir=os.environ.get("GA7_LOG_DIR", "logs"),
        )

    def clamped(self):
        return AgentConfig(
            provider=self.provider,
            base_url=self.base_url,
            model=self.model,
            timeout=self.timeout,
            max_steps=max(1, min(int(self.max_steps), HARD_MAX_STEPS)),
            workspace=self.workspace,
            log_dir=self.log_dir,
        )
