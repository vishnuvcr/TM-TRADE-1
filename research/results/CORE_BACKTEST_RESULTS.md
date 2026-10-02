# NIFTY Positional Double-Calendar Strategy — Final Core Backtest

## Status
Final core deterministic backtest completed on 2026-10-02 after auditing execution costs and contract lot-size transitions.
GitHub Actions run: 37016041530
Data cache SHA-256: d0a07420b9981a94ef1960f7650196dbca730986852cb6515afa9c7f7b3a2694

## Strategy reconstruction
The supplied strategy is a double calendar: sell the near-expiry ATM call and put and buy the same-strike call and put in the farther expiry. The monthly version uses a ₹3,000/lot target with a 7–10 day exit window; the bi-weekly version uses a ₹1,600/lot target and a 7-day maximum holding period. A breach of a break-even is handled by closing the full position and, when early enough, redeploying at the current spot.
The source also explicitly says the live implementation is partly discretionary, including entry timing, strike selection, IV/Greek checks and how long to wait for a breach confirmation. Therefore this is a deterministic reconstruction, not a replication of the creator's exact discretionary trading.

## Test design
- Period: 2025-09-01 to 2026-07-28
- Instrument: NIFTY index options
- Data: cached public daily OHLC DuckDB dataset
- Entry: first trading day after the scheduled cycle boundary, using option open
- ATM: nearest common CE/PE strike available in both the near and far expiries on entry
- Marking and exits: daily option close
- Break-even: model-based Black-Scholes inversion from observed option closes
- Slippage: 10 bps adverse on both entry and exit
- Capital proxy: ₹1.20 lakh per lot
- Lot size: modeled by contract expiry, so the 2025-12/2026-01 transition can contain different near/far contract quantities.

## Costs
- Paytm Money brokerage: ₹10 per executed F&O order
- NSE option transaction charge: ₹3,553 per crore of premium turnover per side, represented as 0.03553%
- SEBI turnover fee: 0.0001%
- Stamp duty on option purchases: 0.003%
- STT on option sales: 0.10% through 2026-03-31 and 0.15% from 2026-04-01
- GST: 18% on brokerage and exchange/SEBI transaction-charge component
The cost model was audited for execution slippage and the direction of STT versus stamp duty on closing long and short option legs.

## Final results

| Metric | Result |
|---|---:|
| Trades | 28 |
| Winning trades | 14 |
| Losing trades | 14 |
| Win rate | 50.00% |
| Gross P&L | ₹25,698.84 |
| Costs + slippage | ₹7,989.54 |
| Net P&L | ₹17,709.28 |
| Cumulative net return on ₹1.20L proxy | 14.76% |
| Average net P&L/trade | ₹632.47 |
| Median net P&L/trade | -₹73.71 |
| Profit factor | 1.58 |
| Worst trade | -₹6,218.31 |
| Best trade | ₹8,108.40 |
| Trade-sequence max drawdown | -₹10,870.78 |
| Max drawdown / ₹1.20L proxy | -9.06% |
| Average holding period | 3.57 days |
| Adjustment segments | 7 |
| Lowest monthly return on ₹1.20L proxy | -2.75% |
| Highest monthly return on ₹1.20L proxy | +6.39% |

The cumulative return is a capital-proxy calculation, not a full portfolio return with daily SPAN margin and mark-to-market capital utilization.

## Monthly vs bi-weekly

| Variant | Trades | Gross P&L | Costs | Net P&L | Win rate | Profit factor |
|---|---:|---:|---:|---:|---:|---:|
| Monthly | 12 | ₹29,125.33 | ₹4,188.54 | ₹24,936.78 | 58.33% | 3.51 |
| Bi-weekly | 16 | -₹3,426.49 | ₹3,801.00 | -₹7,227.50 | 43.75% | 0.65 |
| Combined | 28 | ₹25,698.84 | ₹7,989.54 | ₹17,709.28 | 50.00% | 1.58 |

The positive combined result is primarily driven by the monthly version. The bi-weekly version is negative in the tested sample.

## Exit-reason decomposition

| Exit reason | Trades | Net P&L |
|---|---:|---:|
| Target | 13 | ₹48,488.06 |
| Adjustment | 7 | -₹13,095.89 |
| Time exit | 4 | -₹11,496.21 |
| Break-even exit | 4 | -₹6,186.68 |

## Monthly realized P&L

| Month | Net P&L | Return on ₹1.20L proxy |
|---|---:|---:|
| 2025-10 | -₹2,681.70 | -2.23% |
| 2025-11 | ₹4,367.87 | +3.64% |
| 2025-12 | -₹562.07 | -0.47% |
| 2026-01 | ₹7,664.19 | +6.39% |
| 2026-02 | -₹449.49 | -0.37% |
| 2026-03 | ₹4,286.83 | +3.57% |
| 2026-04 | ₹6,611.46 | +5.51% |
| 2026-05 | -₹3,295.23 | -2.75% |
| 2026-06 | ₹1,767.42 | +1.47% |

## Statistical qualification
The trade-level bootstrap 95% interval for mean net P&L is approximately -₹641.26 to +₹1,963.11, so it still crosses zero. The 50% win rate is not sufficient evidence of an edge; the positive profit factor is driven by larger average winners than losers.
The proxy annualized return implied by compounding the 14.76% cumulative result over the 0.904-year sample is about 16.45%, but this should not be interpreted as a realized portfolio CAGR because margin utilization and daily mark-to-market are not fully modeled.

## Interpretation
The final deterministic reconstruction is positive in aggregate, but it is not statistically decisive and the two strategy variants behave very differently. The monthly version carries the positive result; the bi-weekly version is negative in this sample.
The supplied source reports that, in its live calendar-spread experience, no month fell below -1%. The reconstructed sample reaches approximately -2.75% in its worst month. This difference should not be treated as a direct contradiction because the source itself emphasizes discretionary execution and the backtest is daily rather than intraday.

## Strengths
- Reproducible, rule-based implementation.
- Full four-leg entry/exit treatment.
- Entry and exit slippage explicitly modeled.
- Brokerage and statutory charges included.
- Lot-size transition handled at the contract-expiry level.
- Separate monthly and bi-weekly performance reported.

## Limitations
1. Daily OHLC cannot reconstruct intraday target/breach ordering.
2. Exact source strike/IV/Greek/OI thresholds are not numerically specified.
3. Break-even logic is a model approximation rather than a broker payoff snapshot.
4. Slippage is assumed rather than measured from historical bid/ask quotes.
5. ₹1.20 lakh is a capital proxy, not live SPAN margin.
6. Drawdown is based on realized trade P&L, not full mark-to-market.
7. The option dataset is a third-party cache and should be cross-checked against NSE archives for selected trades.
8. The sample is relatively short and ends at 2026-07-28.

## Research conclusion at this phase
The documented framework has a positive deterministic result over the tested sample after modeled execution costs, but the evidence is not strong enough to treat it as a validated trading edge. The next required research stage is robustness/sensitivity testing followed by frozen-parameter walk-forward validation.