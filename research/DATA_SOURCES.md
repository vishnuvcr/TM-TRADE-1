# Data Sources and Validation Notes

## Primary market-data sources
### NSE India
- NSE publishes historical contract-wise derivatives archives and F&O bhavcopy/UDiFF data.
- NSE contract specifications confirm NIFTY 50 index options have Tuesday expiry; if Tuesday is a holiday, expiry moves to the previous trading day.
- NSE circular FAOP68747 (25-Jun-2025) documents the realignment of NIFTY index-option expiries to Tuesday.
- NSE circular FAOP70616 (03-Oct-2025) revised NIFTY market lot from 75 to 65 for new contracts.
- NSE circular FA73061 (27-Feb-2026) kept the total equity-option transaction charge at Rs. 3,553 per crore of traded premium value.

### Public third-party cache used for the core run
- Repository: `aaryan-say/nifty-options-delta-neutral-backtest`.
- File: `data/market_data.duckdb`.
- SHA-256 used by the successful run: `d0a07420b9981a94ef1960f7650196dbca730986852cb6515afa9c7f7b3a2694`.
- The third-party repository reports 71 NIFTY expiries through 28-Jul-2026 and daily OHLC coverage from March 2025.

## Broker / statutory costs
- Paytm Money current F&O FAQ: ₹10 brokerage per unique executed order.
- NSE STT page: option sale STT 0.10% through 31-Mar-2026 and 0.15% from 01-Apr-2026.
- NSE transaction-charge circular: ₹3,553 per crore of option premium value per side from 01-Mar-2026; total outflow remains at that level.
- Stamp duty and SEBI turnover fee are included in the cost model.

## Data limitations
The third-party daily dataset does not provide the historical bid/ask microstructure needed for an observed spread/slippage model. It also cannot reconstruct intraday order sequencing. The validation phase should therefore sample important trades against NSE archives and, where available, higher-frequency option data.

## Phase 5 historical sources

- `rissin/nse-options-intraday` — yearly NIFTY daily option Parquet files; dataset documentation states daily historical data derives from NSE F&O bhavcopy. https://huggingface.co/datasets/rissin/nse-options-intraday
- `thetrademarkk/india-index-options-1m` — NIFTY index Parquet used for spot OHLC reconstruction from 2021 onward. https://huggingface.co/datasets/thetrademarkk/india-index-options-1m
- `calender/indian-stock-hourly-2017-2021` — earlier NIFTY spot fallback. https://huggingface.co/datasets/calender/indian-stock-hourly-2017-2021
- NSE historical contract-wise F&O price/volume reports: https://www.nseindia.com/report-detail/fo_eq_security

The repository stores hashes/manifests and workflow cache identifiers rather than redistributing raw exchange-derived files.
