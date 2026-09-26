# Multi-Project Power Systems & Energy Storage Simulation Portfolio

[![Portfolio Matrix CI](https://github.com/hariszafar740-lang/ee-portfolio-master/actions/workflows/portfolio_matrix_ci.yml/badge.svg)](https://github.com/hariszafar740-lang/ee-portfolio-master/actions/workflows/portfolio_matrix_ci.yml)

A suite of production-grade Python solvers for power systems engineering, renewable integration, battery energy storage modeling, and microgrid inverter dynamic control. Developed in Kali Linux with `pytest` unit test suites, modular architecture, and GitHub Actions CI pipelines.

---

## Portfolio Repositories & Live Build Status

| Repository | CI Status | Domain | Stack |
| :--- | :--- | :--- | :--- |
| ⚡ **[Power Systems Newton-Raphson Solver](https://github.com/hariszafar740-lang/power-systems-newton-raphson-solver)** | ![CI](https://github.com/hariszafar740-lang/power-systems-newton-raphson-solver/actions/workflows/ci.yml/badge.svg) | Load Flow & Grid Analysis | Python, NumPy, pytest |
| ☀️ **[Solar PV Dynamic MPPT Solver](https://github.com/hariszafar740-lang/solar-pv-mppt-dynamic-solver)** | ![CI](https://github.com/hariszafar740-lang/solar-pv-mppt-dynamic-solver/actions/workflows/ci.yml/badge.svg) | Photovoltaics & Control | Python, NumPy, Matplotlib |
| 🔋 **[BESS SoC Dynamics Solver](https://github.com/hariszafar740-lang/bess-soc-dynamics-solver)** | ![CI](https://github.com/hariszafar740-lang/bess-soc-dynamics-solver/actions/workflows/ci.yml/badge.svg) | Energy Storage & Thermal | Python, NumPy, Matplotlib |
| 🌐 **[Grid-Forming Inverter Control Solver](https://github.com/hariszafar740-lang/inverter-grid-control-solver)** | ![CI](https://github.com/hariszafar740-lang/inverter-grid-control-solver/actions/workflows/ci.yml/badge.svg) | Microgrids & Power Electronics | Python, NumPy, pytest |

---

## Verification & Test Execution Across Portfolio

To execute unit tests across all repositories locally:
bash
cd ~/ee_portfolio
for dir in */; do
if [ -d "$dir/tests" ]; then
echo ""
echo "Testing $dir..."
echo ""
(cd "$dir" && source *_env/bin/activate 2>/dev/null || true && PYTHONPATH=. pytest tests/)
fi
done

## Unified CLI Orchestration

Run all engineering simulation modules directly via `portfolio_cli.py`:
bash
# Run full portfolio test benchmark
python3 portfolio_cli.py --benchmark

## Automated Performance Profiling & Diagnostics

Analyze algorithm bottleneck execution times and total function calls across all solver test suites:

```bash
python3 profile_portfolio.py
