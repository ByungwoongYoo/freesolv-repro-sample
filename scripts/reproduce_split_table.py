#!/usr/bin/env python3
"""Regenerate the key FreeSolv split-leakage table from public MobleyLab/FreeSolv data.

Pain this pack documents: a random train/test split can make a fingerprint model
look strong, while a scaffold split on the same molecules exposes that the model
does not generalize — and a simple physics baseline (GAFF) beats it.

Usage:
  python scripts/reproduce_split_table.py [path/to/database.txt] [outdir]
Defaults: data/database.txt → expected/
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem import rdFingerprintGenerator
from rdkit.Chem.Scaffolds import MurckoScaffold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

RDLogger.DisableLog("rdApp.*")
SEED = 42
COMMIT = "6c7d19b4b565537365ffd22006aa2cd4643200c6"
EXPECTED_RAW_SHA256 = (
    "2d13f095713bc39b85f85dd7b4e5483fbb12fc694bf253bb1d92a4c4d484f260"
)


def load_freesolv(path: Path) -> pd.DataFrame:
    rows = []
    for line in path.read_text().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        f = [x.strip() for x in line.split(";")]
        rows.append(
            dict(
                compound_id=f[0],
                smiles=f[1],
                name=f[2],
                dG_exp=float(f[3]),
                dG_exp_unc=float(f[4]),
                dG_calc_gaff=float(f[5]),
                dG_calc_unc=float(f[6]),
                exp_ref=f[7],
                calc_ref=f[8],
                notes=f[9] if len(f) > 9 else "",
            )
        )
    return pd.DataFrame(rows)


def scaffold_split(ok: pd.DataFrame, seed: int = SEED) -> list[str]:
    rng = random.Random(seed)
    groups: dict[str, list[int]] = defaultdict(list)
    for i, s in enumerate(ok["scaffold"]):
        groups[s].append(i)
    keys = sorted(groups, key=lambda k: (-len(groups[k]), k))
    big = [k for k in keys if len(groups[k]) > len(ok) * 0.05]
    small = [k for k in keys if k not in big]
    rng.shuffle(small)
    split: dict[int, str] = {}
    n = len(ok)
    tr = va = 0
    for k in big + small:
        idx = groups[k]
        if tr + len(idx) <= 0.8 * n:
            lab = "train"
            tr += len(idx)
        elif va + len(idx) <= 0.1 * n:
            lab = "valid"
            va += len(idx)
        else:
            lab = "test"
        for i in idx:
            split[i] = lab
    return [split[i] for i in range(n)]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    raw = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "data" / "database.txt"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "expected"
    out.mkdir(parents=True, exist_ok=True)

    raw_bytes = raw.read_bytes()
    raw_sha = hashlib.sha256(raw_bytes).hexdigest()
    if raw_sha != EXPECTED_RAW_SHA256:
        print(
            f"WARNING: raw sha256 {raw_sha} != pinned FreeSolv@{COMMIT[:7]} "
            f"({EXPECTED_RAW_SHA256}). Results may differ.",
            file=sys.stderr,
        )

    df = load_freesolv(raw)
    mols = [Chem.MolFromSmiles(s) for s in df["smiles"]]
    df["parse_ok"] = [m is not None for m in mols]
    df["canonical_smiles"] = [Chem.MolToSmiles(m) if m else None for m in mols]
    df["inchikey"] = [Chem.MolToInchiKey(m) if m else None for m in mols]
    df["scaffold"] = [
        MurckoScaffold.MurckoScaffoldSmiles(mol=m) if m else None for m in mols
    ]
    df["dup_inchikey"] = df.duplicated("inchikey", keep=False)
    ok = df[df["parse_ok"]].reset_index(drop=True)

    ok["split_scaffold"] = scaffold_split(ok)
    r = np.random.RandomState(SEED).rand(len(ok))
    ok["split_random"] = np.where(r < 0.8, "train", np.where(r < 0.9, "valid", "test"))

    gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    X = np.array(
        [
            gen.GetFingerprintAsNumPy(Chem.MolFromSmiles(s))
            for s in ok["canonical_smiles"]
        ],
        dtype=np.uint8,
    )
    y = ok["dG_exp"].values

    results: dict = {
        "source": {
            "dataset": "FreeSolv",
            "version": "v0.52",
            "commit": COMMIT,
            "raw_file": str(raw.name),
            "raw_sha256": raw_sha,
        },
        "seed": SEED,
        "n_raw": int(len(df)),
        "n_parsed": int(df["parse_ok"].sum()),
        "n_dup_inchikey_rows": int(df["dup_inchikey"].sum()),
    }

    for sp in ["split_random", "split_scaffold"]:
        trm = (ok[sp] == "train").values
        tem = (ok[sp] == "test").values
        model = RandomForestRegressor(
            n_estimators=500, random_state=SEED, n_jobs=-1
        ).fit(X[trm], y[trm])
        pred = model.predict(X[tem])
        results[sp] = dict(
            model="RF500_morgan2048",
            n_train=int(trm.sum()),
            n_test=int(tem.sum()),
            rmse=float(mean_squared_error(y[tem], pred) ** 0.5),
            r2=float(r2_score(y[tem], pred)),
        )

    gt = (ok["split_scaffold"] == "test").values
    results["gaff_physics_on_scaffold_test"] = dict(
        rmse=float(
            mean_squared_error(y[gt], ok["dG_calc_gaff"].values[gt]) ** 0.5
        ),
        r2=float(r2_score(y[gt], ok["dG_calc_gaff"].values[gt])),
    )

    # Human-readable key table (the "figure" buyers care about)
    table_lines = [
        "| Split | Model | n_test | RMSE (kcal/mol) | R² |",
        "| --- | --- | ---: | ---: | ---: |",
        (
            f"| random 80/10/10 | RF Morgan-2048 | {results['split_random']['n_test']} | "
            f"{results['split_random']['rmse']:.2f} | {results['split_random']['r2']:.3f} |"
        ),
        (
            f"| scaffold 80/10/10 | RF Morgan-2048 | {results['split_scaffold']['n_test']} | "
            f"{results['split_scaffold']['rmse']:.2f} | {results['split_scaffold']['r2']:.3f} |"
        ),
        (
            f"| scaffold test (same 65) | GAFF physics | {results['split_scaffold']['n_test']} | "
            f"{results['gaff_physics_on_scaffold_test']['rmse']:.2f} | "
            f"{results['gaff_physics_on_scaffold_test']['r2']:.3f} |"
        ),
    ]
    table_md = "\n".join(table_lines) + "\n"

    (out / "baseline_results.json").write_text(json.dumps(results, indent=2) + "\n")
    (out / "KEY_TABLE.md").write_text(
        "# FreeSolv split leakage — regenerated table\n\n"
        f"Pinned source: MobleyLab/FreeSolv@{COMMIT[:7]} (`database.txt`).\n\n"
        + table_md
        + "\n**Takeaway:** random-split RMSE looks publishable; scaffold-split RMSE "
        "collapses; physics baseline stays useful. Buyers pay for this check being "
        "pinned, hashed, and re-runnable — not for the raw FreeSolv file itself.\n"
    )

    # Slim cleaned table (no huge fingerprints) for the pack
    slim_cols = [
        "compound_id",
        "name",
        "smiles",
        "canonical_smiles",
        "inchikey",
        "scaffold",
        "dG_exp",
        "dG_exp_unc",
        "dG_calc_gaff",
        "dup_inchikey",
        "split_random",
        "split_scaffold",
    ]
    ok[slim_cols].to_csv(out / "freesolv_cleaned.csv", index=False)

    print(table_md)
    print(json.dumps({k: results[k] for k in ("split_random", "split_scaffold", "gaff_physics_on_scaffold_test")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
