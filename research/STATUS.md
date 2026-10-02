# Research Status

Last updated: 2026-10-02

| Phase | Status | Current result |
|---|---|---|
| 0 — Specification/audit | COMPLETE | Strategy rules, assumptions, research plan and error log initialized. |
| 1 — Data acquisition | COMPLETE | Public third-party daily NIFTY option cache validated; SHA-256 recorded. |
| 2 — Deterministic strategy engine | COMPLETE | Monthly + bi-weekly reconstruction implemented with explicit operational assumptions. |
| 3 — Cost/execution model | COMPLETE / CORRECTED | Entry and exit slippage plus STT/stamp direction audited; corrected run completed. |
| 4 — Core backtest | COMPLETE / CORRECTED | 29 trades; corrected net P&L ₹17,717.27; monthly ₹25,958.85; bi-weekly -₹8,241.58. |
| 5 — Robustness/sensitivity | NEXT | Slippage, cost, target, entry-time, breach-confirmation and regime sensitivity. |
| 6 — Walk-forward validation | NOT STARTED | Requires robustness rules to be frozen. |
| 7 — Manuscript | NOT STARTED | Final manuscript after validation phases. |

## Current conclusion
The corrected deterministic reconstruction is positive in aggregate, but the monthly and bi-weekly variants behave very differently: monthly is positive while bi-weekly is negative in the sample. The bootstrap interval for mean trade P&L crosses zero, so the core run is evidence for further testing rather than a statistically decisive edge.

The first published core numbers were superseded after a post-run audit found an exit-cost-model error. The corrected run is the only result to use.

## Next research action
Run robustness/sensitivity analysis and regime segmentation before any final strategy conclusion.
