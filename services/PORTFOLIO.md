# Portfolio — English dataset cleanup (async)

**One line:** I turn messy English CSV/JSON tables into a clean file + one-page data card (schema, nulls/dups, license note, SHA-256) — email-only delivery, no calls.

---

## Problem
Public and internal tables arrive as odd delimiters, comment headers, uncanonical identifiers, and **no documented train/test recipe**. A junior `train_test_split` then produces a number that looks publishable and is not.

## What you get
1. Cleaned CSV/JSON (schema normalized, parse flags, duplicate IDs called out)  
2. One-page **data card** (columns, counts, license/provenance note, hashes)  
3. Optional **split audit** when the task is ML (random vs group/scaffold — same style as the FreeSolv sample)  
4. Delivery as zip or GitHub PR within the agreed window · **email / async chat only — no Zoom, no phone**

**Scope language:** English corpora and English-schema tables only. **No Korean-language annotation or data gigs.**

---

## Proof on public FreeSolv (same pack as the #34 sample)

**Source:** MobleyLab/FreeSolv v0.52, commit `6c7d19b`, CC BY 4.0  
**Raw pin:** SHA-256 `2d13f095713bc39b85f85dd7b4e5483fbb12fc694bf253bb1d92a4c4d484f260` (642 rows)

| | Before | After |
| --- | --- | --- |
| Format | `;` text + `#` comments, long notes | `freesolv_cleaned.csv` (12 ML-ready columns) |
| IDs | SMILES only | + canonical SMILES, InChIKey, Murcko scaffold, `dup_inchikey` |
| Splits | none | `split_random` + `split_scaffold` (seed 42) |
| Audit | easy to overfit a random split | RF Morgan RMSE **1.82** (random) vs **4.95** (scaffold); GAFF physics **1.97** on the same 65 scaffold-test molecules |

Example label flip: `mobley_1034539` is **train** under random and **test** under scaffold — 231 / 642 rows change label between the two recipes.

Same public FreeSolv; **we sell the cleanup + audit, not the molecules.**

Full before/after write-up: `BEFORE_AFTER.md` in this folder (paths under `/workspace/greg-pack-2026-10-24/`).

---

## How to hire (when live)
Fixed-price tiers in `PRICING_DRAFT.md` (Director approval required before listing). Reply by email with file size, schema headache, and deadline.
