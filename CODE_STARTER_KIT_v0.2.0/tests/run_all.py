#!/usr/bin/env python3
"""Run every test and classify the result.  [PROVIDED]  v0.1.1

    PASS              green, not marked todo
    EXPECTED_RED      red, marked @todo(...) **and** the only exception raised
                      was NotImplementedError (i.e. genuinely "not written yet")
    FAIL / ERROR      anything else: TypeError, AttributeError, AssertionError,
                      KeyError, ... even inside a @todo test. A real bug is
                      never allowed to hide behind an "expected" label.
    SKIP              unittest skipTest(); never counted as PASS
    UNEXPECTED_GREEN  green while still marked @todo -> remove the marker

Exit code:
    0  all green (no SKIP, no EXPECTED_RED, no FAIL)
    1  at least one FAIL / ERROR
    2  work remains (EXPECTED_RED > 0)
    3  a test was SKIPPED (unverified behaviour - look at it)
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

MARK = "__ga7_todo__"
EXPECTED_EXC = "NotImplementedError"

PASS = "PASS"
EXPECTED_RED = "EXPECTED_RED"
FAIL = "FAIL"
SKIP = "SKIP"
UNEXPECTED_GREEN = "UNEXPECTED_GREEN"
ORDER = (PASS, EXPECTED_RED, FAIL, SKIP, UNEXPECTED_GREEN)


class CapturingResult(unittest.TestResult):
    """TestResult that remembers WHICH exception types were raised."""

    def __init__(self):
        super().__init__()
        self.exc_types = []

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.exc_types.append(err[0].__name__)

    def addError(self, test, err):
        super().addError(test, err)
        self.exc_types.append(err[0].__name__)


def task_of(test):
    """The @todo marker lives on the test METHOD, not on the TestCase instance."""
    method = getattr(test, getattr(test, "_testMethodName", ""), None)
    return getattr(method, MARK, None) if method is not None else None


def classify_one(test):
    """Return (task_id_or_None, verdict, result)."""
    task = task_of(test)
    res = CapturingResult()
    test.run(res)

    # SKIP must be checked BEFORE wasSuccessful(): a skipped test is "successful".
    if res.skipped:
        return task, SKIP, res

    if res.wasSuccessful():
        return task, (UNEXPECTED_GREEN if task else PASS), res

    # Failing. EXPECTED_RED only when the ONE AND ONLY reason is NotImplementedError.
    if task and res.exc_types and all(t == EXPECTED_EXC for t in res.exc_types):
        return task, EXPECTED_RED, res
    return task, FAIL, res


def _flatten(suite):
    for t in suite:
        if isinstance(t, unittest.TestSuite):
            yield from _flatten(t)
        else:
            yield t


def classify(suite):
    rows = []
    for test in _flatten(suite):
        task, verdict, res = classify_one(test)
        rows.append((test.id().split(".", 1)[-1], task or "-", verdict, res))
    return rows


def main():
    suite = unittest.TestLoader().discover(str(ROOT / "tests"), pattern="test_*.py")
    rows = classify(suite)

    width = max((len(r[0]) for r in rows), default=20)
    print("=" * (width + 26))
    print("%-*s  %-12s  %s" % (width, "TEST", "TASK", "RESULT"))
    print("=" * (width + 26))
    for name, task, verdict, res in rows:
        print("%-*s  %-12s  %s" % (width, name, task, verdict))
    print("=" * (width + 26))

    counts = {k: 0 for k in ORDER}
    for _, _, v, _ in rows:
        counts[v] = counts.get(v, 0) + 1
    print("TOTAL       :", len(rows))
    for k in ORDER:
        print("%-15s:" % k, counts[k])

    todo = sorted({r[1] for r in rows if r[2] == EXPECTED_RED})
    if todo:
        print("\nSTILL TO IMPLEMENT:", ", ".join(todo))

    if counts[FAIL]:
        print("\n>>> RESULT: BREAKAGE (%d test(s) failed for a reason other than "
              "'not implemented yet')" % counts[FAIL])
        return 1
    if counts[SKIP]:
        print("\n>>> RESULT: SKIPPED TESTS (%d) - behaviour not verified" % counts[SKIP])
        return 3
    if todo:
        print("\n>>> RESULT: IN PROGRESS (expected; work through the tasks above)")
        return 2
    print("\n>>> RESULT: ALL GREEN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
