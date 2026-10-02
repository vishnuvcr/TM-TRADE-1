# TM TRADE 1

Research project: empirical evaluation of a NIFTY positional double-calendar option-selling framework.

## Current status

Phase 0 (specification and audit trail) is initialized. Phase 1 is in progress on the `phase-1-data` branch: historical NIFTY option data and a reproducible backtest data path are being validated.

## Research controls
- [Research plan](research/RESEARCH_PLAN.md)
- [Research status](research/STATUS.md)
- [Error log](research/ERROR_LOG.md)
- [Assumptions register](research/ASSUMPTIONS.md)
- [Source notes](research/SOURCE_NOTES.md)

## Strategy under test
The supplied source describes monthly and bi-weekly ATM double calendars with fixed profit targets, time exits, and full-position redeployment after a break-even breach. The exact numerical strike/Greek/IV filters are not fully specified, so the quantitative implementation will expose these as explicit assumptions and sensitivity tests rather than presenting them as source facts.

## Branching
Each research phase is developed on a dedicated branch. Main is used for the consolidated status, links, and completed phase outputs.

## Reproducibility
Historical data will be cached and checksummed. Backtest code will be runnable in GitHub Actions with manual dispatch, and results will be stored as machine-readable artifacts and research outputs.

## Stop criterion
The project ends after the planned data, deterministic backtest, robustness, walk-forward validation, and manuscript phases. The objective is a usable empirical conclusion, not an indefinite research loop.
