# FreeSolv split leakage — regenerated table

Pinned source: MobleyLab/FreeSolv@6c7d19b (`database.txt`).

| Split | Model | n_test | RMSE (kcal/mol) | R² |
| --- | --- | ---: | ---: | ---: |
| random 80/10/10 | RF Morgan-2048 | 69 | 1.82 | 0.686 |
| scaffold 80/10/10 | RF Morgan-2048 | 65 | 4.95 | 0.045 |
| scaffold test (same 65) | GAFF physics | 65 | 1.97 | 0.849 |

**Takeaway:** random-split RMSE looks publishable; scaffold-split RMSE collapses; physics baseline stays useful. Buyers pay for this check being pinned, hashed, and re-runnable — not for the raw FreeSolv file itself.
