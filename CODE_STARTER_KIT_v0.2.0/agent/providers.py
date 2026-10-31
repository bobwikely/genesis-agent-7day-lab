"""Provider layer.  [PARTLY PROVIDED]

PROVIDED : Provider protocol + MockProvider (offline, no key, no network).
YOUR JOB : implement OllamaProvider.decide()  ->  GA7-D2-01
"""
from __future__ import annotations

from .decision import Decision


class ProviderError(Exception):
    """Model backend unusable. NEVER silently fall back to Mock."""


class MockProvider:
    """Deterministic scripted provider. OFFLINE. This is NOT a real model.

    Every log written while using this provider must be labelled MOCK.
    """

    name = "mock"
    is_real_model = False

    def __init__(self, script):
        self._script = list(script)
        self._i = 0

    def describe(self):
        return {"provider": self.name, "real_model": False,
                "script_len": len(self._script)}

    def decide(self, task, history):
        if self._i >= len(self._script):
            raise ProviderError("mock script exhausted")
        item = self._script[self._i]
        self._i += 1
        return Decision.from_payload(item)


class OllamaProvider:
    """Real local model over HTTP.  [YOUR JOB - GA7-D2-01]

    Requirements:
      * build a request to <base_url>/api/chat with JSON body
      * parse the assistant content into a Decision via Decision.from_payload
      * on unreachable/timeout/non-JSON -> raise ProviderError (never fall back)
      * never send or store an API key
    """

    name = "ollama"
    is_real_model = True

    def __init__(self, base_url, model, timeout=120.0, tool_specs=None):
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self.tool_specs = tool_specs or []

    def describe(self):
        return {"provider": self.name, "real_model": True,
                "base_url": self.base_url, "model": self.model}

    def decide(self, task, history):
        raise NotImplementedError(
            "GA7-D2-01: implement OllamaProvider.decide() "
            "(POST /api/chat, parse JSON, raise ProviderError on failure)")


def build_provider(cfg, registry=None):
    """Factory. Mock is the default so the kit works fully offline."""
    if cfg.provider == "mock":
        return MockProvider([])
    if cfg.provider == "ollama":
        if not cfg.model:
            raise ProviderError("GA7-D2-01: GA7_OLLAMA_MODEL is empty; "
                                "set it in .env or use GA7_PROVIDER=mock")
        specs = registry.describe() if registry else []
        return OllamaProvider(cfg.base_url, cfg.model, cfg.timeout, specs)
    raise ProviderError("unknown provider: " + str(cfg.provider))
