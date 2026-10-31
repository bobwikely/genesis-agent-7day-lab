"""Test harness helpers.  [PROVIDED]

`@todo("GA7-Dx-yy")` marks a test that CANNOT pass until you implement that
task. The runner reports those as EXPECTED_RED instead of FAIL, and tells you
when you have made one green so you can remove the marker.
"""
from __future__ import annotations

import functools
import json
import tempfile
from pathlib import Path

MARK = "__ga7_todo__"


def todo(task_id):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*a, **kw):
            return fn(*a, **kw)
        setattr(wrapper, MARK, task_id)
        return wrapper
    return deco


class TempWorkspace:
    """A disposable workspace directory with a known file inside."""

    def __enter__(self):
        self._td = tempfile.TemporaryDirectory()
        self.root = Path(self._td.name)
        self.ws = self.root / "ws"
        self.ws.mkdir()
        (self.ws / "notes.txt").write_text("total_lines=3\n", encoding="utf-8")
        self.outside = self.root / "outside.txt"
        self.outside.write_text("SECRET\n", encoding="utf-8")
        return self

    def __exit__(self, *exc):
        self._td.cleanup()
        return False


class RecordingProvider:
    """Wraps a scripted provider and remembers every (task, history) it saw."""

    name = "recording"
    is_real_model = False

    def __init__(self, script):
        self._script = list(script)
        self._i = 0
        self.calls = []

    def describe(self):
        return {"provider": "recording", "real_model": False}

    def decide(self, task, history):
        from agent.providers import ProviderError
        self.calls.append({"task": task, "history": [dict(h) for h in history]})
        if self._i >= len(self._script):
            raise ProviderError("script exhausted")
        item = self._script[self._i]
        self._i += 1
        from agent.decision import Decision
        return Decision.from_payload(item)


def read_log(path):
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
