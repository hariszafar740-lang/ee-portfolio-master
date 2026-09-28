#!/bin/bash
set -e

HOOK_PATH=".git/hooks/pre-commit"

echo "Installing Git pre-commit quality gate..."

cat << 'HOOK_EOF' > "$HOOK_PATH"
#!/bin/bash
echo "=========================================================================="
echo " RUNNING PRE-COMMIT QUALITY GATES & BENCHMARK AUDIT"
echo "=========================================================================="

source master_env/bin/activate 2>/dev/null || true

# 1. Run unit test benchmark across all solvers
python3 portfolio_cli.py --benchmark
if [ $? -ne 0 ]; then
    echo "❌ Pre-commit failed: One or more unit tests failed across the portfolio."
    exit 1
fi

# 2. Run AST static security audit
python3 audit_portfolio.py
if [ $? -ne 0 ]; then
    echo "❌ Pre-commit failed: Security audit or syntax checks failed."
    exit 1
fi

echo "✅ Pre-commit quality gates passed successfully!"
HOOK_EOF

chmod +x "$HOOK_PATH"
echo "Git pre-commit hook successfully installed at: $HOOK_PATH"
