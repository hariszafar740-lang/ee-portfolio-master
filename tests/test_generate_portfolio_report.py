"""
Regression tests for generate_portfolio_report.py

Covers a defect found during audit: when a solver's repository
directory does not exist, the dashboard generator used to report
"FAILED" (red badge) for unit tests and "SECURE" (blue/affirmative
badge) for the security scan -- indistinguishable from an actual test
failure / an actually-clean security scan. Since this script's output
(`portfolio_dashboard.html`) is published live to GitHub Pages on every
push to main (see .github/workflows/deploy_pages.yml), this produced a
misleading public-facing report.

The fix reports "N/A" (neutral grey badge) when a solver directory does
not exist, and only reports PASSED/FAILED or SECURE/FLAGGED once a real
pytest/bandit run has actually taken place.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR))

import generate_portfolio_report as gpr  # noqa: E402


def test_missing_solver_directory_reports_na():
    test_status, sec_status = gpr.gather_solver_metrics("this-folder-does-not-exist")
    assert test_status == "N/A"
    assert sec_status == "N/A"


def test_render_badge_uses_grey_for_na():
    badge = gpr.render_badge("N/A", "PASSED")
    assert "#757575" in badge
    assert "N/A" in badge


def test_render_badge_uses_green_for_good_status():
    badge = gpr.render_badge("PASSED", "PASSED")
    assert "#2e7d32" in badge


def test_render_badge_uses_red_for_bad_status():
    badge = gpr.render_badge("FAILED", "PASSED")
    assert "#c62828" in badge


def test_generate_html_report_does_not_misreport_missing_repos(tmp_path, monkeypatch):
    """None of the 4 solver repos exist in this checkout, so the
    generated dashboard must contain N/A badges for all of them and must
    not claim PASSED/FAILED/SECURE/FLAGGED for repos that were never
    actually tested or scanned."""
    report_file = tmp_path / "portfolio_dashboard.html"
    monkeypatch.setattr(gpr, "REPORT_FILE", report_file)

    gpr.generate_html_report()

    assert report_file.exists()
    html = report_file.read_text(encoding="utf-8")
    assert html.count("N/A") == 2 * len(gpr.SOLVERS)
    assert "FAILED" not in html
    assert "FLAGGED" not in html
