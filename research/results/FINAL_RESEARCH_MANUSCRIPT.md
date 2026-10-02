# Empirical Evaluation of a NIFTY Positional Double-Calendar Option Framework

## Abstract

This study evaluates a NIFTY 50 positional double-calendar option framework reconstructed from a supplied strategy specification. The framework sells a near-expiry at-the-money call and put while buying the same-strike farther-expiry call and put, with separate monthly and bi-weekly implementations. The documented profit targets are ₹3,000 per lot for the monthly structure and ₹1,600 per lot for the bi-weekly structure.

A deterministic, reproducible implementation was constructed because the source leaves some execution choices discretionary, including exact entry timing, strike selection criteria, and the treatment of break-even breaches. The study uses daily NIFTY index and option data, historical contract specifications, and an explicit transaction-cost/slippage model including brokerage, exchange charges, statutory levies and adverse execution.

The historical reconstruction from 2020 through the available 2026 data produced 264 trade segments and ₹11,71,475.36 net P&L after modeled costs. The bootstrap 95% interval for mean trade P&L was ₹2,442–₹6,668. However, performance was highly heterogeneous: 2020 contributed ₹8,59,653, high-volatility regimes materially outperformed low-volatility regimes, and 39 adjustment exits were all loss-making, totaling -₹42,149.70.

Robustness testing found positive aggregate P&L under 0–30 bps slippage and tested target variations, while same-close entry produced -₹2,74,505 and a profit factor of 0.49. Chronological validation on untouched 2023, 2024, 2025 and 2026 windows produced positive realized P&L in every window, totaling ₹1,21,608.72, but every individual window's bootstrap interval included zero.

The evidence therefore supports a positive historical association under the specified deterministic reconstruction, but not a claim that future profitability is established. The principal research implications are strong sensitivity to entry convention, concentration of returns in high-volatility regimes, and the need to treat adjustment rules separately from target exits.

---

## 1. Introduction

Calendar spreads exploit differences between option expiries rather than relying solely on the direction of the underlying asset. A double calendar combines call and put calendar positions around a common strike and can therefore be exposed to volatility, term structure, time decay, and changes in the underlying price.

The supplied strategy document describes two recurring NIFTY implementations:

1. A monthly double calendar with a ₹3,000-per-lot target and approximately a 7–10 day holding window.
2. A bi-weekly double calendar with a ₹1,600-per-lot target and approximately a 7-day maximum holding period.

The source also describes redeployment after a convincing break-even breach. It explicitly acknowledges discretionary inputs involving risk/reward, probability, delta, vega, implied volatility, open interest and technical factors. Consequently, this study does not claim to reproduce an author's discretionary live execution exactly. Instead, it tests a transparent deterministic approximation.

### 1.1 Research question

Does the documented NIFTY double-calendar framework produce positive net returns after realistic transaction costs and slippage across materially different market regimes and chronological validation windows?

### 1.2 Secondary questions

- Are the monthly and bi-weekly components separately profitable?
- Does the adjustment mechanism add or subtract from total performance?
- How sensitive are results to slippage, target level, entry convention and break-even confirmation?
- Does excluding the unusually strong 2020 period materially change the conclusion?
- Are results concentrated in particular volatility or trend regimes?
- Does the frozen reconstruction retain positive realized P&L in later out-of-sample windows?

---

## 2. Literature and Research Context

The literature was reviewed in three distinct areas.

### 2.1 Option pricing and volatility

Black and Scholes established the canonical option-pricing framework used here as a computational approximation for option values and break-even calculations. Carr and Wu developed a framework for variance risk premia, which is relevant because calendar strategies can be exposed to the relationship between implied and realized variance.

### 2.2 Indian index-option evidence

Indian NIFTY research provides evidence that option-selling returns can depend strongly on volatility forecasts, overnight risk and the variance-risk premium. The reviewed literature includes work on NIFTY variance risk premia, day/night asymmetry in option returns, and more recent work examining structural properties of NIFTY variance premia.

These findings are contextual rather than direct evidence for the double-calendar strategy. A variance premium does not imply that a particular four-leg calendar construction will be profitable.

### 2.3 Calendar-spread research

Calendar-spread literature emphasizes term-structure and dependence effects between option maturities. Research on calendar spreads in other markets and recent work on option calendar strategies provide mechanism and research-design context, but do not constitute direct NIFTY evidence.

The literature therefore motivates testing volatility regime, term structure and execution effects separately rather than treating all option-selling strategies as equivalent.

---

## 3. Aims and Objectives

### Aim

To empirically evaluate the documented NIFTY positional double-calendar framework under realistic execution costs and across historical market conditions.

### Objectives

1. Translate the documented rules into a reproducible deterministic specification.
2. Acquire and cache historical NIFTY index and option data.
3. Incorporate historical contract specifications and lot-size changes.
4. Model brokerage, exchange charges, statutory levies, GST, stamp duty, STT and adverse slippage.
5. Evaluate monthly and bi-weekly structures separately.
6. Quantify adjustment outcomes.
7. Conduct robustness and sensitivity testing.
8. Segment results by volatility and trend regimes.
9. Perform chronological out-of-sample validation.
10. Document limitations and produce a reproducible research record.

---

## 4. Strategy Specification

### 4.1 Monthly structure

After the prior monthly expiry, the reconstruction sells the new near-month ATM call and put and buys the same-strike farther-month call and put.

Target: ₹3,000 per lot.

Maximum holding period: approximately seven trading/calendar days with a Friday-oriented hard exit.

### 4.2 Bi-weekly structure

The reconstruction skips the immediate weekly expiry, sells the next expiry ATM call and put, and buys the following expiry at the same strike.

Target: ₹1,600 per lot.

Maximum holding period: approximately seven days.

### 4.3 Adjustment

When the contemporaneous payoff break-even is breached according to the deterministic confirmation rule, the complete four-leg structure is closed and, where permitted by the hard deadline, a fresh structure is redeployed.

The adjustment rule is especially important because the source describes it operationally but does not provide a fully numerical implementation.

---

## 5. Data

### 5.1 Option data

Historical NIFTY daily option data was assembled from a cached Hugging Face dataset whose documentation states that its historical daily series derives from NSE F&O bhavcopy data.

The assembled database contained:

- 3,117,931 NIFTY option rows.
- 371 distinct expiries.
- Requested research window: 2020-01-01 to 2026-07-28.

### 5.2 Index data

NIFTY index data was assembled from a public index dataset for the later period and an earlier-period fallback source.

Actual assembled spot coverage ended on 2026-07-02. The latest reconstructed trade exit was 2026-06-05. No synthetic data was created to fill the uncovered tail.

### 5.3 Data integrity

Dataset SHA-256:

e4c6d2e1ddd2dbd9a7ab4c3be5460585ca5d8f0267123cd30b507cbbf6414bed

The raw data is cached through GitHub Actions rather than repeatedly downloaded. Source identifiers, hashes, manifests and research results are retained in the repository.

---

## 6. Methodology

### 6.1 ATM definition

ATM is defined as the listed strike nearest the NIFTY spot value at entry, subject to availability of the same strike for both call and put legs across both expiries.

### 6.2 Entry convention

The frozen base convention uses the first available synchronized daily bar after the scheduled entry date and uses the opening option price with adverse 10-bps execution slippage.

A same-close sensitivity was also tested separately.

### 6.3 Option valuation

Observed option prices are used for entry and exit marks. Black–Scholes implied volatility is used only for deterministic reconstruction of contemporaneous break-even boundaries.

### 6.4 Exit hierarchy

The deterministic hierarchy is:

1. Profit target.
2. Break-even breach leading to adjustment where permitted.
3. Break-even exit where adjustment is no longer permitted.
4. Hard time exit.

### 6.5 Historical lot size

Contract quantity is determined from contract expiry/generation rather than trade date to capture historical lot-size changes.

### 6.6 Transaction costs

The model includes:

- ₹10 Paytm Money brokerage per executed F&O order.
- NSE option transaction charges.
- SEBI fee.
- Stamp duty.
- Historical STT schedule.
- GST on the modeled brokerage/exchange-charge base.
- 10 bps adverse entry slippage.
- 10 bps adverse exit slippage.

The historical cost model was explicitly revised when earlier implementation audits found incorrect exit-side treatment.

### 6.7 Statistical analysis

The study reports:

- Number of trades.
- Win rate.
- Gross and net P&L.
- Average and median trade P&L.
- Profit factor.
- Maximum realized drawdown.
- Holding period.
- Exit-reason decomposition.
- Bootstrap 95% intervals for mean trade P&L.
- Regime-stratified results.
- Chronological out-of-sample results.

The bootstrap intervals are descriptive and do not remove dependence between overlapping market conditions or trades.

---

## 7. Historical Results

### 7.1 Aggregate result

| Metric | Result |
|---|---:|
| Trade segments | 264 |
| Winners | 134 |
| Losers | 130 |
| Win rate | 50.76% |
| Gross P&L | ₹12,23,557.86 |
| Costs | ₹52,082.39 |
| Net P&L | ₹11,71,475.36 |
| Average net/trade | ₹4,437.41 |
| Median net/trade | ₹144.71 |
| Profit factor | 5.15 |
| Best trade | ₹1,67,157 |
| Worst trade | -₹16,100.51 |
| Maximum realized drawdown | -₹48,647.19 |
| Average holding period | 4.02 days |
| Bootstrap 95% CI | ₹2,442–₹6,668 |

### 7.2 Monthly and bi-weekly components

| Variant | Trades | Net P&L | Profit factor |
|---|---:|---:|---:|
| Monthly | 88 | ₹7,28,587.80 | 11.42 |
| Bi-weekly | 176 | ₹4,42,887.56 | 3.09 |

Both components contributed positive aggregate P&L in the deterministic reconstruction.

### 7.3 Exit reasons

| Exit reason | Trades | Net P&L |
|---|---:|---:|
| Target | 93 | ₹14,17,649.67 |
| Adjustment | 39 | -₹42,149.70 |
| Break-even exit | 45 | -₹76,084.33 |
| Time exit | 87 | -₹1,27,940.28 |

The result is therefore not generated uniformly across all exit mechanisms. Target exits provide the dominant positive contribution, while adjustment, break-even and time exits are negative.

### 7.4 Adjustment analysis

There were 39 adjustment exits.

- Profitable adjustments: 0.
- Losing adjustments: 39.
- Net adjustment P&L: -₹42,149.70.
- Average adjustment: -₹1,080.76.

This pattern persisted across the longer sample and therefore deserves separate treatment from the base calendar structure.

### 7.5 Calendar-year results

| Year | Net P&L |
|---|---:|
| 2020 | ₹8,59,652.55 |
| 2021 | ₹73,674.38 |
| 2022 | ₹1,14,415.39 |
| 2023 | ₹6,838.33 |
| 2024 | ₹408.71 |
| 2025 | ₹1,02,541.53 |
| 2026 through latest trade | ₹13,944.47 |

![Historical net P&L](figures/historical_net_pnl.svg)

The concentration of 2020 performance is a major interpretive consideration.

---

## 8. Robustness and Sensitivity

### 8.1 Slippage

The historical result remained positive at 0, 20 and 30 bps adverse slippage:

| Slippage | Net P&L |
|---:|---:|
| 0 bps | ₹12,77,944 |
| 10 bps base | ₹11,71,475 |
| 20 bps | ₹10,93,710 |
| 30 bps | ₹10,66,418 |

This indicates that the aggregate result is not eliminated by the tested increase in execution friction.

### 8.2 Target sensitivity

| Test | Net P&L |
|---|---:|
| Monthly ₹2,000 | ₹11,99,604 |
| Monthly ₹3,000 base | ₹11,71,475 |
| Monthly ₹4,000 | ₹11,95,374 |
| Bi-weekly ₹1,000 | ₹9,49,444 |
| Bi-weekly ₹1,600 base | ₹11,71,475 |
| Bi-weekly ₹2,200 | ₹10,67,792 |

The source-defined ₹3,000/₹1,600 targets remain the base specification. Alternative targets are robustness tests, not optimized replacements.

### 8.3 Entry convention

The same-close entry sensitivity produced:

- Net P&L: -₹2,74,505.
- Profit factor: 0.49.
- Maximum drawdown: -₹3,00,521.

This is the strongest robustness warning in the study. The strategy cannot be considered insensitive to entry convention when using daily data.

### 8.4 2020 exclusion

Removing 2020 reduced net P&L to ₹3,16,260 across 216 trades, with profit factor 2.22 and bootstrap mean-P&L interval approximately ₹298–₹2,837.

Thus the positive aggregate result is materially smaller without 2020, but it does not disappear under this reconstruction.

### 8.5 Break-even confirmation

| Confirmation | Net P&L |
|---|---:|
| 1 day base | ₹11,71,475 |
| 2 days | ₹13,54,093 |
| 3 days | ₹11,19,852 |

The result is sensitive to the confirmation convention, although all tested versions remained positive.

---

## 9. Regime Analysis

Regimes were assigned using only information available before trade entry.

### 9.1 Volatility

| Regime | Trades | Net P&L | Win rate | Profit factor |
|---|---:|---:|---:|---:|
| High 20-day realized volatility | 137 | ₹10,65,454 | 56.20% | 9.36 |
| Low volatility | 127 | ₹1,06,021 | 44.88% | 1.68 |

### 9.2 Trend

| Regime | Trades | Net P&L | Win rate | Profit factor |
|---|---:|---:|---:|---:|
| 20-day downtrend | 99 | ₹5,25,596 | 54.55% | 6.95 |
| 20-day uptrend | 165 | ₹6,45,879 | 48.48% | 4.33 |

### 9.3 Joint regimes

| Volatility / trend | Trades | Net P&L | Profit factor |
|---|---:|---:|---:|
| High vol / downtrend | 64 | ₹4,66,888 | 14.35 |
| High vol / uptrend | 73 | ₹5,98,566 | 7.48 |
| Low vol / downtrend | 35 | ₹58,708 | 2.10 |
| Low vol / uptrend | 92 | ₹47,313 | 1.47 |

The historical performance is strongly heterogeneous across volatility regimes. The analysis does not establish that adding a volatility filter would improve future performance because such a filter has not been separately validated.

---

## 10. Chronological Out-of-Sample Validation

The frozen base specification was evaluated on later chronological windows without parameter optimization.

| Validation window | Trades | Net P&L | Profit factor | Bootstrap 95% CI |
|---|---:|---:|---:|---:|
| 2023 | 35 | ₹1,340 | 1.08 | -₹426 to ₹496 |
| 2024 | 36 | ₹11,644 | 1.16 | -₹2,355 to ₹4,219 |
| 2025 | 40 | ₹90,745 | 2.72 | -₹300 to ₹5,760 |
| 2026 YTD | 12 | ₹17,880 | 2.01 | -₹2,688 to ₹6,573 |

Combined:

- 123 trades.
- ₹1,21,608.72 net P&L.
- Positive realized net P&L in all four windows.

![Chronological out-of-sample net P&L](figures/walkforward_net_pnl.svg)

The chronological results are encouraging as a replication check, but the individual samples are small and every confidence interval includes zero.

---

## 10A. Monthly vs Bi-weekly Differential Analysis

A bounded post-validation extension decomposed the historical ledger by strategy component without changing the frozen base rules. The monthly component comprised 88 reconstructed segments and produced ₹7,28,587.80 net P&L; the bi-weekly component comprised 176 segments and produced ₹4,42,887.56.

The differential was substantial at the trade level. Monthly average net P&L was ₹8,279 per segment versus ₹2,516 for bi-weekly, with profit factors of 11.42 and 3.09 respectively. Monthly's median trade was positive at ₹1,058.87, while the bi-weekly median was -₹231.05. Monthly average winners were approximately ₹15,658 versus ₹7,893 for bi-weekly, while average losers were approximately -₹1,891 versus -₹2,282.

The exit decomposition provides a mechanism for the difference. Monthly had 37 target exits generating ₹7,82,292.88, while its non-target exits combined lost ₹53,705.08. Bi-weekly had 56 target exits generating ₹6,35,356.79, but its non-target exits combined lost ₹1,92,469.23. Thus, the monthly advantage reflects both larger winning trades and substantially smaller cumulative losses from non-target exits.

Calendar-year consistency also differed. Monthly was positive in every calendar year in the reconstructed ledger. Bi-weekly was negative in 2021 and 2024 and nearly flat in 2023. Excluding 2020 left ₹2,85,892.08 net for monthly versus only ₹25,930.73 for bi-weekly.

The regime cross-tabulation showed that both components benefited from high volatility, but monthly retained materially stronger profit factors. In the low-volatility/uptrend bucket, monthly produced ₹87,181.54 while bi-weekly produced -₹39,868.56. These regime results are descriptive and were not used to optimize or filter the base strategy.

The completed Phase 7 walk-forward artifacts contain aggregate window summaries rather than component-level trade ledgers. Accordingly, no separate monthly/bi-weekly walk-forward attribution is claimed.

The full differential analysis is documented in `research/results/PHASE9_MONTHLY_BIWEEKLY_DIFFERENTIAL.md`.

## 11. Inference

Several findings are consistent across the research phases.

First, the deterministic reconstruction generated positive aggregate net P&L over a long historical period and retained positive realized P&L in each later chronological validation window.

Second, the adjustment mechanism was consistently negative in the historical reconstruction. The strategy's positive result was therefore not produced by profitable adjustments; it came primarily from target exits.

Third, performance is regime-dependent. High-volatility environments contributed substantially more P&L than low-volatility environments.

Fourth, entry convention matters materially. The same-close sensitivity reversed the aggregate outcome.

Fifth, the result is not solely dependent on 2020. Excluding 2020 left positive aggregate P&L, although substantially lower.

The statistical evidence remains limited by the deterministic nature of the reconstruction, daily-bar data, small chronological validation samples and dependence among observations.

---

## 12. Discussion

The findings are consistent with a strategy that can benefit from favorable option-pricing and volatility conditions while being vulnerable to adverse price movement and the timing of execution. The strong high-volatility performance is compatible with the broader literature on volatility premia and option-selling economics, but the study does not establish that the double calendar earns a stable variance-risk premium independently of other exposures.

The large 2020 contribution requires particular caution. It demonstrates that the strategy can produce very large modeled gains under a severe volatility regime, but those gains should not be extrapolated linearly into future expectations.

The adjustment result is especially important. The documented strategy treats adjustment as a risk-management response, yet in this reconstruction the adjustment trades were uniformly loss-making. This may mean that the cost of closing and redeploying after a break-even breach outweighs the subsequent benefits, or it may reflect limitations of the deterministic break-even approximation. The latter possibility cannot be ruled out without higher-frequency data and the source's original discretionary inputs.

The entry-time sensitivity provides another important limitation. Because the available data is daily, the exact intraday timing of entry and break-even confirmation cannot be reconstructed. A same-close convention produced a very different outcome from the next-open convention. This demonstrates that execution timing is not a minor implementation detail.

---

## 13. Strengths

1. Long historical period covering materially different market environments.
2. Separate monthly and bi-weekly structures.
3. Explicit transaction-cost and slippage model.
4. Historical lot-size and STT treatment.
5. Reproducible code and cached data pipeline.
6. Explicit error log and audit trail.
7. Bootstrap uncertainty analysis.
8. Sensitivity analysis rather than reliance on one parameter set.
9. Regime analysis using information available before entry.
10. Chronological out-of-sample validation after the base specification was frozen.

---

## 14. Limitations

1. The original strategy contains discretionary Greek, IV, OI and technical filters that cannot be reconstructed exactly.
2. Daily data cannot reproduce intraday fills, spreads, queue position or execution sequencing.
3. Third-party transformed historical datasets were used and require continued independent cross-checking against raw NSE archives.
4. The capital figure of ₹1.20 lakh is a research proxy, not a demonstrated broker margin requirement or complete capital-allocation model.
5. Overlapping trades and adjustment redeployments complicate simple return annualization.
6. Bootstrap intervals do not fully account for serial dependence or common market shocks.
7. The historical spot source ends before the requested July 28, 2026 end date.
8. Regime filters were descriptive and were not optimized or promoted into the base strategy.
9. The same-close sensitivity shows that execution convention can materially alter conclusions.
10. No live paper-trading or real-time execution validation was performed.

---

## 15. Conclusion

Under the deterministic reconstruction documented in this project, the NIFTY double-calendar framework generated positive aggregate net P&L from 2020 through the available 2026 data after modeled transaction costs and slippage.

The result was not confined entirely to 2020: excluding 2020 retained positive aggregate P&L, and the frozen specification generated positive realized P&L in each chronological 2023, 2024, 2025 and 2026 validation window.

However, the evidence should not be interpreted as proof of a stable future trading edge. The individual out-of-sample confidence intervals all included zero. Performance was strongly concentrated in high-volatility conditions, and the same-close entry convention produced a negative aggregate result.

The adjustment mechanism is the clearest negative component: all 39 reconstructed adjustment exits lost money, totaling approximately ₹42,150.

Therefore the most defensible empirical conclusion is:

> The documented double-calendar framework has a positive historical deterministic reconstruction under the frozen next-open execution convention, but its performance is materially regime- and execution-dependent, and the adjustment component is consistently loss-making in the available data.

This conclusion supports further controlled live/paper validation but does not establish guaranteed or stable future profitability.

---

## 16. Future Research

1. Obtain higher-frequency NSE option and index data to model intraday entry and exit.
2. Reconstruct bid/ask spreads rather than percentage slippage alone.
3. Reproduce the source's IV, delta, vega and OI filters numerically if their exact thresholds can be recovered.
4. Test volatility-regime filters strictly out-of-sample.
5. Investigate whether adjustment can be replaced by predefined risk exits without discretionary redeployment.
6. Cross-check selected trades directly against raw NSE contract-wise reports.
7. Model actual portfolio margin/collateral requirements and overlapping capital usage.
8. Evaluate overnight gap exposure explicitly.
9. Separate monthly and bi-weekly systems in future walk-forward portfolio tests.
10. Conduct paper-trading validation before any real-money deployment.

---

## Appendix A — Frozen Base Parameters

| Parameter | Value |
|---|---|
| Monthly target | ₹3,000/lot |
| Bi-weekly target | ₹1,600/lot |
| Entry | Next available scheduled trading-day open |
| ATM | Nearest listed strike |
| Slippage | 10 bps adverse per entry/exit |
| Brokerage | ₹10 per executed F&O order |
| Capital proxy | ₹1.20 lakh |
| Break-even | Deterministic Black–Scholes reconstruction |
| Research stop | After chronological validation and manuscript |

## Appendix B — Research Controls

Repository controls include:

- Research plan.
- Assumption register.
- Error log.
- Source notes.
- Literature notes.
- Data-source register.
- Cached-data manifests and hashes.
- Trade ledgers.
- GitHub Actions workflows.
- Phase-specific branches and merges.

## Appendix C — Reproducibility

The principal historical data hash is:

e4c6d2e1ddd2dbd9a7ab4c3be5460585ca5d8f0267123cd30b507cbbf6414bed

Historical backtest GitHub Actions run: 37023127851.

Phase 6 robustness workflow run: 37024072980.

Phase 7 chronological validation workflow run: 37025149087.

## Appendix D — Key Repository Outputs

- research/results/HISTORICAL_2020_2026_RESULTS.md
- research/results/PHASE6_ROBUSTNESS_RESULTS.md
- research/results/PHASE7_WALKFORWARD_RESULTS.md
- research/results/historical_summary.json
- research/results/figures/historical_net_pnl.svg
- research/results/figures/walkforward_net_pnl.svg
- .github/workflows/phase5_historical.yml
- .github/workflows/phase6_robustness.yml
- .github/workflows/phase6_regime.yml
- .github/workflows/phase7_walkforward.yml
