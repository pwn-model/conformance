#!/usr/bin/env bash
# Runs the Julia model with configs/default.yaml. Output goes to out/julia/.
set -euo pipefail
cd "$(dirname "$0")/.."
julia --project=../PWNModel.jl -e 'using PWNModel; run_model("configs/default.yaml"; out_dir="out/julia")'
