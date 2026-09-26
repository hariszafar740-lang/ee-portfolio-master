#!/usr/bin/env python3
"""
Automated Static Security Vulnerability & Code Quality Audit Suite
Author: Haris Zafar
"""

import subprocess
from pathlib import Path
from tabulate import tabulate

ROOT_DIR = Path(__file__).parent.resolve()

SOLVERS = [
    ("Power Systems Newton-Raphson Solver", "power-systems-newton-raphson-solver"),
    ("Solar PV Dynamic MPPT Solver", "solar-pv-mppt-dynamic-solver"),
    ("BESS 1RC Electro-Thermal ECM Solver", "bess-soc-dynamics-solver"),
    ("Grid-Forming Inverter Control Solver", "inverter-grid-control-solver")
]

def audit_solver(name, folder):
    solver_dir = ROOT_DIR / folder
    src_dir = solver_dir / "src"
    
    # Check if source directory exists
    if not src_dir.exists():
        return [name, "N/A", "N/A"]

    # Run Bandit AST Security Vulnerability Scan
    bandit_cmd = f"bandit -r {src_dir} -q -f custom --msg-template '{{severity}}:{{cwe}}'"
    bandit_res = subprocess.run(bandit_cmd, shell=True, capture_output=True, text=True)
    sec_status = "PASS" if bandit_res.returncode == 0 else "FLAGGED"

    # Run Flake8 Critical Syntax & Logic Audit
    flake_cmd = f"flake8 {src_dir} --count --select=E9,F63,F7,F82 --show-source --statistics"
    flake_res = subprocess.run(flake_cmd, shell=True, capture_output=True, text=True)
    syntax_status = "PASS" if flake_res.returncode == 0 else "FAIL"

    return [name, sec_status, syntax_status]

def main():
    print("==========================================================================")
    print(" STARTING PORTFOLIO SECURITY VULNERABILITY & CODE QUALITY AUDIT")
    print("==========================================================================")
    
    results = []
    for name, folder in SOLVERS:
        print(f"Auditing security & static quality for: {name}...")
        results.append(audit_solver(name, folder))
        
    print("\n" + tabulate(results, headers=["Solver Module", "Bandit Security Scan", "Flake8 Syntax Audit"], tablefmt="github"))
    print("\nAudit sweep completed successfully.")

if __name__ == "__main__":
    main()
