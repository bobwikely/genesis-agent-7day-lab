#!/usr/bin/env python3
"""Day0 environment self-check (GA7-D0-02).  [PROVIDED]

    python scripts/check_env.py
Paste the output into EVIDENCE/D0/E-D0-02_BASELINE.md
"""
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def main():
    print("=== GA7 Day0 environment check ===")
    print("python      :", platform.python_version())
    print("executable  :", sys.executable)
    print("platform    :", platform.platform())
    print("machine     :", platform.machine())
    print("data/notes.txt :", "OK" if (ROOT / "data" / "notes.txt").is_file() else "MISSING")
    try:
        from agent.config import AgentConfig
        cfg = AgentConfig.from_env()
        print("provider    :", cfg.provider, "(mock = offline, no key, no model download)")
        print("max_steps   :", cfg.max_steps)
    except Exception as exc:
        print("config      : ERROR", exc)
        return 1
    try:
        import unittest  # noqa: F401
        print("unittest    : available")
    except Exception:
        print("unittest    : MISSING")
        return 1
    print("=== OK: you can run the tests ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
