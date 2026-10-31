"""GA7-D2-01 - provider must not be interchangeable with a real model."""
import unittest

from agent.config import AgentConfig
from agent.providers import MockProvider, ProviderError, build_provider
from tests._harness import todo


class ProviderTests(unittest.TestCase):
    def test_mock_is_explicitly_not_a_real_model(self):
        p = MockProvider([])
        self.assertFalse(p.is_real_model)
        self.assertFalse(p.describe()["real_model"])

    def test_unknown_provider_is_rejected(self):
        with self.assertRaises(ProviderError):
            build_provider(AgentConfig(provider="magic"))

    def test_ollama_without_model_name_is_rejected(self):
        with self.assertRaises(ProviderError):
            build_provider(AgentConfig(provider="ollama", model=""))

    @todo("GA7-D2-01")
    def test_unreachable_ollama_raises_provider_error_not_crash(self):
        """A real provider must FAIL LOUDLY when the backend is absent.

        No model, no key, no network: we point at a closed local port.
        """
        from agent.providers import OllamaProvider
        p = OllamaProvider("http://127.0.0.1:9", "does-not-matter", timeout=3)
        with self.assertRaises(ProviderError):
            p.decide("hello", [])
