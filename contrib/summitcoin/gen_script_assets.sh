#!/usr/bin/env bash
# Generate script_assets_test.json locally (unminimized) per src/test/fuzz/script_assets_test_minimizer.cpp
# and run script_assets_tests against it. Usage: contrib/summitcoin/gen_script_assets.sh [build_dir] [out_dir] [runs]
set -euo pipefail
BUILD=${1:-build}; OUT=${2:-/tmp/unit_test_data}; RUNS=${3:-2}
DUMP=$(mktemp -d); mkdir -p "$OUT"
for N in $(seq 1 "$RUNS"); do TEST_DUMP_DIR="$DUMP" "$BUILD/test/functional/feature_taproot.py" --dumptests; done
( echo '['; find "$DUMP" -type f -exec cat {} + | head -c -2; echo; echo ']' ) > "$OUT/script_assets_test.json"
rm -rf "$DUMP"
DIR_UNIT_TEST_DATA="$OUT" "$BUILD/bin/test_summitcoin" --run_test=script_assets_tests
