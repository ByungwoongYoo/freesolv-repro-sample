# FAILURES — known reproducibility pains (FreeSolv)

These are the reasons a buyer cares about a provenance/reproducibility pack.

## 1. Random-split optimism (documented here)
Fingerprint models trained with a **random** 80/10/10 split can report ~**1.8 kcal/mol** RMSE.  
The **same** model and molecules with a **scaffold** split jump to ~**4.95 kcal/mol** RMSE, while the GAFF physics column on that test set stays ~**1.97**.  
If a paper or blog only shows the random split, the “ML win” is partly **leakage / near-neighbor memorization**, not generalization.

## 2. Unpinned “FreeSolv” citations
Many notebooks say `FreeSolv` without commit or `database.txt` hash. Molecule lists and notes fields have changed across versions → silent score drift.

## 3. Missing rebuild code
Some “cleaned FreeSolv CSVs” on the internet ship features but not the script that made the splits. Without the scaffold grouping rule and seed, you cannot audit the test set.

## 4. Out of scope for this sample (honest gaps)
- Full conformal / uncertainty calibration  
- 3D conformer ensembles  
- Cross-lab experimental meta-analysis  
- EU AI Act training-content legal opinion (we only pin **technical** provenance)

If regenerate fails on your machine, check: RDKit version major, `requirements.txt`, and that `database.txt` SHA-256 matches `ORIGIN.md`.
