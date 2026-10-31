#!/usr/bin/env python3
"""Run one task through your agent.  [PROVIDED]

    python run_demo.py --task "read notes.txt and tell me the line count"
    python run_demo.py --task "..." --provider mock --script examples/mock_calc.json
"""
import argparse
import sys
import uuid
from pathlib import Path

from agent.config import AgentConfig
from agent.providers import MockProvider, ProviderError, build_provider
from agent.runlog import RunLogger, resolve_log_dir
from agent.tools import build_registry

import json


def main(argv=None):
    cfg = AgentConfig.from_env().clamped()
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--provider", default=cfg.provider, choices=["mock", "ollama"])
    ap.add_argument("--script", default=None, help="JSON file with a Mock decision script")
    ap.add_argument("--max-steps", dest="max_steps", type=int, default=cfg.max_steps)
    ap.add_argument("--workspace", default=cfg.workspace)
    ap.add_argument("--log-dir", dest="log_dir", default=cfg.log_dir)
    a = ap.parse_args(argv)

    cfg = AgentConfig(provider=a.provider, base_url=cfg.base_url, model=cfg.model,
                      timeout=cfg.timeout, max_steps=a.max_steps,
                      workspace=a.workspace, log_dir=a.log_dir).clamped()

    task_id = uuid.uuid4().hex[:8]
    try:
        log_path = resolve_log_dir(cfg.log_dir, Path.cwd())
    except ValueError as exc:
        print("INVALID --log-dir:", exc, file=sys.stderr)
        return 2
    logger = RunLogger(log_path, task_id)

    try:
        registry = build_registry(Path(cfg.workspace))
    except NotImplementedError as exc:
        print("NOT_IMPLEMENTED:", exc, file=sys.stderr)
        print("This is expected on a fresh kit. Start with agent/tools.py (GA7-D3-01).",
              file=sys.stderr)
        return 3

    if cfg.provider == "mock":
        if not a.script:
            print("ERROR: --provider mock needs --script <file.json>", file=sys.stderr)
            return 2
        provider = MockProvider(json.loads(Path(a.script).read_text(encoding="utf-8")))
    else:
        try:
            provider = build_provider(cfg, registry)
        except ProviderError as exc:
            print("PROVIDER_ERROR:", exc, file=sys.stderr)
            return 4

    print("MODEL SOURCE:", "MOCK (no real model was called)" if not provider.is_real_model
          else "REAL (%s)" % cfg.model)
    print("task_id :", task_id, "| max_steps:", cfg.max_steps)
    print("-" * 56)

    from agent.loop import AgentLoop
    try:
        result = AgentLoop(provider, registry, logger, cfg).run(a.task, task_id)
    except NotImplementedError as exc:
        print("NOT_IMPLEMENTED:", exc, file=sys.stderr)
        return 3

    print("-" * 56)
    print("status:", result.status, "| steps:", result.steps)
    if result.answer:
        print("answer:", result.answer)
    print("log   :", logger.jsonl_path)
    return 0 if result.status == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
