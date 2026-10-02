# Error Log

| Date | Phase | Error / limitation | Impact | Resolution |
|---|---|---|---|---|
| 2026-10-02 | 0 | GitHub repository was empty when inspected. | No prior project files, cached datasets, or logs were available. | Initialized audit trail on main branch. |
| 2026-10-02 | 1 | Historical option data source not yet validated. | Backtest cannot be run credibly until synchronized option histories are available. | Searching and validating exchange/public datasets; results will be logged here. |

| 2026-10-02 | 1 | First Actions run found zero reconstructable trades. | The backtest did not execute. | Diagnosed pandas DATE/TIMESTAMP comparison in common ATM strike selection; corrected expiry normalization and added data diagnostics. |

| 2026-10-02 | 4 | Successful core run required a post-merge verification because the first documented fix had not actually changed the phase branch. | Results from the earlier run were not used until the corrected commit produced a successful run (37015101390). | Verified the exact phase commit and merged the correction into main via PR #2. |

| 2026-10-02 | 4 | Post-run audit found exit-side execution slippage was omitted and STT/stamp duty were reversed on closing long/short option legs. | The previously published ₹20,850.33 net result was not used as the final result. | Corrected exit execution, exit levies, and GST base; rerunning the core backtest. |

| 2026-10-02 | 4 | Final audit found lot size was applied by trade date rather than by contract expiry, mis-sizing calendar legs during the NIFTY 75→65 transition. | The ₹17,717.27 result is superseded pending the lot-size-corrected rerun. | Engine now sizes each leg from its expiry date; near/far lot sizes are written separately. |
