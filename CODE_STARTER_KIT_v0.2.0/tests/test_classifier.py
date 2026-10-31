"""Tests for the test-classifier itself.

These exist because the v0.1.0 classifier had two real bugs:
  * a genuine TypeError inside a @todo test was reported as EXPECTED_RED
  * a skipped test was reported as PASS
Both are reproduced here as negative controls.
"""
import unittest

from tests._harness import todo
from tests.run_all import (
    EXPECTED_RED, FAIL, PASS, SKIP, UNEXPECTED_GREEN, classify_one,
)


def verdict_of(case):
    _task, verdict, _res = classify_one(case)
    return verdict


class ExpectedRedTests(unittest.TestCase):
    def test_not_implemented_inside_todo_is_expected_red(self):
        class C(unittest.TestCase):
            @todo("GA7-D1-01")
            def test_x(self):
                raise NotImplementedError("not yet")

        self.assertEqual(verdict_of(C("test_x")), EXPECTED_RED)


class MaskingRegressionTests(unittest.TestCase):
    """v0.1.0 bug: real exceptions were swallowed by the todo marker."""

    def test_type_error_inside_todo_is_fail(self):
        class C(unittest.TestCase):
            @todo("GA7-D1-01")
            def test_x(self):
                raise TypeError("genuine bug")

        self.assertEqual(verdict_of(C("test_x")), FAIL)

    def test_attribute_error_inside_todo_is_fail(self):
        class C(unittest.TestCase):
            @todo("GA7-D3-01")
            def test_x(self):
                raise AttributeError("genuine bug")
        self.assertEqual(verdict_of(C("test_x")), FAIL)

    def test_assertion_error_inside_todo_is_fail(self):
        class C(unittest.TestCase):
            @todo("GA7-D2-02")
            def test_x(self):
                self.assertEqual(1, 2)

        self.assertEqual(verdict_of(C("test_x")), FAIL)

    def test_key_error_inside_todo_is_fail(self):
        class C(unittest.TestCase):
            @todo("GA7-D5-01")
            def test_x(self):
                raise KeyError("genuine bug")

        self.assertEqual(verdict_of(C("test_x")), FAIL)

    def test_unmarked_failure_is_fail(self):
        class C(unittest.TestCase):
            def test_x(self):
                self.assertEqual(1, 2)

        self.assertEqual(verdict_of(C("test_x")), FAIL)


class SkipRegressionTests(unittest.TestCase):
    """v0.1.0 bug: skipTest() was reported as PASS."""

    def test_skip_is_skip_not_pass(self):
        class C(unittest.TestCase):
            def test_x(self):
                self.skipTest("deliberately skipped")

        self.assertEqual(verdict_of(C("test_x")), SKIP)

    def test_skip_inside_todo_is_skip_not_expected_red(self):
        class C(unittest.TestCase):
            @todo("GA7-D1-01")
            def test_x(self):
                self.skipTest("deliberately skipped")

        self.assertEqual(verdict_of(C("test_x")), SKIP)

    def test_skip_result_reports_skipped(self):
        class C(unittest.TestCase):
            def test_x(self):
                self.skipTest("x")

        _task, _v, res = classify_one(C("test_x"))
        self.assertEqual(len(res.skipped), 1)


class GreenTests(unittest.TestCase):
    def test_plain_pass(self):
        class C(unittest.TestCase):
            def test_x(self):
                pass

        self.assertEqual(verdict_of(C("test_x")), PASS)

    def test_green_while_marked_is_unexpected_green(self):
        class C(unittest.TestCase):
            @todo("GA7-D1-01")
            def test_x(self):
                pass

        self.assertEqual(verdict_of(C("test_x")), UNEXPECTED_GREEN)


class TaskIdTests(unittest.TestCase):
    def test_task_id_is_read_from_the_method(self):
        class C(unittest.TestCase):
            @todo("GA7-D4-02")
            def test_x(self):
                raise NotImplementedError()

        task, verdict, _ = classify_one(C("test_x"))
        self.assertEqual(task, "GA7-D4-02")
        self.assertEqual(verdict, EXPECTED_RED)

    def test_unmarked_test_has_no_task(self):
        class C(unittest.TestCase):
            def test_x(self):
                pass

        task, _, _ = classify_one(C("test_x"))
        self.assertIsNone(task)
