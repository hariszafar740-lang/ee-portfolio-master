#!/usr/bin/env python3
"""
Automated Multi-Project Portfolio Executive HTML Dashboard & Report Exporter
Author: Haris Zafar
"""

import datetime
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
REPORT_FILE = ROOT_DIR / "portfolio_dashboard.html"

SOLVERS = [
    {"name": "Power Systems Newton-Raphson Solver", "folder": "power-systems-newton-raphson-solver", "domain": "Grid Analysis & Load Flow"},
    {"name": "Solar PV Dynamic MPPT Solver", "folder": "solar-pv-mppt-dynamic-solver", "domain": "Photovoltaics & Control Loops"},
    {"name": "BESS 1RC Electro-Thermal ECM Solver", "folder": "bess-soc-dynamics-solver", "domain": "Battery Energy Storage Systems"},
    {"name": "Grid-Forming Inverter Control Solver", "folder": "inverter-grid-control-solver", "domain": "Microgrid Power Electronics"}
]

def gather_solver_metrics(folder):
    solver_dir = ROOT_DIR / folder

    # If the solver repository has not been checked out alongside this
    # master repository, there is nothing to test or scan. Report "N/A"
    # rather than "FAILED"/"SECURE" -- those labels previously implied a
    # real (and in the case of "SECURE", falsely reassuring) result even
    # though no test run or security scan ever took place.
    if not solver_dir.exists():
        return "N/A", "N/A"

    # 1. Run pytest validation sweep
    # Group "source ... || true" so a failed `cd` (e.g. solver directory
    # not checked out) short-circuits the whole chain instead of falling
    # through to `pytest tests/` in the current working directory. See
    # the equivalent note in portfolio_cli.py for the full rationale.
    pytest_cmd = f"cd {solver_dir} && (source *_env/bin/activate 2>/dev/null || true) && PYTHONPATH=. pytest tests/"
    p_res = subprocess.run(pytest_cmd, shell=True, capture_output=True, text=True, executable="/bin/bash")
    test_status = "PASSED" if p_res.returncode == 0 else "FAILED"

    # 2. Run Bandit security check
    src_dir = solver_dir / "src"
    if src_dir.exists():
        bandit_cmd = f"bandit -r {src_dir} -q 2>/dev/null"
        b_res = subprocess.run(bandit_cmd, shell=True, capture_output=True, text=True)
        sec_status = "SECURE" if b_res.returncode == 0 else "FLAGGED"
    else:
        sec_status = "N/A"

    return test_status, sec_status

def render_badge(status, good_status):
    """Render a status badge: green for the "good" status, grey for the
    neutral "N/A" status (repo not checked out / nothing scanned), and
    red/orange for any other (actual failure/flagged) status."""
    if status == good_status:
        color = "#2e7d32"  # green
    elif status == "N/A":
        color = "#757575"  # grey - no data, not a failure
    else:
        color = "#c62828"  # red
    return f'<span style="background-color: {color}; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">{status}</span>'

def generate_html_report():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    rows_html = ""
    for item in SOLVERS:
        test_status, sec_status = gather_solver_metrics(item["folder"])
        test_badge = render_badge(test_status, "PASSED")
        sec_badge = render_badge(sec_status, "SECURE")
        
        rows_html += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #ddd; font-weight: bold;">{item['name']}</td>
            <td style="padding: 12px; border-bottom: 1px solid #ddd;">{item['domain']}</td>
            <td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center;">{test_badge}</td>
            <td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center;">{sec_badge}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Electrical Engineering Portfolio Executive Dashboard</title>
<style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 40px; color: #333; }}
    .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
    h1 {{ color: #1a237e; border-bottom: 2px solid #1a237e; padding-bottom: 10px; }}
    .meta {{ font-size: 0.9em; color: #666; margin-bottom: 25px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
    th {{ background-color: #1a237e; color: white; padding: 12px; text-align: left; }}
</style>
</head>
<body>
<div class="container">
    <h1>Electrical Engineering Simulation Portfolio</h1>
    <div class="meta"><strong>Author:</strong> Haris Zafar | <strong>Generated:</strong> {timestamp}</div>
    <p>Executive compliance, test coverage, and security audit metrics for all open-source power system solvers.</p>
    <table>
        <thead>
            <tr>
                <th>Solver Module</th>
                <th>Engineering Domain</th>
                <th style="text-align: center;">Unit Test Status</th>
                <th style="text-align: center;">Security Audit</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
</div>
</body>
</html>
"""
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Executive HTML Dashboard successfully generated at: {REPORT_FILE}")

if __name__ == "__main__":
    print("==========================================================================")
    print(" GENERATING PORTFOLIO EXECUTIVE HTML DASHBOARD & METRICS REPORT")
    print("==========================================================================")
    generate_html_report()
