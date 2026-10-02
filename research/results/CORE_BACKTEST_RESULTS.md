# Core Backtest Results — NIFTY Positional Double-Calendar Framework

## Status
Phase 4 (core deterministic backtest): **completed** on 2026-10-02.

Successful GitHub Actions run: **37015101390**.
Data-cache SHA-256: **d0a07420b9981a94ef1960f7650196dbca730986852cb6515afa9c7f7b3a2694**.

## Test definition
- Window: **2025-09-01 through 2026-07-28**.
- Instrument: **NIFTY index options**.
- Data: public third-party DuckDB cache from the `aaryan-say/nifty-options-delta-neutral-backtest` repository.
- Source-reported coverage: NIFTY OHLC from 2025-03-24 onward and 71 expiries through 2026-07-28.
- Entry: first trading day after the cycle boundary, using option **open**.
- ATM: nearest strike common to CE/PE in both near and far expiries on entry.
- Marking / exits: daily option **close**.
- Daily data means intraday target/breach ordering cannot be reconstructed.
- Break-even: model-based Black-Scholes inversion from observed close prices and current theoretical payoff roots.
- Slippage: **10 bps adverse** per option execution.
- Capital proxy: **₹1.20 lakh per lot**.

## Cost model
- Paytm Money brokerage: **₹10 per executed order**.
- NSE equity-option transaction charges: **0.03553% of traded premium value per side**.
- SEBI turnover fee: **0.0001%**.
- Stamp duty on option purchases: **0.003%**.
- STT on option sales: **0.10% through 2026-03-31; 0.15% from 2026-04-01**.
- GST: **18%** on brokerage and exchange transaction-charge component in this first implementation.

## Core results
| Metric | Result |
|---|---:|
| Reconstructed trades | **29** |
| Winning trades | **14** |
| Losing trades | **15** |
| Win rate | **48.28%** |
| Gross P&L | **₹28,596.26** |
| Modeled costs + slippage impact | **₹7,745.89** |
| Net P&L | **₹20,850.33** |
| Average net P&L / trade | **₹718.98** |
| Median net P&L / trade | **-₹24.98** |
| Profit factor | **1.71** |
| Worst trade | **-₹6,156.44** |
| Best trade | **₹9,888.77** |
| Trade-sequence max drawdown | **-₹10,330.32 (8.61% of ₹1.20L)** |
| Average holding period | **3.45 days** |
| Adjustment segments | **8** |
| Lowest monthly return on ₹1.20L proxy | **-2.18%** |
| Highest monthly return on ₹1.20L proxy | **+5.70%** |

The drawdown above is based on realized trade P&L, not full daily mark-to-market, so it can understate interim risk.

## Monthly vs bi-weekly
| Variant | Trades | Gross P&L | Costs | Net P&L | Win rate | Profit factor |
|---|---:|---:|---:|---:|---:|---:|
| Monthly | 12 | ₹31,682.62 | ₹3,916.68 | **₹27,765.93** | 58.33% | **4.00** |
| Bi-weekly | 17 | -₹3,086.36 | ₹3,829.21 | **-₹6,915.60** | 41.18% | 0.65 |
| Combined | 29 | ₹28,596.26 | ₹7,745.89 | **₹20,850.33** | 48.28% | 1.71 |

The positive combined result is driven primarily by the **monthly** variant. The **bi-weekly** variant is negative in this reconstructed sample.

## Exit-reason decomposition
| Exit reason | Trades | Net P&L |
|---|---:|---:|
| Target | 12 | **₹50,018.03** |
| Adjustment | 8 | **-₹14,110.08** |
| Time exit | 5 | **-₹11,028.58** |
| Break-even exit | 4 | **-₹4,029.04** |

Target exits supplied most of the positive realized P&L; adjustment and time-exit segments accounted for most losses.

## Monthly realized P&L
- 2025-10: **-₹2,417.79**
- 2025-11: **+₹6,408.74**
- 2025-12: **-₹446.14**
- 2026-01: **+₹6,606.83**
- 2026-02: **-₹70.79**
- 2026-03: **+₹4,478.51**
- 2026-04: **+₹6,836.90**
- 2026-05: **-₹2,621.12**
- 2026-06: **+₹2,075.19**

## Interpretation
1. The documented framework is not uniformly profitable across its variants in this sample.
2. The reconstructed **monthly double calendar** is materially stronger than the bi-weekly version.
3. The combined result remains positive after modeled costs and 10-bps adverse slippage, but implementation costs remove a meaningful fraction of gross P&L.
4. Losses cluster in the adjustment and time-exit paths.
5. This is a **deterministic reconstruction**, not a replication of the creator's exact live execution, because the source explicitly leaves entry timing, strike filters, IV/Greek checks and breach confirmation partly discretionary.

## Limitations
- Daily OHLC cannot identify intraday target/breach ordering.
- Exact numerical strike/IV/Greek/OI filters are not fully specified in the source.
- The break-even calculation is an approximation of a broker/Sensibull payoff engine.
- 10-bps slippage is a sensitivity assumption, not an observed bid/ask measurement.
- ₹1.20 lakh is a capital proxy rather than live SPAN margin.
- The reported drawdown is not full mark-to-market drawdown.
- The public dataset is third-party cached data; a later phase should cross-check selected observations against NSE archives.
- One historical window is insufficient to establish robustness.

## Next phase
Run slippage/cost sensitivity, target-before-vs-after-cost tests, entry-time sensitivity, break-even confirmation sensitivity, monthly-only vs bi-weekly-only tests, market-regime splits, and walk-forward out-of-sample validation.