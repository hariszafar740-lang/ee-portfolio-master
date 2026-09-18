#!/bin/bash
set -e

USERNAME="hariszafar740-lang"

echo "=========================================================================="
echo "STARTING PORTFOLIO METADATA STANDARDIZATION & GITHUB TOPIC SYNCHRONIZATION"
echo "=========================================================================="

# 1. Newton-Raphson Load Flow Solver
echo "Updating metadata for: power-systems-newton-raphson-solver..."
gh repo edit "$USERNAME/power-systems-newton-raphson-solver" \
  --description "High-performance Python solver for N-bus power system load flow analysis using sparse Jacobian Newton-Raphson numerical methods." \
  --add-topic "power-systems" --add-topic "load-flow" --add-topic "newton-raphson" --add-topic "python" --add-topic "electrical-engineering" --add-topic "pytest"

# 2. Solar PV MPPT & Dynamics Solver
echo "Updating metadata for: solar-pv-mppt-dynamic-solver..."
gh repo edit "$USERNAME/solar-pv-mppt-dynamic-solver" \
  --description "Dynamic solar PV simulation suite with dynamic irradiance modeling, perturb-and-observe MPPT control, and IV/PV characteristic curve engines." \
  --add-topic "photovoltaics" --add-topic "mppt" --add-topic "solar-energy" --add-topic "renewable-energy" --add-topic "python" --add-topic "control-systems"

# 3. 1RC BESS ECM Solver
echo "Updating metadata for: bess-soc-dynamics-solver..."
gh repo edit "$USERNAME/bess-soc-dynamics-solver" \
  --description "Electro-thermal 1RC equivalent circuit model solver for Battery Energy Storage Systems featuring dynamic SoC Coulomb counting and transient thermal kinetics." \
  --add-topic "bess" --add-topic "battery-management" --add-topic "electro-thermal" --add-topic "energy-storage" --add-topic "python" --add-topic "simulation"

# 4. Grid-Forming Inverter Control Solver
echo "Updating metadata for: inverter-grid-control-solver..."
gh repo edit "$USERNAME/inverter-grid-control-solver" \
  --description "Grid-forming inverter simulation engine featuring P-w/Q-V droop control, LPF measurement loops, VSG virtual inertia, virtual impedance, and FRT compliance benchmarks." \
  --add-topic "grid-forming" --add-topic "inverter-control" --add-topic "virtual-inertia" --add-topic "microgrid" --add-topic "power-electronics" --add-topic "fault-ride-through"

echo "=========================================================================="
echo "PORTFOLIO METADATA SYNCHRONIZATION COMPLETE"
echo "=========================================================================="
