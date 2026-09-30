#!/usr/bin/env bash
# Compares Go and Julia output. Fails on any difference.
set -euo pipefail
cd "$(dirname "$0")/.."
diff -r out/go out/julia
