# FreeSolv Reproducibility Sample Pack

**Product thesis:** Ancestry for datasets — pin origin, license, hashes, and a script that regenerates the table people actually quote.

**Dataset:** [FreeSolv](https://github.com/MobleyLab/FreeSolv) v0.52 (642 small molecules, hydration free energy).  
**Why buyers care:** Random train/test splits make fingerprint models look strong (~1.8 kcal/mol RMSE); a scaffold split on the **same** public data exposes the gap (~4.95), while a physics baseline (GAFF) stays ~1.97. Most free CSVs online do not pin commit + seed + split recipe.

This folder is a **free sample** (GitHub). Paid cleanup / split-audit services are listed under `services/`.

---

## What / why / how

### What
- Provenance pin (`ORIGIN.md`)
- License honesty (`LICENSE.md`)
- Known failure modes (`FAILURES.md`)
- Data card (`DATA_CARD.md`)
- One script that rebuilds the key table from public data
- Checksums for every file in the pack

### Why
Public ML work cites FreeSolv without a commit hash or scaffold audit. This pack makes the optimistic-vs-honest split comparison **re-runnable in one command**.

### How to reproduce
```bash
# optional clean venv
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# downloads database.txt if missing, verifies SHA-256, writes expected/
./reproduce.sh
```

Or manually:
```bash
python scripts/reproduce_split_table.py data/database.txt expected/
```

You should get a table like:

| Split | Model | n_test | RMSE (kcal/mol) | R² |
| --- | --- | ---: | ---: | ---: |
| random 80/10/10 | RF Morgan-2048 | 69 | 1.82 | 0.686 |
| scaffold 80/10/10 | RF Morgan-2048 | 65 | 4.95 | 0.045 |
| scaffold test (same 65) | GAFF physics | 65 | 1.97 | 0.849 |

Full numbers: `expected/baseline_results.json`. Cleaned columns: `expected/freesolv_cleaned.csv`.

Prefer fetching upstream yourself? Use the URL in `ORIGIN.md` — the script checks the pinned SHA-256 either way.

---

## Layout
```
SAMPLE_PACK/
  README.md
  ORIGIN.md
  DATA_CARD.md
  FAILURES.md
  LICENSE.md
  CHECKSUMS.sha256
  requirements.txt
  reproduce.sh
  scripts/reproduce_split_table.py
  data/database.txt          # small cache of upstream; re-downloadable
  expected/KEY_TABLE.md
  expected/baseline_results.json
  expected/freesolv_cleaned.csv
```

## Cite
Mobley & Guthrie (2014); Duarte Ramos Matos et al. (2017); MobleyLab/FreeSolv CC BY 4.0. See `LICENSE.md`.

## Status
Free sample pack — public. Paid add-ons (USD, fixed price):

| Offer | Price | Turnaround |
| --- | ---: | --- |
| Clean + data card | $150 | 48 hours |
| + Split audit | $280 | 72 hours |
| Pack refresh | $400 | 5 business days |

See `services/PRICING.md` and `services/PORTFOLIO.md`. Waitlist copy: `WAITLIST.md`.
