# Phase 7 — Chronological Out-of-Sample Validation

## Frozen specification

Validation used the frozen Phase 6 base configuration:

- Monthly target: ₹3,000 per lot.
- Bi-weekly target: ₹1,600 per lot.
- Next-open entry convention.
- 10 bps adverse slippage.
- Historical statutory/brokerage cost model.
- Deterministic ATM and break-even reconstruction.
- No parameter selection from the validation windows.

## Results

| Test window | Trades | Winners | Net P&L | Profit factor | Max DD | Bootstrap 95% CI for mean trade P&L |
|---|---:|---:|---:|---:|---:|---:|
| 2023 | 35 | 16 | ₹1,340.00 | 1.08 | -₹6,494 | -₹426 to ₹496 |
| 2024 | 36 | 16 | ₹11,643.77 | 1.16 | -₹42,672 | -₹2,355 to ₹4,219 |
| 2025 | 40 | 22 | ₹90,745.06 | 2.72 | -₹14,769 | -₹300 to ₹5,760 |
| 2026 through Jul-02 | 12 | 4 | ₹17,879.89 | 2.01 | -₹14,603 | -₹2,688 to ₹6,573 |

Combined chronological validation:

- 123 reconstructed trade segments.
- Aggregate net P&L: **₹1,21,608.72**.
- Every test window had positive realized net P&L.
- None of the individual window bootstrap intervals excludes zero.
- 2024 was nearly flat relative to the other windows.
- The 2025 window contributed the largest validation-period P&L.

## Interpretation

The chronological results provide evidence that the positive historical result was not confined to 2020: every untouched 2023–2026 test window was positive under the frozen rules.

At the same time, the statistical evidence is weaker than the aggregate P&L alone suggests. Each yearly window is small, and every bootstrap interval includes zero. Therefore the validation supports **repeated positive realized outcomes under the reconstruction**, but it does not establish a precisely estimated positive expected trade return.

The 2024 result is particularly useful as a stress observation because the strategy remained slightly positive while its confidence interval was wide. This is consistent with a strategy whose outcome varies substantially across market regimes.

## Phase 7 conclusion

The frozen deterministic reconstruction passes the chronological realized-P&L check across all four validation windows, but the sample size within each window is too small for strong statistical inference. The research should therefore stop at an empirical conclusion rather than a claim of proven future profitability.

No further parameter optimization is performed after this point.
