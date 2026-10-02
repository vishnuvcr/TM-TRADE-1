# TM TRADE 1

Research project: empirical evaluation of a NIFTY positional double-calendar option-selling framework.

## Current status

**Phase 5 historical extension is complete.** The 2020-2026 requested window produced **264 reconstructed trade segments and ₹11,71,475.36 net P&L** after modeled execution costs. The long-sample result is not yet the final trading-system conclusion; Phase 6 robustness and walk-forward validation remain.

Most relevant to the original question: the historical extension found **39 adjustment exits, with 0 profitable adjustment exits and -₹42,149.70 total adjustment P&L**.

## Research controls

- [Research plan](research/RESEARCH_PLAN.md)
- [Research status](research/STATUS.md)
- [Error log](research/ERROR_LOG.md)
- [Assumptions register](research/ASSUMPTIONS.md)
- [Source notes](research/SOURCE_NOTES.md)
- [Literature notes](research/LITERATURE_NOTES.md)
- [Data sources](research/DATA_SOURCES.md)
- [Core backtest report](research/results/CORE_BACKTEST_RESULTS.md)
- [Historical 2020-2026 report](research/results/HISTORICAL_2020_2026_RESULTS.md)
- [Historical machine-readable summary](research/results/historical_summary.json)
- [Final trade ledger](research/results/trade_ledger.csv)
- [Final machine-readable summary](research/results/summary.json)

## Strategy under test

The supplied source describes monthly and bi-weekly ATM double calendars with fixed profit targets, time exits, and full-position redeployment after a break-even breach. Exact Greek/IV/OI/strike filters and some execution timings are discretionary in the source, so this quantitative implementation makes those choices explicit.

## Phase 5 — Historical extension

The historical workflow has a manual `workflow_dispatch` control and caches the Hugging Face inputs and constructed DuckDB. The historical option files are from `rissin/nse-options-intraday` and derive from NSE F&O bhavcopy data; NIFTY spot is sourced from `thetrademarkk/india-index-options-1m`, with a 2017-2021 fallback dataset for the earlier spot period.

The requested research window is **2020-01-01 through 2026-07-28**, but the assembled spot data ends on 2026-07-02 and the latest reconstructed trade exits on 2026-06-05. Raw market data is not committed to the repository; source identifiers, hashes, code, manifests and results are recorded instead.

## Next research phase

Phase 6 will test whether the historical result survives slippage/cost/target/entry-time/break-even sensitivities, exclusion of 2020, and market-regime segmentation. Only after those rules are frozen will walk-forward validation and the final manuscript be produced.
