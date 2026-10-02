# Research Status

Last updated: 2026-10-02

| Phase | Status | Current result |
|---|---|---|
| 0 — Specification/audit | COMPLETE | Strategy rules, assumptions, research plan and error log initialized. |
| 1 — Data acquisition | COMPLETE / EXTENDED | Historical NIFTY daily option data acquired through a cached Hugging Face pipeline; coverage and hashes recorded. |
| 2 — Deterministic strategy engine | COMPLETE | Monthly + bi-weekly reconstruction implemented with explicit operational assumptions. |
| 3 — Cost/execution model | COMPLETE / EXTENDED | Entry/exit slippage, brokerage, exchange charges, historical STT, stamp duty and GST modeled. |
| 4 — Core backtest | COMPLETE / AUDITED | 28 trades in 2025-09 to 2026-07; net P&L ₹17,709.28. |
| 5 — Historical extension | COMPLETE / AUDITED | 264 reconstructed segments over the 2020-2026 requested window; net P&L ₹11,71,475.36. |
| 6 — Robustness/sensitivity | COMPLETE | 12 sensitivity scenarios plus volatility/trend regime analysis. Most cost/target/confirmation variants remained positive; same-close entry was negative. High-volatility regimes materially outperformed low-volatility regimes. |
| 7 — Walk-forward validation | COMPLETE | 123 chronological validation trades across 2023, 2024, 2025 and 2026 YTD; every window had positive realized P&L, but every bootstrap interval included zero. |
| 8 — Manuscript | COMPLETE | Final structured manuscript, tables, figures, appendices and reproducibility references committed. |

## Final empirical conclusion

Under the frozen deterministic reconstruction, the strategy produced positive aggregate historical P&L after modeled costs and remained positive in every chronological validation window tested from 2023 through 2026 YTD. The evidence is not statistically decisive at the individual validation-window level because all bootstrap intervals include zero.

The strongest caveats are:
- material sensitivity to entry convention;
- substantial concentration of historical P&L in high-volatility regimes;
- a large 2020 contribution;
- 39/39 losing adjustment exits;
- daily-bar and third-party-data limitations;
- discretionary source rules that cannot be reproduced exactly.

No parameter was promoted from sensitivity testing into the base strategy after walk-forward validation.

## Research stop criterion

The planned research phases are complete. Further work is listed under Future Research in the final manuscript rather than extending the current research indefinitely.
