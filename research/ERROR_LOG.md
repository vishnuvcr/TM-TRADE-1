# Error Log

| Date | Phase | Error / limitation | Impact | Resolution |
|---|---|---|---|---|
| 2026-10-02 | 0 | GitHub repository was empty when inspected. | No prior project files, cached datasets, or logs were available. | Initialized audit trail on main branch. |
| 2026-10-02 | 1 | Historical option data source not yet validated. | Backtest cannot be run credibly until synchronized option histories are available. | Searched exchange/public/open datasets and selected a cached Hugging Face daily source derived from NSE F&O bhavcopy. |
| 2026-10-02 | 1 | First Actions run found zero reconstructable trades. | The backtest did not execute. | Diagnosed pandas DATE/TIMESTAMP comparison in common ATM strike selection; corrected expiry normalization and added diagnostics. |
| 2026-10-02 | 4 | Successful core run required post-merge verification. | Earlier results were not used until the corrected commit produced a successful run. | Verified the exact phase commit and merged the correction into main. |
| 2026-10-02 | 4 | Exit-side execution slippage was omitted and STT/stamp duty were reversed on closing legs. | Earlier published net result was superseded. | Corrected exit execution, levies and GST base. |
| 2026-10-02 | 4 | Lot size was applied by trade date rather than contract expiry. | The pre-correction result was superseded. | Engine now sizes each leg from expiry date. |
| 2026-10-02 | 5 | Historical dataset initially had a coverage-validation SQL alias error. | The first historical run stopped before backtesting. | Replaced reserved alias `rows` with `row_count`; dataset build itself was retained and hashed. |
| 2026-10-02 | 5 | Historical lot-size constants were initially written with literal newline escape characters. | The historical engine failed before calculating trades. | Corrected the constants and reran. |
| 2026-10-02 | 5 | Final summary still referenced superseded STT variable names after the historical calculation had completed. | The calculation completed but the job failed while writing summary output. | Corrected summary field references and reran successfully. |
| 2026-10-02 | 5 | Historical spot coverage ends 2026-07-02 although the requested window ends 2026-07-28. | No valid claim can be made for the uncovered tail. | Reported actual spot coverage and latest reconstructed trade exit explicitly; no synthetic extension used. |
| 2026-10-02 | 5 | Third-party transformed data may contain coverage or transformation differences from raw NSE files. | Historical results require independent source validation. | Added provenance, hashes and a requirement for selected-trade cross-checks in the next phase. |
