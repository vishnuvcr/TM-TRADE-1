# TM TRADE 1

Research project: empirical evaluation of a NIFTY positional double-calendar option-selling framework.

## Current status

**Final audited core deterministic backtest completed.** The daily-option sample from 2025-09-01 through 2026-07-28 produced 28 reconstructed trades and **₹17,709.28 net P&L** on the modelled ₹1.20 lakh/lot capital proxy after brokerage, exchange levies, STT, stamp duty, GST and 10-bps entry/exit slippage. The positive combined result is driven by the monthly variant; the bi-weekly variant is negative in this sample.

## Research controls

- [Research plan](research/RESEARCH_PLAN.md)
- [Research status](research/STATUS.md)
- [Error log](research/ERROR_LOG.md)
- [Assumptions register](research/ASSUMPTIONS.md)
- [Source notes](research/SOURCE_NOTES.md)
- [Literature notes](research/LITERATURE_NOTES.md)
- [Data sources](research/DATA_SOURCES.md)
- [Final core backtest report](research/results/CORE_BACKTEST_RESULTS.md)
- [Final trade ledger](research/results/trade_ledger.csv)
- [Final machine-readable summary](research/results/summary.json)

## Strategy under test

The supplied source describes monthly and bi-weekly ATM double calendars with fixed profit targets, time exits, and full-position redeployment after a break-even breach. Exact Greek/IV/OI/strike filters and some execution timings are discretionary in the source, so this quantitative implementation makes those choices explicit.

## Reproducibility

The backtest code is in `scripts/run_backtest.py`. GitHub Actions caches the public market-data DuckDB file and has a manual `workflow_dispatch` button plus automatic runs on code/workflow changes.

## Research result at this stage

The final core run is **not yet a validated trading-system conclusion**. The bootstrap 95% interval for mean trade P&L crosses zero, daily data cannot reconstruct intraday execution order, and the monthly and bi-weekly variants behave differently. The next planned stage is robustness/sensitivity testing, followed by frozen-parameter walk-forward validation and the final research manuscript.
