# Data card — FreeSolv Reproducibility Sample Pack

## Summary
Small public chemistry regression set (642 molecules, hydration free energy in kcal/mol) packaged with **pinned origin, hashes, and a one-command rebuild** of the random-vs-scaffold leakage table.

## Motivation
Demonstrate “Ancestry for datasets” (#34): buyers (ML engineers, chem-informatics leads, AI compliance writers) need **where the rows came from** and **whether published scores are honest**, not another unlabeled CSV mirror.

## Composition
| Artifact | Role |
| --- | --- |
| `data/database.txt` | Cached upstream raw (or re-download via `reproduce.sh`) |
| `expected/freesolv_cleaned.csv` | Parsed + IDs + scaffolds + split labels |
| `expected/baseline_results.json` | Machine-readable key metrics |
| `expected/KEY_TABLE.md` | Human-readable table / “figure” |
| `scripts/reproduce_split_table.py` | Regenerator |
| `ORIGIN.md` / `LICENSE.md` / `FAILURES.md` | Provenance & honesty |

## Splits
- `split_random`: per-molecule Bernoulli with seed 42 (≈80/10/10)  
- `split_scaffold`: Murcko-scaffold grouped 80/10/10, seed 42 (large scaffolds assigned first)

## Label
`dG_exp` — experimental hydration free energy (kcal/mol), with `dG_exp_unc`.

## Sensitive / exclusion
No personal data. English SMILES/names only. **No Korean-language annotation corpus.** No North Korea–related content.

## Recommended uses
- Teaching split leakage  
- Baseline for small-molecule property models  
- Portfolio sample for paid “monthly provenance refresh” offers  

## Not recommended
- Clinical decisions  
- Claiming FreeSolv itself is a paid proprietary dataset  

## Maintenance
Sample pack frozen to commit `6c7d19b`. Paid tier (future): re-pin when MobleyLab tags a new release; open issues for hash mismatches.
