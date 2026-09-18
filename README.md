# Multi-Project Power Systems & Energy Storage Simulation Portfolio

A suite of production-grade Python solvers for power systems engineering, renewable integration, battery energy storage modeling, and microgrid inverter dynamic control. Developed in Kali Linux with `pytest` unit test suites, modular architecture, and GitHub Actions CI pipelines.

---

## Portfolio Repositories

### 1. [Power Systems Newton-Raphson Solver](https://github.com/hariszafar740-lang/power-systems-newton-raphson-solver)
* **Domain:** Power Distribution & Transmission Grid Analysis
* **Core Capabilities:** N-bus admittance matrix ($Y_{bus}$) formulation, sparse Jacobian construction, power mismatch convergence, line flow loss analysis.
* **Stack:** Python 3, `numpy`, `pytest`, GitHub Actions CI.

### 2. [Solar PV MPPT Dynamic Solver](https://github.com/hariszafar740-lang/solar-pv-mppt-dynamic-solver)
* **Domain:** Photovoltaic Systems & Dynamic Resource Modeling
* **Core Capabilities:** Single-diode PV cell modeling, dynamic irradiance/temperature profiles, Perturb & Observe ($P\&O$) MPPT tracking, $I-V$ and $P-V$ visualization.
* **Stack:** Python 3, `numpy`, `matplotlib`, `pytest`.

### 3. [BESS SoC Dynamics Solver](https://github.com/hariszafar740-lang/bess-soc-dynamics-solver)
* **Domain:** Battery Energy Storage Systems & Electro-Thermal Modeling
* **Core Capabilities:** 1RC Equivalent Circuit Model dynamics, State of Charge ($\text{SoC}$) Coulomb counting, temperature-dependent internal resistance, dynamic drive cycle stress testing.
* **Stack:** Python 3, `numpy`, `matplotlib`, `pytest`.

### 4. [Grid-Forming Inverter Control Solver](https://github.com/hariszafar740-lang/inverter-grid-control-solver)
* **Domain:** Microgrid Power Electronics & Grid Stability
* **Core Capabilities:** $P-\omega$ and $Q-V$ droop control loops, 1st-order LPF power filtering, Virtual Synchronous Generator ($\text{VSG}$) virtual inertia, virtual impedance loops, and Fault Ride-Through ($\text{FRT}$) compliance benchmarking.
* **Stack:** Python 3, `numpy`, `matplotlib`, `pytest`, GitHub Actions CI.

---

## Verification & Test Execution Across Portfolio

To execute unit tests across all repositories in one automated sweep:

```bash
cd ~/ee_portfolio
for dir in */; do
  if [ -d "$dir/tests" ]; then
    echo "=========================================="
    echo "Testing $dir..."
    echo "=========================================="
    (cd "$dir" && source *_env/bin/activate 2>/dev/null || true && PYTHONPATH=. pytest tests/)
  fi
done
