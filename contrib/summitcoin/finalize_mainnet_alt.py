#!/usr/bin/env python3
"""Convert the background difficulty-1 miner output into test/functional/data/mainnet_alt.json
and remove the Summitcoin skip from test/functional/mining_mainnet.py.

Usage: contrib/summitcoin/finalize_mainnet_alt.py [/workspace/miner/checkpoint.txt]

checkpoint.txt lines: "<height> <timestamp> <nonce> <blockhash>" (height 1..2016).
Refuses to run until all 2016 blocks are present and contiguous.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
ckpt = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/workspace/miner/checkpoint.txt")
rows = {}
for line in ckpt.read_text().split("\n"):
    p = line.split()
    if len(p) >= 3:
        rows[int(p[0])] = (int(p[1]), int(p[2]))
missing = [h for h in range(1, 2017) if h not in rows]
if missing:
    sys.exit(f"incomplete: {2016 - len(missing)}/2016 blocks mined (first missing height {missing[0]})")
out = ROOT / "test/functional/data/mainnet_alt.json"
data = {"timestamps": [rows[h][0] for h in range(1, 2017)], "nonces": [rows[h][1] for h in range(1, 2017)]}
out.write_text(json.dumps(data, indent=4) + "\n")
print(f"wrote {out}")

test = ROOT / "test/functional/mining_mainnet.py"
src = test.read_text()
new = re.sub(r"\n    def skip_test_if_missing_module\(self\):\n        # TODO\(summitcoin\).*?raise SkipTest\([^\n]*\)\n", "\n", src, flags=re.S)
if new != src:
    test.write_text(new)
    print(f"removed skip from {test} (drop the now-unused SkipTest import if flagged by lint)")
print("next: build/test/functional/mining_mainnet.py, then commit and push")
