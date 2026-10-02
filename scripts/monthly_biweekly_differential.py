#!/usr/bin/env python3
import argparse, json, math
from pathlib import Path
import pandas as pd
import numpy as np

def bootstrap_ci(x, n=5000, seed=42):
    x=np.asarray(x,dtype=float)
    if len(x)==0: return [None,None]
    rng=np.random.default_rng(seed)
    means=np.array([rng.choice(x,size=len(x),replace=True).mean() for _ in range(n)])
    return [float(np.quantile(means,.025)),float(np.quantile(means,.975))]

def metrics(df):
    if df.empty: return {"trades":0}
    x=df.net_pnl.astype(float); wins=x[x>0]; losses=x[x<0]
    eq=x.cumsum(); dd=eq-eq.cummax()
    return {
        "trades":int(len(df)),
        "wins":int((x>0).sum()),
        "losses":int((x<0).sum()),
        "win_rate":float((x>0).mean()),
        "gross_pnl":float(df.gross_pnl.sum()),
        "costs":float(df.costs.sum()),
        "net_pnl":float(x.sum()),
        "avg_net_pnl":float(x.mean()),
        "median_net_pnl":float(x.median()),
        "avg_winner":float(wins.mean()) if len(wins) else None,
        "avg_loser":float(losses.mean()) if len(losses) else None,
        "profit_factor":float(wins.sum()/abs(losses.sum())) if len(losses) else None,
        "max_drawdown":float(dd.min()),
        "avg_holding_days":float(pd.to_numeric(df.days_held).mean()),
        "adjustments":int((df.exit_reason=="adjustment").sum()),
        "bootstrap_95_ci_mean_net_pnl":bootstrap_ci(x),
    }

def group_metrics(df, col):
    out={}
    for k,g in df.groupby(col, dropna=False):
        out[str(k)] = metrics(g)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--ledger",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(args.ledger)
    df["entry_date"]=pd.to_datetime(df.entry_date)
    df["exit_date"]=pd.to_datetime(df.exit_date)
    df["year"]=df.exit_date.dt.year.astype(str)
    df["quarter"]=df.exit_date.dt.to_period("Q").astype(str)
    df["net_margin_on_gross"]=np.where(df.gross_pnl!=0,df.net_pnl/df.gross_pnl,np.nan)

    result={
      "scope":{
        "base_rules":"Current frozen engine: next-open entry, monthly target ₹3,000/lot, bi-weekly target ₹1,600/lot, 10 bps adverse slippage, historical cost model.",
        "purpose":"Differential decomposition; no parameter optimization.",
        "source_baseline":"Phase 5 historical report remains the 264-segment baseline; this extension reports the current engine output separately if its segment count differs."
      },
      "overall":metrics(df),
      "by_component":group_metrics(df,"kind"),
      "by_component_exit_reason":{},
      "by_component_year":{},
      "by_component_quarter":{},
      "by_exit_reason":group_metrics(df,"exit_reason")
    }
    for kind,g in df.groupby("kind"):
        result["by_component_exit_reason"][kind]=group_metrics(g,"exit_reason")
        result["by_component_year"][kind]=group_metrics(g,"year")
        result["by_component_quarter"][kind]=group_metrics(g,"quarter")

    # Cost and target-hit diagnostics.
    comp=[]
    for kind,g in df.groupby("kind"):
        target_n=(g.exit_reason=="target").sum()
        comp.append({
          "kind":kind,
          "target_exit_rate":float(target_n/len(g)),
          "adjustment_rate":float((g.exit_reason=="adjustment").mean()),
          "breakeven_exit_rate":float((g.exit_reason=="breakeven_exit").mean()),
          "time_exit_rate":float((g.exit_reason=="time_exit").mean()),
          "cost_as_pct_gross_abs":float(g.costs.sum()/abs(g.gross_pnl.sum())) if g.gross_pnl.sum()!=0 else None,
          "net_pnl_share_total":float(g.net_pnl.sum()/df.net_pnl.sum()) if df.net_pnl.sum()!=0 else None
        })
    result["component_diagnostics"]=comp

    # Statistical comparison of mean trade P&L (descriptive; no multiple-testing claim).
    if set(df.kind.dropna())=={"monthly","biweekly"}:
        m=df[df.kind=="monthly"].net_pnl.to_numpy()
        b=df[df.kind=="biweekly"].net_pnl.to_numpy()
        rng=np.random.default_rng(123)
        diffs=[]
        for _ in range(5000):
            diffs.append(rng.choice(m,size=len(m),replace=True).mean()-rng.choice(b,size=len(b),replace=True).mean())
        result["mean_trade_difference_monthly_minus_biweekly"]={
          "observed":float(m.mean()-b.mean()),
          "bootstrap_95_ci":[float(np.quantile(diffs,.025)),float(np.quantile(diffs,.975))]
        }

    Path(out/"differential_summary.json").write_text(json.dumps(result,indent=2))
    with open(out/"DIFFERENTIAL_ANALYSIS.md","w") as f:
        f.write("# Phase 9 — Monthly vs Bi-weekly Differential Analysis\n\n")
        f.write("This report decomposes the current frozen deterministic reconstruction by component. It does not optimize parameters or replace the historical baseline.\n\n")
        for kind in ["monthly","biweekly"]:
            g=df[df.kind==kind]
            if g.empty: continue
            f.write(f"## {kind.title()}\n\n")
            m=metrics(g)
            f.write(pd.DataFrame([m]).T.to_markdown(header=False)+"\n\n")
            f.write("### Exit reasons\n\n")
            f.write(pd.DataFrame(group_metrics(g,"exit_reason")).T.to_markdown()+"\n\n")
            f.write("### Year\n\n")
            f.write(pd.DataFrame(group_metrics(g,"year")).T.to_markdown()+"\n\n")
        f.write("## Direct differential\n\n")
        f.write(pd.DataFrame(result["component_diagnostics"]).to_markdown(index=False)+"\n\n")
        if "mean_trade_difference_monthly_minus_biweekly" in result:
            f.write("Mean net P&L per trade difference (monthly minus bi-weekly): **₹%.2f**; bootstrap 95%% interval ₹%.2f to ₹%.2f.\n" % (
                result["mean_trade_difference_monthly_minus_biweekly"]["observed"],
                result["mean_trade_difference_monthly_minus_biweekly"]["bootstrap_95_ci"][0],
                result["mean_trade_difference_monthly_minus_biweekly"]["bootstrap_95_ci"][1]))
        f.write("\n## Interpretation controls\n\n")
        f.write("- Results are descriptive and use the frozen current engine.\n- A positive component result is not evidence of future profitability.\n- The component comparison does not establish causality for volatility or regime effects.\n- Walk-forward component results require separate chronological runs and are reported separately if generated.\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__": main()
