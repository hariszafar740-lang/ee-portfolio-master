#!/usr/bin/env python3
"""
Automated Performance Profiling & Diagnostics Engine
Author: Haris Zafar
"""

import pstats
import subprocess
import time
from pathlib import Path
from tabulate import tabulate

ROOT_DIR = Path(__file__).parent.resolve()

SOLVERS = [
    ("Power Systems Newton-Raphson Solver", "power-systems-newton-raphson-solver"),
    ("Solar PV Dynamic MPPT Solver", "solar-pv-mppt-dynamic-solver"),
    ("BESS 1RC Electro-Thermal ECM Solver", "bess-soc-dynamics-solver"),
    ("Grid-Forming Inverter Control Solver", "inverter-grid-control-solver")
]

def profile_solver(name, folder):
    solver_dir = ROOT_DIR / folder
    prof_file = solver_dir / "profile.prof"
    
    cmd = (
        f"cd {solver_dir} && "
        f"source *_env/bin/activate 2>/dev/null || true && "
        f"PYTHONPATH=. python3 -m cProfile -o profile.prof -m pytest tests/ > /dev/null 2>&1"
    )
    
    start_time = time.perf_counter()
    res = subprocess.run(cmd, shell=True, executable="/bin/bash")
    end_time = time.perf_counter()
    
    elapsed_ms = (end_time - start_time) * 1000.0
    
    num_calls = "N/A"
    if prof_file.exists():
        try:
            stats = pstats.Stats(str(prof_file))
            num_calls = f"{stats.total_calls:,}"
            prof_file.unlink() # Clean up temporary profile binary
        except Exception:
            pass
            
    status = "PASS" if res.returncode == 0 else "FAIL"
    return [name, status, f"{elapsed_ms:.2f} ms", num_calls]

def main():
    print("==========================================================================")
    print(" STARTING AUTOMATED PERFORMANCE PROFILING & DIAGNOSTICS SWEEP")
    print("==========================================================================")
    
    results = []
    for name, folder in SOLVERS:
        print(f"Profiling execution metrics for: {name}...")
        results.append(profile_solver(name, folder))
        
    print("\n" + tabulate(results, headers=["Solver Module", "Status", "Latency (ms)", "Total Function Calls"], tablefmt="github"))
    print("\nProfiling sweep successfully completed.")

if __name__ == "__main__":
    main()
