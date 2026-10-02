# Research Status

Last updated: 2026-10-02

| Phase | Status | Current result |
|---|---|---|
| 0 — Specification/audit | COMPLETE | Strategy rules, assumptions, research plan and error log initialized. |
| 1 — Data acquisition | COMPLETE / EXTENDED | Historical NIFTY daily option data source identified on Hugging Face; source derives from NSE F&O bhavcopy. NIFTY spot source covers 2021-05 onward, with a 2017-2021 hourly fallback. |
| 2 — Deterministic strategy engine | COMPLETE | Monthly + bi-weekly reconstruction implemented with explicit operational assumptions. |
| 3 — Cost/execution model | COMPLETE / EXTENDED | Entry/exit slippage, brokerage, exchange charges, STT, stamp duty and GST modeled; historical STT schedule added. |
| 4 — Core backtest | COMPLETE / AUDITED | 28 trades in the 2025-09 to 2026-07 sample; final net P&L ₹17,709.28. |
| 5 — Historical extension | IN PROGRESS | Phase branch phase-5-historical-2020-2026; target window 2020-01-01 to 2026-07-28 using cached Hugging Face Parquet inputs. |
| 6 — Robustness/sensitivity | NOT STARTED | Slippage, cost, target, entry-time, breach-confirmation and regime sensitivity. |
| 7 — Walk-forward validation | NOT STARTED | Requires robustness rules to be frozen. |
| 8 — Manuscript | NOT STARTED | Final manuscript after validation phases. |

## Current conclusion
The original deterministic reconstruction is positive in aggregate, but the bootstrap 95% interval for mean trade P&L crosses zero. The monthly and bi-weekly variants diverge materially: monthly is positive while bi-weekly is negative in the tested 2025-09 to 2026-07 sample.

The historical extension is being treated as a new research phase rather than silently replacing the audited result. The phase-5 dataset will be separately hashed and coverage-checked before its results are accepted.

## Next research action
Complete the historical 2020-2026 reconstruction, audit data coverage and lot-size transitions, then compare adjustment outcomes across market regimes. After that, proceed to robustness/sensitivity testing.
