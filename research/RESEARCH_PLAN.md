# TM Trade 1 — Backtest Research Plan

## Research question
Does the NIFTY positional double-calendar framework described in the supplied strategy document produce positive risk-adjusted returns after realistic transaction costs, slippage, and execution constraints, across materially different market regimes?

## Source-derived strategy rules
The supplied document specifies:
- Strategy: ATM double calendar, i.e. sell near-expiry ATM call + put and buy the same-strike farther-expiry call + put.
- Monthly leg: after the prior monthly expiry, sell the new month's monthly straddle and buy the following month's monthly straddle.
- Monthly target: ₹3,000 per lot.
- Monthly holding period: normally 7 days, extend to Friday (about 7–10 days), then exit regardless of result.
- Bi-weekly leg: skip the current weekly expiry; sell the next expiry ATM straddle and buy the following expiry ATM straddle.
- Bi-weekly target: ₹1,600 per lot.
- Bi-weekly maximum holding period: 7 days / exit before the short leg becomes a weekly trade.
- Adjustment: if a break-even is breached with a convincing close outside it, close the whole position and redeploy a fresh double calendar at current spot; after roughly 7 days, prefer closure rather than adjustment.
- Monthly and bi-weekly cycles repeat through the year.
- The document explicitly notes that strike selection also depends on risk/reward, probability, delta, vega, IV, OI and technical factors, but the exact numerical thresholds are not specified.

## Backtest phases
### Phase 0 — Research specification and audit trail
Status: COMPLETE/INITIALIZED
Deliverables: plan, research status, error log, source reference, assumptions register.

### Phase 1 — Market-data acquisition
Status: COMPLETE
Data needed: NIFTY spot/index history; historical NIFTY option contracts for all required expiries/strikes; contract specifications; expiry calendar; lot-size history; contract changes; optional volatility/regime context.
Preferred sources: NSE historical derivatives data / bhavcopy archives; exchange-compatible public datasets; reputable open datasets / GitHub / Kaggle / Hugging Face.
Data should be cached rather than re-downloaded on every workflow run.

### Phase 2 — Deterministic strategy engine
Status: COMPLETE
Base test will use a fully reproducible execution convention: entry at the first available synchronized quote/bar after the scheduled entry date/time; ATM defined as strike nearest spot at entry; exit at target, adjustment event, or time-based exit; no look-ahead; complete four-leg position closed together.
Because the source leaves some choices discretionary, the engine will expose them as parameters rather than treating them as source facts.

### Phase 3 — Cost and execution model
Status: COMPLETE
Model brokerage, exchange transaction charges, GST, STT, stamp duty, SEBI/other statutory charges where applicable, bid/ask or configurable slippage, and adverse execution on gaps/fast markets. Paytm Money fee schedule must be verified before final net-return results are accepted.

### Phase 4 — Core backtest
Status: COMPLETE
Outputs: trade ledger; equity curve; monthly/annual returns; CAGR/annualized return; volatility; Sharpe/Sortino; maximum drawdown and duration; hit rate; average win/loss; expectancy; profit factor; exposure/capital utilization; adjustment frequency; gap-event behavior.

### Phase 5 — Robustness and sensitivity analysis
Status: NOT STARTED
Test variations of entry time, ATM definition / strike rounding, target thresholds, break-even confirmation rule, slippage, transaction cost, execution delay, regime filters, data source, and alternative strike-selection proxies where exact source thresholds are unavailable.

### Phase 6 — Out-of-sample / walk-forward validation
Status: NOT STARTED
Separate development and validation windows. Any parameter changes must be frozen before validation.

### Phase 7 — Research manuscript
Status: NOT STARTED
Include abstract; introduction; research questions; literature/research-data review; aims/objectives; methodology; statistical analysis; results; robustness; inference; discussion; strengths/limitations; conclusion; future research; tables; charts; appendices; supplements.

## Important interpretation rule
The supplied source itself says this is partly manual/discretionary and argues traditional backtesting is imperfect. Therefore results will be labeled as a deterministic approximation of the documented framework, not proof of the creator's exact live execution.

## Stop criterion
Research stops after Phase 6 and completion of Phase 7. It must produce a usable empirical conclusion and will not be extended indefinitely.

## Phase 9 extension — Monthly vs bi-weekly differential analysis
Status: COMPLETE
Reason: User explicitly requested a deeper differential analysis after completion of the original stop criterion.
Scope: Decompose the frozen reconstruction by monthly and bi-weekly component without changing entry convention, targets, costs, slippage or break-even logic. Report exit reasons, winner/loser distribution, holding period, costs, yearly/quarterly behavior and descriptive uncertainty.
No parameter optimization is permitted in this phase. The extension stops after the differential report is audited and committed; this condition has now been met.

## Versioning rule
Material changes to the proposed methodology require an explicit plan revision entry. Routine status/results updates do not alter the core plan.