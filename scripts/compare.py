#!/usr/bin/env python3
"""Compares Go and Julia CSV output. Fails on any difference.

Values are compared as numbers, not as strings, as the two implementations
format them differently (e.g. Go `65138` vs Julia `65138.0`).
Numbers must be exactly equal, as both implementations are bit-identical.

Usage: scripts/compare.py [go_dir] [julia_dir]   (default: out/go out/julia)
"""

import csv
import math
import sys
from pathlib import Path

MAX_REPORTED = 10


def main():
    root = Path(__file__).resolve().parent.parent
    go_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "out" / "go"
    julia_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "out" / "julia"

    go_files = csv_files(go_dir)
    julia_files = csv_files(julia_dir)

    ok = True
    if not go_files:
        print(f"FAIL no CSV files in {go_dir}")
        ok = False
    for f in sorted(go_files - julia_files):
        print(f"FAIL {f}: only in {go_dir}")
        ok = False
    for f in sorted(julia_files - go_files):
        print(f"FAIL {f}: only in {julia_dir}")
        ok = False

    for f in sorted(go_files & julia_files):
        errors = compare_file(go_dir / f, julia_dir / f)
        if errors:
            ok = False
            print(f"FAIL {f}")
            for e in errors[:MAX_REPORTED]:
                print(f"     {e}")
            if len(errors) > MAX_REPORTED:
                print(f"     ... and {len(errors) - MAX_REPORTED} more")
        else:
            print(f"OK   {f}")

    sys.exit(0 if ok else 1)


def csv_files(directory):
    """Returns the paths of all CSV files in directory, relative to it."""
    return {p.relative_to(directory) for p in directory.rglob("*.csv")}


def compare_file(go_file, julia_file):
    """Returns a list of differences between the two CSV files."""
    go_rows = read_csv(go_file)
    julia_rows = read_csv(julia_file)

    if not go_rows or not julia_rows:
        return ["empty file"]
    header = go_rows[0]
    if header != julia_rows[0]:
        return [f"headers differ: go {go_rows[0]}, julia {julia_rows[0]}"]

    errors = []
    if len(go_rows) != len(julia_rows):
        errors.append(f"row counts differ: go {len(go_rows) - 1}, julia {len(julia_rows) - 1}")

    for line, (go_row, julia_row) in enumerate(zip(go_rows[1:], julia_rows[1:]), start=2):
        if len(go_row) != len(header) or len(julia_row) != len(header):
            errors.append(f"line {line}: column counts differ from header")
            continue
        for col, go_val, julia_val in zip(header, go_row, julia_row):
            if not equal(go_val, julia_val):
                errors.append(f"line {line} (t={go_row[0]}), {col}: go {go_val}, julia {julia_val}")

    return errors


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.reader(f))


def equal(a, b):
    """Compares two CSV values as numbers, treating NaN as equal to NaN."""
    try:
        x, y = float(a), float(b)
    except ValueError:
        return a == b
    return x == y or (math.isnan(x) and math.isnan(y))


if __name__ == "__main__":
    main()
