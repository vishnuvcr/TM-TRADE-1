# Error Log

| Date | Phase | Error / limitation | Impact | Resolution |
|---|---|---|---|---|
| 2026-10-02 | 0 | GitHub repository was empty when inspected. | No prior project files, cached datasets, or logs were available. | Initialized audit trail on main branch. |
| 2026-10-02 | 1 | Historical option data source not yet validated. | Backtest cannot be run credibly until synchronized option histories are available. | Searching and validating exchange/public datasets; results will be logged here. |
| 2026-10-02 | 1 | First Actions run found zero reconstructable trades. | The backtest did not execute. | Diagnosed pandas DATE/TIMESTAMP comparison in common ATM strike selection; corrected expiry normalization and added data diagnostics. |
| 2026-10-02 | 4 | Successful core run required a post-merge verification because the first documented fix had not actually changed the phase branch. | Earlier results were not used until the corrected commit produced a successful run. | Verified the exact phase commit and merged the correction into main. |
| 2026-10-02 | 4 | Post-run audit found exit-side execution slippage was omitted and STT/stamp duty were reversed on closing long/short option legs. | Earlier published net result was superseded. | Corrected exit execution, exit levies and GST base. |
| 2026-10-02 | 4 | Lot size was applied by trade date rather than by contract expiry. | The ₹17,717.27 pre-correction result was superseded. | Engine now sizes each leg from its expiry date. |
| 2026-10-02 | 5 | The original public DuckDB cache begins in 2025, so it cannot answer the 2021+ question. | A longer-period result cannot be inferred from the original cache. | Added a dedicated historical-data phase using yearly Hugging Face Parquet files derived from NSE F&O bhavcopy data. |
| 2026-10-02 | 5 | Historical lot sizes changed more than once during 2020-2026. | Applying one lot size would materially distort older P&L. | Added expiry-date schedule: 50, then 25, then 75, then 65; exact contract-generation transitions remain an audit item. |
| 2026-10-02 | 5 | Historical STT rates changed during the study window. | Using the 2026 rate throughout would overstate older costs. | Added date-based STT schedule: 0.05% pre-Apr-2023, 0.0625% Apr-2023 to Sep-2024, 0.10% Oct-2024 to Mar-2026, 0.15% from Apr-2026. |
| 2026-10-02 | 5 | HF historical daily option files are third-party datasets and may contain coverage gaps/transformations. | Results require source validation and cannot automatically be treated as exchange-authoritative. | Coverage verification and selected-trade cross-checks are required before final acceptance. |
