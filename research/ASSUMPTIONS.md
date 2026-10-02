# Assumptions Register

This file contains backtest operational assumptions that are NOT claimed to be explicit rules from the supplied strategy source.

## Current assumptions to test
- ATM = nearest listed strike to entry spot.
- Entry uses a reproducible market-data timestamp convention rather than discretionary manual timing.
- A target is measured on the complete four-leg position net P&L before costs, with net-of-cost P&L also reported.
- A break-even breach must be converted into a deterministic testable rule; primary implementation will use a close beyond the contemporaneous payoff break-even, with sensitivity tests for confirmation delays.
- Adjustment redeploys the full structure at current ATM after closure, preserving the relevant near/far expiry pattern.
- Where the source says "Tuesday" or "Friday", actual exchange trading dates/calendars will be used rather than assuming every calendar Tuesday/Friday is a trading day.

Each assumption may be revised only through an explicit plan revision and will be sensitivity-tested when material.
