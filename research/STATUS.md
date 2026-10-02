# Research Status

Last updated: 2026-10-02

| Phase | Status | Current result |
|---|---|---|
| 0 — Specification/audit | COMPLETE | Strategy rules, assumptions, research plan and error log initialized. |
| 1 — Data acquisition | COMPLETE / EXTENDED | Historical NIFTY daily option data acquired through a cached Hugging Face pipeline; coverage and hashes recorded. |
| 2 — Deterministic strategy engine | COMPLETE | Monthly + bi-weekly reconstruction implemented with explicit operational assumptions. |
| 3 — Cost/execution model | COMPLETE / EXTENDED | Entry/exit slippage, brokerage, exchange charges, historical STT, stamp duty and GST modeled. |
| 4 — Core backtest | COMPLETE / AUDITED | 28 trades in 2025-09 to 2026-07; net P&L ₹17,709.28. |
| 5 — Historical extension | COMPLETE / AUDITED | 264 reconstructed segments over 2020-2026 requested window; net P&L ₹11,71,475.36. Adjustment exits: 39/39 losses, total -₹42,149.70. |
| 6 — Robustness/sensitivity | COMPLETE | 12 sensitivity scenarios plus volatility/trend regime analysis completed. Most cost/target/confirmation variants remained positive; same-close entry was negative. High-volatility regimes materially outperformed low-volatility regimes. |
| 7 — Walk-forward validation | NEXT | Chronological rolling out-of-sample windows using frozen Phase 6 base rules. |
| 8 — Manuscript | NOT STARTED | Final manuscript after validation phases. |

## Current conclusion
The historical extension materially expands the sample. Under the deterministic reconstruction, the aggregate result is positive and the bootstrap 95% interval for mean trade P&L is above zero. However, 2020 contributes an unusually large share of the aggregate P&L, and the model still has daily-data, discretionary-rule and third-party-data limitations.

For the specific adjustment question: **adjustments remained loss-making in the long sample**. There were 39 adjustment exits, with zero profitable adjustment exits and total net P&L of -₹42,149.70.

## Next research action
Freeze the historical rules and run robustness/sensitivity analysis, including a dedicated 2020 exclusion/regime analysis and parameter sensitivity before any final trading-system conclusion.
