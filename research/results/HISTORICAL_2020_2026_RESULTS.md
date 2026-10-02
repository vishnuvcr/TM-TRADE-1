# Phase 5 — Historical 2020-2026 Backtest Results

## Status

Historical extension completed successfully in GitHub Actions run **37023127851**.

- Requested window: 2020-01-01 to 2026-07-28
- Actual NIFTY spot coverage in the assembled dataset: 2020-01-01 to 2026-07-02
- Latest reconstructed trade exit: 2026-06-05
- Option rows: 3,117,931
- Spot days: 1,599
- Distinct option expiries: 371
- Dataset SHA-256: `e4c6d2e1ddd2dbd9a7ab4c3be5460585ca5d8f0267123cd30b507cbbf6414bed`
- Actions artifact: 11233429861

## Core results

| Metric | 2020-2026 reconstruction |
|---|---:|
| Reconstructed trade segments | 264 |
| Winners | 134 |
| Losers | 130 |
| Win rate | 50.76% |
| Gross P&L | ₹12,23,557.86 |
| Costs | ₹52,082.39 |
| Net P&L | ₹11,71,475.36 |
| Average net/trade | ₹4,437.41 |
| Median net/trade | ₹144.71 |
| Profit factor | 5.15 |
| Best trade | ₹1,67,157.00 |
| Worst trade | -₹16,100.51 |
| Max realized trade-sequence drawdown | -₹48,647.19 |
| Max drawdown / ₹1.20L proxy | -40.54% |
| Average holding period | 4.02 days |
| Bootstrap 95% CI for mean trade P&L | ₹2,442.20 to ₹6,668.31 |

The requested end date is retained as the research-window parameter, but the source spot series ends on 2026-07-02. The trade ledger itself ends on 2026-06-05, so no claim is made for later dates.

## Monthly vs bi-weekly

| Variant | Trades | Gross P&L | Costs | Net P&L | Winners | Profit factor |
|---|---:|---:|---:|---:|---:|---:|
| Monthly | 88 | ₹7,49,961.44 | ₹21,373.59 | ₹7,28,587.80 | 51 | 11.42 |
| Bi-weekly | 176 | ₹4,73,596.42 | ₹30,708.80 | ₹4,42,887.56 | 83 | 3.09 |

## Adjustment analysis

This directly answers the question that motivated the historical extension.

- **39 adjustment exits**
- **0 profitable adjustment exits**
- **39 losing adjustment exits**
- Combined adjustment net P&L: **-₹42,149.70**
- Average adjustment net P&L: **-₹1,080.76**
- Median adjustment net P&L: **-₹841.26**
- Monthly adjustments: 17, net **-₹20,997.04**
- Bi-weekly adjustments: 22, net **-₹21,152.66**

Thus, under this deterministic reconstruction, the adjustment mechanism remained a losing component across the much longer sample. This is materially consistent with the shorter 2025-09 to 2026-07 sample, where adjustment segments were also negative.

### Exit-reason decomposition

| Exit reason | Trades | Net P&L |
|---|---:|---:|
| Target | 93 | ₹14,17,649.67 |
| Adjustment | 39 | -₹42,149.70 |
| Break-even exit | 45 | -₹76,084.33 |
| Time exit | 87 | -₹1,27,940.28 |

The aggregate positive result is therefore dominated by target exits, while adjustment, break-even and time exits are negative.

## Yearly realized net P&L

| Year | Net P&L |
|---|---:|
| 2020 | ₹8,59,652.55 |
| 2021 | ₹73,674.38 |
| 2022 | ₹1,14,415.39 |
| 2023 | ₹6,838.33 |
| 2024 | ₹408.71 |
| 2025 | ₹1,02,541.53 |
| 2026 through latest reconstructed trade | ₹13,944.47 |

The 2020 result is unusually large and materially affects the aggregate. It must therefore be treated as a regime-specific observation, not as evidence that the same return magnitude should be expected in later periods.

## Lot-size schedule used

The historical engine uses expiry-date lot-size proxies:

- 50 contracts through the April 2024 transition.
- 25 contracts for the subsequent transition window before the November 2024 revision.
- 75 contracts thereafter until the January 2026 transition.
- 65 contracts from the January 2026 transition onward.

NSE documentation confirms the 50→25 April 2024 revision and the later 75→65 revision; the exact contract-generation transition remains an audit consideration for individual long-dated contracts. citeturn6search19turn6search20

## Costs and execution

The same execution framework was retained: 10 bps adverse slippage on entry and exit, ₹10 Paytm Money brokerage per executed F&O order, exchange/SEBI charges, stamp duty, GST and date-dependent STT.

Historical option STT was modeled as 0.05% before April 2023, 0.0625% from April 2023 through September 2024, 0.10% from October 2024 through March 2026, and 0.15% from April 2026 onward. NSE documents the 2023 and 2024 changes and the April 2026 increase. citeturn8search3turn8search5turn8view0

## Data provenance and limitations

The historical option data was downloaded from the Hugging Face dataset `rissin/nse-options-intraday`, whose documentation states that its daily historical series derives from NSE F&O bhavcopy data and covers NIFTY from 2001 onward. citeturn3view0

NIFTY spot for the later period came from `thetrademarkk/india-index-options-1m`; its published file is an 8.38 MB NIFTY index Parquet file. citeturn5view0 An earlier-period spot fallback came from the published 2017-2021 hourly NIFTY dataset. citeturn2search8

These are third-party transformed datasets, not a direct exchange dump committed to this repository. Selected trades should be cross-checked against NSE archives before treating the historical result as final research evidence. NSE publishes historical contract-wise F&O price/volume data and daily F&O reports. citeturn9search5turn0search11

## Interpretation

The longer sample changes the evidentiary picture relative to the short sample: the trade-level bootstrap interval for mean P&L is now entirely above zero under this deterministic reconstruction. However, the very large 2020 contribution, the fixed ₹1.20 lakh capital proxy, daily rather than intraday execution, third-party transformed data, and discretionary elements in the original strategy source remain important limitations.

Most importantly for the original question, the adjustment mechanism does **not** become profitable when the sample is extended. It produced losses in every reconstructed adjustment segment in this historical run.

## Next phase

Freeze the historical reconstruction rules and perform robustness/sensitivity analysis, especially:

1. Slippage sensitivity.
2. Cost/brokerage sensitivity.
3. Target sensitivity around ₹3,000 monthly and ₹1,600 bi-weekly.
4. Entry-time sensitivity.
5. Break-even confirmation-delay sensitivity.
6. Excluding or separately analyzing 2020.
7. Regime segmentation using volatility and trend measures.
8. Independent cross-checks of selected trades against NSE historical reports.
