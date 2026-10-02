# Phase 6 — Robustness and Regime Analysis

## Scope

The frozen historical reconstruction was subjected to 12 deterministic sensitivity scenarios plus trailing 20-day volatility/trend regime segmentation.

### Sensitivity results

| Scenario | Trades | Net P&L | Profit factor | Max DD | 95% CI mean P&L |
|---|---:|---:|---:|---:|---:|
| Base | 264 | ₹11,71,475 | 5.15 | -₹48,647 | ₹2,442–₹6,668 |
| 2020 excluded | 216 | ₹3,16,260 | 2.22 | -₹48,647 | ₹298–₹2,837 |
| 0 bps slippage | 267 | ₹12,77,944 | 6.12 | -₹45,077 | ₹2,673–₹7,192 |
| 20 bps slippage | 273 | ₹10,93,710 | 4.58 | -₹59,651 | ₹2,153–₹6,195 |
| 30 bps slippage | 267 | ₹10,66,418 | 4.55 | -₹54,516 | ₹1,954–₹6,185 |
| Monthly target ₹2,000 | 246 | ₹11,99,604 | 6.08 | -₹38,152 | ₹2,667–₹7,507 |
| Monthly target ₹4,000 | 266 | ₹11,95,374 | 5.05 | -₹48,363 | ₹2,527–₹6,721 |
| Bi-weekly target ₹1,000 | 269 | ₹9,49,444 | 4.22 | -₹48,647 | ₹1,655–₹5,710 |
| Bi-weekly target ₹2,200 | 258 | ₹10,67,792 | 4.79 | -₹48,647 | ₹2,140–₹6,432 |
| Same-close entry | 313 | **-₹2,74,505** | **0.49** | **-₹3,00,521** | -₹1,733–-₹61 |
| 2-day confirmation | 237 | ₹13,54,093 | 6.29 | -₹35,286 | ₹3,250–₹8,554 |
| 3-day confirmation | 225 | ₹11,19,852 | 5.26 | -₹32,445 | ₹2,631–₹7,633 |

## Interpretation

1. **Slippage:** the aggregate result remains positive at 20 and 30 bps adverse slippage in this model. Costs reduce performance but do not eliminate the aggregate result.
2. **Target:** moving the monthly target from ₹3,000 to ₹2,000 or ₹4,000 and the bi-weekly target from ₹1,600 to ₹1,000 or ₹2,200 leaves positive aggregate P&L in every tested scenario.
3. **2020 dependence:** excluding 2020 reduces net P&L from ₹11.71 lakh to ₹3.16 lakh, but the bootstrap interval remains above zero. The result is therefore not solely caused by 2020, although 2020 materially contributes to the aggregate.
4. **Entry timing:** using same-day close rather than next-open produces a strongly negative result. This demonstrates substantial dependence on the entry convention and reinforces that daily OHLC data cannot reproduce intraday discretionary execution.
5. **Break-even confirmation:** two-day confirmation produced the largest aggregate P&L among tested confirmation delays; three-day confirmation remained positive. This is a sensitivity finding, not a parameter-selection recommendation.
6. The original source's ₹3,000 monthly and ₹1,600 bi-weekly targets remain the frozen base specification; alternative targets are robustness tests only.

## Regime analysis

Using only information available before each trade entry:

| Regime | Trades | Net P&L | Win rate | Profit factor |
|---|---:|---:|---:|---:|
| High 20-day realized volatility | 137 | ₹10,65,454 | 56.20% | 9.36 |
| Low 20-day realized volatility | 127 | ₹1,06,021 | 44.88% | 1.68 |
| 20-day downtrend | 99 | ₹5,25,596 | 54.55% | 6.95 |
| 20-day uptrend | 165 | ₹6,45,879 | 48.48% | 4.33 |

The joint buckets were:

- High-vol / down-trend: 64 trades, ₹4,66,888 net, PF 14.35.
- High-vol / up-trend: 73 trades, ₹5,98,566 net, PF 7.48.
- Low-vol / down-trend: 35 trades, ₹58,708 net, PF 2.10.
- Low-vol / up-trend: 92 trades, ₹47,313 net, PF 1.47.

This suggests that the reconstructed framework's historical performance was concentrated in higher-volatility environments. The analysis does not establish that volatility filtering would improve future performance because the filter itself has not yet been validated out-of-sample.

## Phase 6 conclusion

The strategy's aggregate historical result is reasonably robust to the tested cost, target and confirmation perturbations, but it is **not robust to entry-price convention**. The regime analysis also shows substantial heterogeneity.

The correct next step is chronological validation using the frozen base rules, without selecting parameters based on the robustness results.
