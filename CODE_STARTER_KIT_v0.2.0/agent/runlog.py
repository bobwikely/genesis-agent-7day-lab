"""Structured run log: JSONL + human mirror.  [PROVIDED]

Every step becomes one JSON line. Fields are the evidence basis for A4/A14.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_FIELDS = ("ts", "task_id", "step", "kind", "status")


class RunLogger:
    def __init__(self, log_dir, task_id: str):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.task_id = task_id
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.jsonl_path = self.log_dir / ("run_" + stamp + "_" + task_id + ".jsonl")
        self.text_path = self.log_dir / ("run_" + stamp + "_" + task_id + ".log")
        self._n = 0

    def event(self, kind, status, detail="", tool=None, args_summary="",
              result_summary="", error=None):
        self._n += 1
        rec = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "task_id": self.task_id,
            "step": self._n,
            "kind": kind,
            "status": status,
            "tool": tool,
            "args_summary": str(args_summary)[:200],
            "result_summary": str(result_summary)[:300],
            "error": error,
            "detail": str(detail)[:400],
        }
        with self.jsonl_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        line = "[{0}] step={1:<2} {2:<9} {3:<12} {4}".format(
            rec["ts"], rec["step"], rec["kind"], rec["status"], rec["detail"])
        with self.text_path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        return rec

    def final(self, status, detail=""):
        return self.event("run_end", status, detail)


def read_jsonl(path):
    """Helper used by tests and by the evidence collector."""
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out

DEFAULT_LOG_DIR = "logs"


def resolve_log_dir(raw, root):
    """Map a user-supplied log directory onto a path INSIDE the project root.

    Why this exists: ``RunLogger`` accepts any Path so that tests can use
    temporary directories. That means the CLI must not pass a user string
    straight through, or ``--log-dir ../../somewhere`` would write outside the
    project. This function is the single validated entry point for that input.

    Raises:
        ValueError: absolute path, drive-qualified path (``C:foo``), UNC path,
                    or any path that resolves outside ``root``.
    """
    text = (raw or "").strip()
    if not text:
        text = DEFAULT_LOG_DIR
    if text.startswith(("\\\\", "//")):
        raise ValueError("log dir must be a relative path inside the project")
    candidate = Path(text)
    if candidate.drive or candidate.is_absolute():
        raise ValueError("log dir must be a relative path inside the project")
    root_resolved = Path(root).resolve()
    target = (root_resolved / text).resolve()
    if target != root_resolved and root_resolved not in target.parents:
        raise ValueError("log dir escapes the project directory")
    return target
