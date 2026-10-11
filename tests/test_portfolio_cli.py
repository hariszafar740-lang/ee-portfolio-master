"""
Regression tests for portfolio_cli.py

These tests specifically cover two defects found during audit:

1. `run_solver()` used to return a bare `False` for an unknown solver key
   but a `(bool, float)` tuple for every other code path, which would
   raise a `ValueError: not enough values to unpack` if ever called with
   an invalid key through any code path other than argparse's own
   `choices` validation.

2. `main()` never propagated solver/test failures to the process exit
   code. This silently broke the documented use case in
   `setup_hooks.sh` / README.md, where `portfolio_cli.py --benchmark` is
   expected to make a pre-commit hook fail (`if [ $? -ne 0 ]`) whenever
   a solver's test suite fails.

Because the four external solver repositories are NOT checked out
inside this repository (they are independent GitHub repos), running
these tests here naturally exercises the "solver directory missing"
path, which previously still returned an exit code of 0.
"""
import subprocess
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR))

import portfolio_cli  # noqa: E402


def test_run_solver_unknown_key_returns_a_tuple():
    """run_solver() must always return a (success, elapsed) tuple so
    callers can safely unpack it, regardless of the key's validity."""
    result = portfolio_cli.run_solver("not-a-real-solver-key")
    assert isinstance(result, tuple)
    assert len(result) == 2
    success, elapsed = result
    assert success is False
    assert isinstance(elapsed, float)


def test_run_solver_missing_directory_reports_failure():
    """When a solver's directory does not exist (as is the case in this
    master repository), run_solver() must report failure rather than
    silently succeeding."""
    success, elapsed = portfolio_cli.run_solver("nr")
    assert success is False
    assert elapsed >= 0


def test_run_benchmark_returns_false_when_any_solver_fails():
    """run_benchmark() must return an overall success flag that is False
    whenever at least one solver did not pass."""
    overall_success = portfolio_cli.run_benchmark()
    # None of the 4 external solver repos are present in this checkout,
    # so the benchmark must be reported as failed overall.
    assert overall_success is False


def test_cli_benchmark_exits_nonzero_on_failure():
    """End-to-end: `python3 portfolio_cli.py --benchmark` must exit with
    a non-zero status code when solvers fail / are missing, so that
    shell quality-gates (`if [ $? -ne 0 ]`) correctly detect the
    failure.

    A `timeout` is used deliberately: before the "missing solver
    directory" fast-path and the "cd && (source || true) && pytest"
    grouping fix were added, a failed `cd` silently fell through to
    running `pytest tests/` in the CURRENT working directory. Since this
    master repo's own `tests/` directory contains this very test, that
    bug caused uncontrolled recursive self-invocation (a process "fork
    bomb") instead of a normal, fast failure. If that regression is ever
    reintroduced, this test fails loudly via TimeoutExpired instead of
    hanging / exhausting the sandbox.
    """
    result = subprocess.run(
        [sys.executable, str(ROOT_DIR / "portfolio_cli.py"), "--benchmark"],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode != 0


def test_cli_prints_help_with_no_args():
    result = subprocess.run(
        [sys.executable, str(ROOT_DIR / "portfolio_cli.py")],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


def test_failed_cd_does_not_fall_through_to_final_command():
    """Pins the root cause of the fork-bomb regression directly: in a
    shell chain `A && B || true && D`, if `A` (cd to the solver
    directory) fails, `D` must NOT run. Without grouping the
    "|| true" clause in a subshell, `((A && B) || true) && D` always
    evaluates to true after a failed `A`, so `D` runs anyway -- using
    whatever the current working directory happens to be.

    This test exercises the exact command-construction pattern used by
    portfolio_cli.py / profile_portfolio.py / generate_portfolio_report.py
    with a harmless marker file instead of pytest, so it is fast and
    cannot recurse.
    """
    marker = Path("/tmp") / f"should_not_exist_{id(object())}.txt"
    marker.unlink(missing_ok=True)
    try:
        cmd = (
            f"cd /no/such/solver/directory && "
            f"(source /no/such/env/bin/activate 2>/dev/null || true) && "
            f"touch {marker}"
        )
        result = subprocess.run(cmd, shell=True, executable="/bin/bash", timeout=10)
        assert result.returncode != 0
        assert not marker.exists(), (
            "The final command ran even though `cd` to a non-existent "
            "directory failed -- the '|| true' grouping regression is back."
        )
    finally:
        marker.unlink(missing_ok=True)
