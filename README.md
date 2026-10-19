# Model conformance tests

[![Conformance](https://github.com/pwn-model/conformance/actions/workflows/conformance.yml/badge.svg)](https://github.com/pwn-model/conformance/actions/workflows/conformance.yml)

Tests for conformance between the two PWN model implementations,
[pwn](https://github.com/pwn-model/pwn) (Go) and
[PWNModel.jl](https://github.com/pwn-model/PWNModel.jl) (Julia).

Both implementations run the same headless config, and their CSV output must be identical.
That config is generated from the documented model parameters
([`model-spec/parameters.yaml`](https://github.com/pwn-model/model-spec/blob/main/parameters.yaml)),
merged with [`configs/base.yaml`](https://github.com/pwn-model/conformance/blob/main/configs/base.yaml),
which holds what is not a model parameter (seed, reporters).
As both models reject unknown and missing parameters, running them with it also checks
that the documented parameters are exactly those the models take.

Further, the documented parameters themselves are checked,
as well as that the default configs shipped with both models match them.

## Running locally

With `model-spec/`, `pwn/` and `PWNModel.jl/` checked out next to this repository:

```sh
python scripts/check_params.py      # checks parameters.yaml, and the models' config.yaml files against it
python scripts/params_to_config.py  # generates the config from parameters.yaml  -> out/default.yaml
scripts/run_go.sh                   # runs the Go model with out/default.yaml     -> out/go/
scripts/run_julia.sh                # runs the Julia model with out/default.yaml  -> out/julia/
python scripts/compare.py           # compares the outputs as numbers, non-zero exit on mismatch
```

The run scripts optionally take another config file as argument.
The Python scripts require [PyYAML](https://pypi.org/project/PyYAML/) (except `compare.py`).

## CI

The workflow [conformance.yml](.github/workflows/conformance.yml) is triggered manually
(Actions → Conformance → Run workflow), with the refs of both model repositories as inputs.
Model outputs are uploaded as a workflow artifact.
