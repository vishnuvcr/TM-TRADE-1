# TM TRADE 1

Research project: empirical evaluation of a NIFTY positional double-calendar option-selling framework.

## Current status

**Phase 5 historical extension is in progress.** The original audited daily-option sample from 2025-09-01 through 2026-07-28 produced 28 reconstructed trades and **₹17,709.28 net P&L** on the modelled ₹1.20 lakh/lot capital proxy after brokerage, exchange levies, STT, stamp duty, GST and 10-bps entry/exit slippage. That result remains the baseline and is not being overwritten by the historical extension.

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

## Phase 5 — Historical extension

The new workflow is `.github/workflows/phase5_historical.yml`. It has a manual `workflow_dispatch` control and uses GitHub Actions caching for the Hugging Face dataset cache and the constructed DuckDB. The historical option files are sourced from `rissin/nse-options-intraday` and derive from NSE F&O bhavcopy data; NIFTY spot is sourced from `thetrademarkk/india-index-options-1m`, with a 2017-2021 fallback dataset for the earlier spot period.

The target research window is **2020-01-01 through 2026-07-28**, subject to actual data coverage. Raw market data is not committed to the repository; the repo records source identifiers, hashes, code, manifests and results, while Actions cache stores downloaded/build inputs.

## Research result at this stage

The original core run is **not yet a validated trading-system conclusion**. The bootstrap 95% interval for mean trade P&L crosses zero, daily data cannot reconstruct intraday execution order, and the monthly and bi-weekly variants behave differently. Phase 5 is intended to determine whether the adjustment losses observed in the short sample persist across a longer market history.
