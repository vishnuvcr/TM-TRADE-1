#!/usr/bin/env python3
import argparse
from pathlib import Path
import duckdb, pandas as pd, numpy as np

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--db",required=True)
    ap.add_argument("--ledger",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()

    con=duckdb.connect(args.db,read_only=True)
    idx=con.execute("""SELECT date, close FROM bars
                       WHERE instrument_type='INDEX' AND underlying='NIFTY'
                       ORDER BY date""").fetchdf()
    idx["date"]=pd.to_datetime(idx["date"])
    idx=idx.set_index("date")
    idx["ret"]=idx["close"].pct_change()
    idx["rv20"]=idx["ret"].rolling(20).std()*np.sqrt(252)
    idx["trend20"]=idx["close"].pct_change(20)
    med=float(idx["rv20"].median())
    idx["vol_regime"]=np.where(idx["rv20"]>=med,"high_vol","low_vol")
    idx["trend_regime"]=np.where(idx["trend20"]>=0,"up_20d","down_20d")

    tr=pd.read_csv(args.ledger)
    tr["entry_date"]=pd.to_datetime(tr["entry_date"])
    tr["exit_date"]=pd.to_datetime(tr["exit_date"])
    tr=tr.merge(idx[["rv20","trend20","vol_regime","trend_regime"]],left_on="entry_date",right_index=True,how="left")
    tr["vol_regime"]=tr["vol_regime"].fillna("unknown")
    tr["trend_regime"]=tr["trend_regime"].fillna("unknown")

    def agg(g):
        x=g.net_pnl.astype(float)
        pos=x[x>0]; neg=x[x<0]
        return pd.Series({
            "trades":len(g),
            "net_pnl":x.sum(),
            "avg_net_pnl":x.mean(),
            "win_rate":(x>0).mean(),
            "profit_factor":pos.sum()/abs(neg.sum()) if len(neg) else np.nan,
            "adjustments":(g.exit_reason=="adjustment").sum(),
            "max_trade":x.max(),
            "min_trade":x.min()
        })
    vol=tr.groupby("vol_regime",dropna=False).apply(agg,include_groups=False).reset_index()
    trend=tr.groupby("trend_regime",dropna=False).apply(agg,include_groups=False).reset_index()
    joint=tr.groupby(["vol_regime","trend_regime"],dropna=False).apply(agg,include_groups=False).reset_index()

    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    tr.to_csv(out/"regime_trade_ledger.csv",index=False)
    vol.to_csv(out/"regime_volatility.csv",index=False)
    trend.to_csv(out/"regime_trend.csv",index=False)
    joint.to_csv(out/"regime_joint.csv",index=False)
    print("\nVOLATILITY\n",vol.to_string(index=False))
    print("\nTREND\n",trend.to_string(index=False))
    print("\nJOINT\n",joint.to_string(index=False))

if __name__=="__main__":
    main()
