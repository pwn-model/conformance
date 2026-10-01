# Model conformance tests

[![Conformance](https://github.com/pwn-model/conformance/actions/workflows/conformance.yml/badge.svg)](https://github.com/pwn-model/conformance/actions/workflows/conformance.yml)

Tests for conformance between the two PWN model implementations,
[pwn](https://github.com/pwn-model/pwn) (Go) and
[PWNModel.jl](https://github.com/pwn-model/PWNModel.jl) (Julia).

Both implementations run the same headless config
([`configs/default.yaml`](https://github.com/pwn-model/conformance/blob/main/configs/default.yaml)),
and their CSV output must be identical.

## Running locally

With `pwn/` and `PWNModel.jl/` checked out next to this repository:

```sh
scripts/run_go.sh      # runs the Go model with configs/default.yaml     -> out/go/
scripts/run_julia.sh   # runs the Julia model with configs/default.yaml  -> out/julia/
scripts/compare.py     # compares the outputs as numbers, non-zero exit on mismatch
```

## CI

The workflow [conformance.yml](.github/workflows/conformance.yml) is triggered manually
(Actions → Conformance → Run workflow), with the refs of both model repositories as inputs.
Model outputs are uploaded as a workflow artifact.
