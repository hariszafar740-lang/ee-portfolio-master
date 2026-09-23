#!/usr/bin/env python3
"""
Unified Electrical Engineering Portfolio Simulation Orchestrator
Author: Haris Zafar
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path
from tabulate import tabulate

ROOT_DIR = Path(__file__).parent.resolve()

SOLVERS = {
    "nr": {
        "name": "Power Systems Newton-Raphson Load Flow Solver",
        "dir": "power-systems-newton-raphson-solver",
        "venv": "nr_env",
        "entry": "src/main.py"
    },
    "pv": {
        "name": "Solar PV Dynamic MPPT Solver",
        "dir": "solar-pv-mppt-dynamic-solver",
        "venv": "pv_env",
        "entry": "src/main.py"
    },
    "bess": {
        "name": "BESS 1RC Electro-Thermal ECM Solver",
        "dir": "bess-soc-dynamics-solver",
        "venv": "bess_env",
        "entry": "src/main.py"
    },
    "inverter": {
        "name": "Grid-Forming Inverter Control Solver",
        "dir": "inverter-grid-control-solver",
        "venv": "inverter_env",
        "entry": "src/main.py"
    }
}

def run_solver(key):
    if key not in SOLVERS:
        print(f"Error: Unknown solver key '{key}'")
        return False
    
    info = SOLVERS[key]
    solver_path = ROOT_DIR / info["dir"]
    print(f"\n==================================================")
    print(f" Executing: {info['name']}")
    print(f"==================================================")

    cmd = f"cd {solver_path} && source *_env/bin/activate 2>/dev/null || true && PYTHONPATH=. pytest tests/"
    start_time = time.time()
    res = subprocess.run(cmd, shell=True, executable="/bin/bash")
    elapsed = time.time() - start_time

    print(f"Status: {'PASSED' if res.returncode == 0 else 'FAILED'} | Execution Time: {elapsed:.2f}s\n")
    return res.returncode == 0, elapsed

def run_benchmark():
    print("\n==================================================")
    print(" Running Master Portfolio Benchmark Suite")
    print("==================================================")
    results = []
    for key, info in SOLVERS.items():
        success, exec_time = run_solver(key)
        results.append([info["name"], "PASS" if success else "FAIL", f"{exec_time:.3f} s"])
    
    print("\n" + tabulate(results, headers=["Solver Module", "Validation Status", "Runtime"], tablefmt="github"))

def main():
    parser = argparse.ArgumentParser(description="EE Portfolio Master Orchestration CLI")
    parser.add_argument("--run", choices=["nr", "pv", "bess", "inverter", "all"], help="Run specific solver or all solvers")
    parser.add_argument("--benchmark", action="store_true", help="Execute complete execution benchmark sweep")

    args = parser.parse_args()

    if args.benchmark or args.run == "all":
        run_benchmark()
    elif args.run:
        run_solver(args.run)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
