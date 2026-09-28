#!/usr/bin/env python3
"""
Automated System Topology & Architectural Flowchart Generator
Author: Haris Zafar
"""

from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
README_FILE = ROOT_DIR / "README.md"

MERMAID_DIAGRAM = '''```mermaid
graph TD
    subgraph Microgrid & Power Grid Simulation Infrastructure
        PV["☀️ Solar PV Dynamic MPPT Solver<br/><i>Single-Diode Dynamics & P&O Loop</i>"]
        BESS["🔋 BESS SoC Dynamics ECM Solver<br/><i>1RC Electro-Thermal ECM & Coulomb Counting</i>"]
        GFM["🌐 Grid-Forming Inverter Control Solver<br/><i>P-ω / Q-V Droop & VSG Inertia Control</i>"]
        NR["⚡ Power Systems Newton-Raphson Solver<br/><i>N-Bus Ybus Formulation & Mismatch Convergence</i>"]

        PV -->|DC Power Output| BESS
        BESS -->|DC Bus Voltage| GFM
        GFM -->|AC Injection & Voltage/Freq Reference| NR
    end

    subgraph Portfolio Orchestration & Quality Control Gate
        CLI["🚀 portfolio_cli.py<br/><i>Master Runner & Benchmark Suite</i>"]
        PROF["⏱️ profile_portfolio.py<br/><i>cProfile Diagnostic Engine</i>"]
        AUDIT["🛡️ audit_portfolio.py<br/><i>Bandit Security AST Scanner</i>"]
        BUILD["📦 build_release.py<br/><i>Tarball Bundler & SHA-256 Hasher</i>"]
        DASH["📊 generate_portfolio_report.py<br/><i>Executive HTML Exporter</i>"]

        CLI --> PROF
        CLI --> AUDIT
        CLI --> BUILD
        CLI --> DASH
    end
```'''

def inject_architecture_docs():
    print("Generating portfolio system topology flowchart...")
    
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if "## System Architecture & Physical Flowchart" in content:
        print("System architecture documentation is already embedded in README.md.")
        return

    architecture_section = f"\n## System Architecture & Physical Flowchart\n{MERMAID_DIAGRAM}\n"
    
    with open(README_FILE, "a", encoding="utf-8") as f:
        f.write(architecture_section)

    print(f"System architecture diagram successfully appended to: {README_FILE}")

if __name__ == "__main__":
    print("==========================================================================")
    print(" GENERATING SYSTEM TOPOLOGY & ARCHITECTURAL DOCUMENTATION")
    print("==========================================================================")
    inject_architecture_docs()
