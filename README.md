# TM TRADE 1

Research project: empirical evaluation of a NIFTY positional double-calendar option-selling framework.

## Final research status

**The planned research is complete through chronological validation and manuscript production.**

The frozen deterministic reconstruction produced **264 historical trade segments and ₹11,71,475.36 net P&L** over the 2020-2026 requested window after modeled costs. The later chronological validation produced **123 trades and ₹1,21,608.72 net P&L** across 2023, 2024, 2025 and 2026 YTD, with positive realized P&L in every window.

This is **not a claim of guaranteed or statistically proven future profitability**. Every individual chronological validation window had a bootstrap confidence interval that included zero.

The most important structural findings are:

- Monthly target: **₹3,000/lot**.
- Bi-weekly target: **₹1,600/lot**.
- 39 adjustment exits were reconstructed and **all 39 were loss-making**, totaling **-₹42,149.70**.
- High-volatility regimes materially outperformed low-volatility regimes.
- The result remained positive under tested 20–30 bps adverse slippage.
- Excluding 2020 left **₹3,16,260** net P&L.
- Same-close entry produced **-₹2,74,505**, demonstrating material execution-timing sensitivity.

## Final manuscript

- [Final research manuscript](research/results/FINAL_RESEARCH_MANUSCRIPT.md)
- [Historical 2020-2026 results](research/results/HISTORICAL_2020_2026_RESULTS.md)
- [Phase 6 robustness and regime results](research/results/PHASE6_ROBUSTNESS_RESULTS.md)
- [Phase 7 walk-forward results](research/results/PHASE7_WALKFORWARD_RESULTS.md)
- [Historical machine-readable summary](research/results/historical_summary.json)
- [Historical P&L figure](research/results/figures/historical_net_pnl.svg)
- [Walk-forward P&L figure](research/results/figures/walkforward_net_pnl.svg)

## Research controls

- [Research plan](research/RESEARCH_PLAN.md)
- [Research status](research/STATUS.md)
- [Error log](research/ERROR_LOG.md)
- [Assumptions register](research/ASSUMPTIONS.md)
- [Source notes](research/SOURCE_NOTES.md)
- [Literature notes](research/LITERATURE_NOTES.md)
- [Data sources](research/DATA_SOURCES.md)
- [Core backtest report](research/results/CORE_BACKTEST_RESULTS.md)
- [Final trade ledger](research/results/trade_ledger.csv)

## Reproducibility

Historical dataset SHA-256:
e4c6d2e1ddd2dbd9a7ab4c3be5460585ca5d8f0267123cd30b507cbbf6414bed

Key GitHub Actions runs:

- Historical reconstruction: 37023127851
- Robustness sensitivity: 37024072980
- Regime analysis: 37024672046
- Walk-forward validation: 37025149087

All major workflows retain manual workflow-dispatch controls and use cached historical data rather than re-downloading the market dataset on every run.

## Final interpretation

The documented double-calendar framework has a positive historical deterministic reconstruction under the frozen next-open execution convention. Its performance is materially regime- and execution-dependent, and the adjustment component is consistently loss-making in the available data.

The study therefore supports further controlled paper/live validation and higher-frequency research, but it does not establish a guaranteed or stable future trading edge.
