"""Restricted tool registry.  [YOUR JOB - GA7-D3-01 / GA7-D3-02]

Rules you must keep:
  * allow-list only. No shell, no exec, no network, no arbitrary paths.
  * every tool validates its own arguments and raises ToolError on bad input
    (it must NOT let a raw TypeError/KeyError escape).
  * read_file may only read files INSIDE the workspace.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class ToolError(Exception):
    """Bad arguments, boundary violation, or tool-level failure."""


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    parameters: dict
    handler: object


class ToolRegistry:
    """Allow-list registry.  [GA7-D3-01]"""

    def __init__(self):
        self._tools = {}

    def register(self, tool):
        raise NotImplementedError("GA7-D3-01: implement ToolRegistry.register()")

    def get(self, name):
        raise NotImplementedError(
            "GA7-D3-01: implement ToolRegistry.get() raising ToolError for unknown names")

    def names(self):
        raise NotImplementedError("GA7-D3-01: implement ToolRegistry.names()")

    def describe(self):
        raise NotImplementedError("GA7-D3-01: implement ToolRegistry.describe()")


def calculate(expression):
    """Safe arithmetic only.  [GA7-D3-02]

    Use ast parsing with an operator allow-list; reject names, calls,
    attributes, and oversized exponents. Never use eval().
    """
    raise NotImplementedError("GA7-D3-02: implement calculate() using an AST allow-list")


class WorkspaceReader:
    """Reads files strictly inside one workspace.  [GA7-D3-02]

    Must reject: empty path, parent traversal, absolute paths, drive-qualified
    paths (C:foo), UNC paths (\\\\host\\share), and oversized files.
    """

    def __init__(self, workspace, max_bytes=65536):
        self.workspace = Path(workspace).resolve()
        self.max_bytes = max_bytes

    def read_file(self, path):
        raise NotImplementedError(
            "GA7-D3-02: implement WorkspaceReader.read_file() with path boundary checks")


def build_registry(workspace):
    """Return a registry containing exactly two real tools:
    calculator and read_file.  [GA7-D3-01 / GA7-D3-02]
    """
    raise NotImplementedError("GA7-D3-01: implement build_registry()")
