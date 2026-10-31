"""GA7-D3-01 / D3-02 - registry, parameter validation, path boundary."""
import unittest

from agent.tools import ToolError, build_registry, calculate
from tests._harness import TempWorkspace, todo


class RegistryTests(unittest.TestCase):
    @todo("GA7-D3-01")
    def test_exact_allow_list(self):
        with TempWorkspace() as t:
            self.assertEqual(build_registry(t.ws).names(), ["calculator", "read_file"])

    @todo("GA7-D3-01")
    def test_no_dangerous_tools(self):
        with TempWorkspace() as t:
            names = build_registry(t.ws).names()
            for bad in ("shell", "exec", "run", "system", "http"):
                self.assertNotIn(bad, names)

    @todo("GA7-D3-01")
    def test_unknown_tool_raises_toolerror(self):
        with TempWorkspace() as t:
            with self.assertRaises(ToolError):
                build_registry(t.ws).get("shell")


class CalculatorTests(unittest.TestCase):
    @todo("GA7-D3-02")
    def test_basic_arithmetic(self):
        self.assertEqual(calculate("2+3*4"), "14")

    @todo("GA7-D3-02")
    def test_rejects_code_injection(self):
        with self.assertRaises(ToolError):
            calculate("__import__('os').system('echo hi')")

    @todo("GA7-D3-02")
    def test_rejects_names(self):
        with self.assertRaises(ToolError):
            calculate("open")


class PathBoundaryTests(unittest.TestCase):
    @todo("GA7-D3-02")
    def test_reads_inside_workspace(self):
        with TempWorkspace() as t:
            self.assertIn("total_lines", build_registry(t.ws).get("read_file").handler("notes.txt"))

    @todo("GA7-D3-02")
    def test_rejects_traversal(self):
        with TempWorkspace() as t:
            h = build_registry(t.ws).get("read_file").handler
            for bad in ("../outside.txt", "sub/../../outside.txt", "..\\outside.txt"):
                with self.assertRaises(ToolError):
                    h(bad)

    @todo("GA7-D3-02")
    def test_rejects_absolute_drive_unc(self):
        with TempWorkspace() as t:
            h = build_registry(t.ws).get("read_file").handler
            for bad in ("C:\\Windows\\win.ini", "C:notes.txt", "\\\\localhost\\c$\\x", "/etc/passwd"):
                with self.assertRaises(ToolError):
                    h(bad)

    @todo("GA7-D3-02")
    def test_rejects_empty_and_non_string(self):
        with TempWorkspace() as t:
            h = build_registry(t.ws).get("read_file").handler
            for bad in ("", "   ", None, 123):
                with self.assertRaises(ToolError):
                    h(bad)
