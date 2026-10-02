# Phase 9 — Monthly vs Bi-weekly Differential Analysis

## Purpose

This bounded extension decomposes the frozen NIFTY double-calendar reconstruction into its monthly and bi-weekly components. It is descriptive: no parameters were optimized and no component-specific rule was promoted into the base strategy.

The primary historical ledger is the Phase 5 artifact (264 trade segments, 2020-01-01 through the latest valid trade exit on 2026-06-05). Regime decomposition uses the Phase 6 regime artifact. The previously completed Phase 7 walk-forward artifacts contain summary statistics but not component-level trade ledgers, so component-specific walk-forward attribution is not claimed here.

## Frozen specification

- Monthly target: ₹3,000/lot.
- Bi-weekly target: ₹1,600/lot.
- Entry: next available scheduled trading-day open.
- ATM: nearest common listed strike.
- Slippage: 10 bps adverse on entry and exit.
- Historical brokerage/statutory cost model.
- Same deterministic break-even/adjustment framework as the historical reconstruction.

## 1. Headline differential

| Metric | Monthly | Bi-weekly |
|---|---:|---:|
| Trades | 88 | 176 |
| Share of trades | 33.3% | 66.7% |
| Winners | 51 | 83 |
| Win rate | 57.95% | 47.16% |
| Gross P&L | ₹7,49,961.44 | ₹4,73,596.42 |
| Costs | ₹21,373.59 | ₹30,708.80 |
| Net P&L | **₹7,28,587.80** | **₹4,42,887.56** |
| Share of total net P&L | **62.19%** | **37.81%** |
| Average net/trade | **₹8,279.41** | **₹2,516.41** |
| Median net/trade | **₹1,058.87** | **-₹231.05** |
| Average winner | ₹15,657.70 | ₹7,893.13 |
| Average loser | -₹1,890.67 | -₹2,282.17 |
| Profit factor | **11.42** | **3.09** |
| Average holding | 4.50 days | 3.78 days |
| Maximum component-sequence DD* | -₹23,365.66 | -₹65,456.98 |

*Component-sequence drawdown is calculated from each component's own chronological trade sequence; it is not a portfolio drawdown because the two streams interleave in time.

### Differential interpretation

The monthly component generated 62.2% of total net P&L from only one-third of the trade segments. Its average net P&L per trade was approximately 3.29 times the bi-weekly figure.

The difference is driven by both sides of the payoff distribution:

- Monthly average winner: ₹15,658 versus ₹7,893 bi-weekly.
- Monthly average loser: -₹1,891 versus -₹2,282 bi-weekly.
- Monthly median trade was positive; bi-weekly median trade was negative.
- Monthly profit factor was approximately 3.7 times the bi-weekly profit factor.

Thus, the monthly advantage is not explained by win rate alone. It combines a higher hit rate, much larger winning trades, and smaller average losing trades.

## 2. Exit-mechanism decomposition

| Component | Exit | Trades | Net P&L | Avg/trade | Avg holding |
|---|---|---:|---:|---:|---:|
| Monthly | Target | 37 | ₹7,82,292.88 | ₹21,143.05 | 3.76 d |
| Monthly | Adjustment | 17 | -₹20,997.04 | -₹1,235.12 | 3.47 d |
| Monthly | Break-even | 8 | -₹17,699.25 | -₹2,212.41 | 6.88 d |
| Monthly | Time | 26 | -₹15,008.79 | -₹577.26 | 5.50 d |
| Bi-weekly | Target | 56 | ₹6,35,356.79 | ₹11,345.66 | 2.25 d |
| Bi-weekly | Adjustment | 22 | -₹21,152.66 | -₹961.48 | 1.91 d |
| Bi-weekly | Break-even | 37 | -₹58,385.08 | -₹1,577.98 | 4.51 d |
| Bi-weekly | Time | 61 | -₹1,12,931.49 | -₹1,851.34 | 5.43 d |

### Exit-rate differential

| Exit type | Monthly | Bi-weekly |
|---|---:|---:|
| Target | 42.05% | 31.82% |
| Adjustment | 19.32% | 12.50% |
| Break-even | 9.09% | 21.02% |
| Time | 29.55% | 34.66% |

The clearest structural difference is the higher monthly target-exit rate and the much smaller monthly losses from non-target exits.

Monthly target exits contributed ₹7.82 lakh, while all non-target exits together lost only ₹53,705. Bi-weekly target exits contributed ₹6.35 lakh, but non-target exits lost ₹1.92 lakh.

This explains why the bi-weekly component can have a positive aggregate result while having a much weaker profit factor: its target exits are substantially smaller and are offset by much larger cumulative non-target losses.

## 3. Cost drag

| Metric | Monthly | Bi-weekly |
|---|---:|---:|
| Total costs | ₹21,373.59 | ₹30,708.80 |
| Cost / trade | ₹242.88 | ₹174.48 |
| Costs / gross P&L | 2.85% | 6.48% |

The bi-weekly component has lower modeled cost per trade but substantially greater aggregate cost and cost drag relative to gross P&L. Its weaker gross payoff distribution makes execution costs more consequential.

## 4. Calendar-year differential

| Year | Monthly trades | Monthly net | Bi-weekly trades | Bi-weekly net |
|---|---:|---:|---:|---:|
| 2020 | 15 | ₹4,42,695.72 | 29 | ₹4,16,956.83 |
| 2021 | 12 | ₹89,952.50 | 29 | **-₹16,278.12** |
| 2022 | 14 | ₹1,04,316.06 | 31 | ₹10,099.33 |
| 2023 | 12 | ₹6,663.19 | 25 | ₹175.14 |
| 2024 | 15 | ₹56,344.60 | 26 | **-₹55,935.89** |
| 2025 | 14 | ₹19,533.75 | 28 | ₹83,007.78 |
| 2026* | 6 | ₹9,081.98 | 8 | ₹4,862.49 |

*Through the latest valid reconstructed trade period.

### Year-level observation

The monthly component was positive in **every calendar year** in the historical ledger.

The bi-weekly component was negative in **2021 and 2024**, and was approximately flat in 2023.

This is a major consistency difference in the available reconstruction.

## 5. 2020 dependence

2020 contributed:

- Monthly: ₹4,42,695.72, or **60.8%** of monthly total net P&L.
- Bi-weekly: ₹4,16,956.83, or **94.1%** of bi-weekly total net P&L.

After excluding 2020:

| Component | Trades | Net P&L | Profit factor |
|---|---:|---:|---:|
| Monthly | 73 | **₹2,85,892.08** | 5.65 |
| Bi-weekly | 147 | **₹25,930.73** | 1.13 |

This is one of the strongest differential findings.

The monthly component retains a substantial positive result after removing 2020. The bi-weekly component is reduced to a near-flat result with a profit factor only slightly above 1.

This does not establish future performance, but it demonstrates that the aggregate bi-weekly result is far more concentrated in the 2020 environment.

## 6. Volatility-regime differential

The Phase 6 regime ledger allows the same pre-entry 20-day realized-volatility classification to be cross-tabulated by component.

| Component | Volatility | Trades | Win rate | Net P&L | PF |
|---|---|---:|---:|---:|---:|
| Monthly | High vol | 46 | 60.9% | ₹6,42,078 | 22.87 |
| Monthly | Low vol | 42 | 54.8% | ₹86,509 | 3.13 |
| Bi-weekly | High vol | 91 | 53.8% | ₹4,23,375 | 5.32 |
| Bi-weekly | Low vol | 85 | 40.0% | ₹19,512 | 1.17 |

Both components benefited from high-volatility conditions, but the monthly component's high-volatility profit factor was substantially larger.

The low-volatility difference is also notable: monthly remained strongly positive, while bi-weekly was only marginally positive.

## 7. Joint volatility/trend regimes

| Component | Regime | Trades | Win rate | Net P&L | PF |
|---|---|---:|---:|---:|---:|
| Monthly | High vol / downtrend | 23 | 56.5% | ₹2,99,282 | 23.21 |
| Monthly | High vol / uptrend | 23 | 65.2% | ₹3,42,797 | 22.58 |
| Monthly | Low vol / downtrend | 12 | 50.0% | -₹672 | 0.96 |
| Monthly | Low vol / uptrend | 30 | 56.7% | ₹87,182 | 4.56 |
| Bi-weekly | High vol / downtrend | 41 | 61.0% | ₹1,67,606 | 8.79 |
| Bi-weekly | High vol / uptrend | 50 | 48.0% | ₹2,55,769 | 4.34 |
| Bi-weekly | Low vol / downtrend | 23 | 43.5% | ₹59,381 | 2.60 |
| Bi-weekly | Low vol / uptrend | 62 | 38.7% | **-₹39,869** | **0.48** |

The strongest differential is the low-volatility/uptrend bucket: the monthly component remained positive, whereas the bi-weekly component was negative with a profit factor below 1.

These are descriptive regime results, not evidence that a regime filter should be added to either strategy.

## 8. Mean trade differential

Observed mean net P&L per trade:

- Monthly: ₹8,279.41.
- Bi-weekly: ₹2,516.41.
- Difference: **₹5,763.00 per trade**.

A bootstrap comparison of the difference in component means produced an approximate 95% interval of:

**₹646 to ₹11,837.**

This is a descriptive resampling result. It does not account for serial dependence, overlapping market conditions or multiple-testing considerations.

## 9. What explains the differential?

The evidence points to four interacting mechanisms:

### A. Monthly wins are larger

The average monthly winner was approximately twice the average bi-weekly winner.

### B. Monthly losses are smaller

The average monthly loser was about ₹392 smaller in absolute value.

### C. Monthly avoids more negative non-target outcomes

Monthly had much lower break-even and time-exit rates.

### D. Bi-weekly performance is more regime-dependent

The bi-weekly component was especially weak in low-volatility/uptrend conditions and in 2021/2024, whereas monthly remained positive across all calendar years.

## 10. Important qualification

This analysis does **not** establish that the monthly component should replace the bi-weekly component.

The two components are not independent experiments. They share:

- the same underlying NIFTY market;
- the same option-data source;
- the same deterministic ATM approximation;
- the same execution model;
- the same break-even model;
- overlapping calendar periods;
- potentially overlapping capital and market exposures.

Therefore the differential should be interpreted as **component attribution**, not as a randomized comparison.

## 11. Walk-forward limitation

The completed Phase 7 validation established positive aggregate realized P&L in 2023, 2024, 2025 and 2026 YTD, but its committed artifacts contain window-level summaries rather than component-level trade ledgers.

Accordingly, this Phase 9 report does **not** invent monthly/bi-weekly walk-forward attribution.

A future higher-frequency validation could calculate this directly, but doing so would constitute another explicitly authorized research extension.

## 12. Differential conclusion

The historical reconstruction shows a clear structural asymmetry:

> **The monthly component is the more consistent source of modeled P&L in this dataset, while the bi-weekly component is higher-frequency, less efficient per trade, and substantially more dependent on favorable regimes—especially 2020.**

The strongest quantitative evidence is:

1. Monthly generated ₹7.29 lakh versus ₹4.43 lakh bi-weekly.
2. Monthly generated this with half as many trade segments.
3. Monthly average net P&L/trade was ₹8,279 versus ₹2,516.
4. Monthly profit factor was 11.42 versus 3.09.
5. Monthly was positive in every calendar year in the historical ledger.
6. Bi-weekly was negative in 2021 and 2024.
7. Excluding 2020 left monthly with ₹2.86 lakh net but bi-weekly with only ₹25,931.
8. Monthly's target exits averaged ₹21,143 net versus ₹11,346 for bi-weekly.
9. Monthly's combined non-target exits lost ₹53,705 versus ₹1,92,469 for bi-weekly.
10. In low-volatility/uptrend conditions, monthly produced ₹87,182 while bi-weekly produced -₹39,869.

The differential therefore appears to arise primarily from **payoff quality and consistency rather than trade frequency**.

This remains an empirical property of the deterministic reconstruction, not a forecast of future profitability.
