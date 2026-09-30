#!/usr/bin/env bash
# Runs the Go model with configs/default.yaml. Output goes to out/go/.
set -euo pipefail
cd "$(dirname "$0")/.."
go build -C ../pwn -o "$PWD/pwn" .
./pwn configs/default.yaml -o out/go
