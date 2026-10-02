# NIFTY Positional Double-Calendar Strategy — Corrected Core Backtest

## Status
Corrected core deterministic backtest completed on 2026-10-02.
GitHub Actions run: 37015617205
Data cache SHA-256: d0a07420b9981a94ef1960f7650196dbca730986852cb6515afa9c7f7b3a2694

## Source strategy translated into testable rules
The supplied strategy uses an ATM double calendar: sell the near-expiry ATM call and put and buy the same-strike call and put in the farther expiry. The monthly version targets ₹3,000/lot and normally exits after 7–10 days; the bi-weekly version targets ₹1,600/lot and exits within 7 days. A break-even breach triggers closure of the full position and, when early enough, redeployment at the current spot.
The source also states that real execution uses discretionary judgment around strike selection, Greeks, IV, open interest, timing and confirmation of a breach. Therefore this is a deterministic reconstruction, not an exact replication of the source creator's discretionary live trading.

## Test window and data
- Period: 2025-09-01 to 2026-07-28
- Instrument: NIFTY index options
- Data: cached public daily OHLC DuckDB dataset from aaryan-say/nifty-options-delta-neutral-backtest
- Execution granularity: daily OHLC
- Entry: first trading day after the cycle boundary, option open
- ATM: nearest common CE/PE strike available in both near and far expiries on entry date
- Exit/mark: option close
- Break-even: model-based Black-Scholes inversion from observed option closes
- Slippage: 10 bps adverse on entry and exit executions
- Capital proxy: ₹1.20 lakh/lot

## Corrected transaction-cost model
- Paytm Money brokerage: ₹10 per executed order
- NSE option transaction charge: 0.03553% of traded premium value per side
- SEBI turnover fee: 0.0001%
- Stamp duty: 0.003% on option purchases
- STT: 0.10% on option sales through 2026-03-31 and 0.15% from 2026-04-01
- GST: 18% on brokerage and exchange/SEBI transaction-charge component
Exit-side slippage and the direction of STT versus stamp duty were explicitly audited and corrected before accepting the final run.

## Final core results

| Metric | Result |
|---|---:|
| Trades | 29 |
| Winning trades | 14 |
| Losing trades | 15 |
| Win rate | 48.28% |
| Gross P&L | ₹25,964.23 |
| Costs + slippage | ₹8,246.95 |
| Net P&L | ₹17,717.27 |
| Average net P&L/trade | ₹610.94 |
| Median net P&L/trade | -₹153.70 |
| Profit factor | 1.58 |
| Worst trade | -₹6,218.31 |
| Best trade | ₹9,725.50 |
| Trade-sequence max drawdown | -₹10,870.78 |
| Max drawdown / ₹1.20L proxy | -9.06% |
| Average holding period | 3.45 days |
| Adjustment segments | 8 |
| Lowest monthly return on ₹1.20L proxy | -2.75% |
| Highest monthly return on ₹1.20L proxy | +5.51% |

The reported drawdown is a realized-trade-sequence drawdown, not full daily mark-to-market drawdown.

## Monthly versus bi-weekly

| Variant | Trades | Gross P&L | Costs | Net P&L | Win rate | Profit factor |
|---|---:|---:|---:|---:|---:|---:|
| Monthly | 12 | ₹30,197.55 | ₹4,238.68 | ₹25,958.85 | 58.33% | 3.61 |
| Bi-weekly | 17 | -₹4,233.32 | ₹4,008.27 | -₹8,241.58 | 41.18% | 0.60 |
| Combined | 29 | ₹25,964.23 | ₹8,246.95 | ₹17,717.27 | 48.28% | 1.58 |

The corrected result is therefore primarily driven by the monthly version. The bi-weekly version is negative over this sample.

## Exit-reason decomposition

| Exit reason | Trades | Net P&L |
|---|---:|---:|
| Target | 12 | ₹48,481.40 |
| Adjustment | 8 | -₹14,955.89 |
| Time exit | 5 | -₹11,474.43 |
| Break-even exit | 4 | -₹4,333.81 |

## Monthly realized P&L

| Month | Net P&L | Return on ₹1.20L proxy |
|---|---:|---:|
| 2025-10 | -₹2,681.70 | -2.23% |
| 2025-11 | ₹5,984.97 | +4.99% |
| 2025-12 | -₹562.07 | -0.47% |
| 2026-01 | ₹6,055.08 | +5.05% |
| 2026-02 | -₹449.49 | -0.37% |
| 2026-03 | ₹4,286.83 | +3.57% |
| 2026-04 | ₹6,611.46 | +5.51% |
| 2026-05 | -₹3,295.23 | -2.75% |
| 2026-06 | ₹1,767.42 | +1.47% |

## Statistical qualification
The bootstrap 95% interval for mean trade P&L is approximately -₹568.93 to +₹1,957.92, so the interval includes zero. This is a trade-level resampling interval and does not address serial dependence or parameter uncertainty. The 48.28% win rate is also not itself evidence of a statistical edge; the positive profit factor comes from the average win being much larger than the average loss.

## Interpretation
The corrected deterministic sample is positive in aggregate, but it does not establish a statistically reliable edge. The strongest empirical feature is the large difference between the monthly and bi-weekly variants. Modeled costs and slippage remove about 31.8% of gross P&L.
The source's live-performance statement that no month was below -1% is not reproduced by this deterministic backtest; the worst reconstructed month is approximately -2.75%. That difference is not a direct contradiction because the source itself describes discretionary execution and because the backtest uses daily rather than intraday data.

## Limitations
1. Daily OHLC cannot reconstruct intraday target/break-even ordering.
2. Exact source strike/IV/Greek/OI filters are not numerically specified.
3. The break-even calculation is a model approximation rather than an exchange/broker payoff snapshot.
4. Slippage is assumed, not observed from historical bid/ask quotes.
5. ₹1.20 lakh is a capital proxy, not live SPAN margin.
6. Drawdown is not full mark-to-market drawdown.
7. The current dataset is a third-party cached dataset and should be cross-checked against NSE archives for selected trades before final validation.
8. The sample is relatively short and ends at 2026-07-28, the available data endpoint.

## Next phase
Run parameter sensitivity (slippage, targets, entry timing and breach confirmation), regime segmentation (including volatility/gap states), and frozen-parameter walk-forward validation. Only after those tests should the project produce a final research manuscript/conclusion.