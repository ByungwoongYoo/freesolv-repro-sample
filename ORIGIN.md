# ORIGIN — FreeSolv provenance pin

| Field | Value |
| --- | --- |
| Dataset | FreeSolv (hydration free energies) |
| Version | v0.52 (header date 2017-06-11) |
| Canonical repo | https://github.com/MobleyLab/FreeSolv |
| Pinned commit | `6c7d19b4b565537365ffd22006aa2cd4643200c6` |
| Raw file | `database.txt` (semicolon-delimited) |
| Direct URL | https://raw.githubusercontent.com/MobleyLab/FreeSolv/6c7d19b4b565537365ffd22006aa2cd4643200c6/database.txt |
| Raw SHA-256 | `2d13f095713bc39b85f85dd7b4e5483fbb12fc694bf253bb1d92a4c4d484f260` |
| License | CC BY 4.0 |
| Rows (data lines) | 642 molecules |
| Language | English chemistry identifiers (SMILES / IUPAC-style names) — **not** a Korean-language corpus |

## Why this pin exists
Public ML tutorials often cite “FreeSolv” without commit, split recipe, or seed. Scores then drift across forks. This pack freezes **URL + commit + hash + seed + split algorithm** so the key table can be regenerated bit-for-bit (within RF float noise tolerance on displayed decimals).

## What we add (derived)
1. RDKit parse + canonical SMILES + InChIKey + Murcko scaffold  
2. Duplicate InChIKey flag  
3. Random and scaffold splits (80/10/10, seed 42)  
4. Random-forest Morgan baseline vs GAFF physics on the same scaffold test set  

Experimental ΔG values are **not altered**.
