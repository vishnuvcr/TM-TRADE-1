#!/usr/bin/env python3
import os, hashlib, json
from pathlib import Path
import pandas as pd
import duckdb
from huggingface_hub import hf_hub_download

START = pd.Timestamp(os.environ.get("START_DATE", "2020-01-01"))
END = pd.Timestamp(os.environ.get("END_DATE", "2026-07-28"))
OUT = Path(os.environ.get("OUT_DB", "data/historical_2020_2026.duckdb"))
HF_TOKEN = os.environ.get("HF_TOKEN")

OPTION_REPO = "rissin/nse-options-intraday"
INDEX_REPO = "thetrademarkk/india-index-options-1m"
EARLY_SPOT_REPO = "calender/indian-stock-hourly-2017-2021"

def download_options(year):
    fn=f"historical_daily/NIFTY/NIFTY_{year}.parquet"
    return hf_hub_download(OPTION_REPO, fn, repo_type="dataset", token=HF_TOKEN)

def load_options():
    frames=[]
    for y in range(START.year, END.year+1):
        p=download_options(y)
        df=pd.read_parquet(p)
        df["date"]=pd.to_datetime(df["date"]).dt.normalize()
        df["expiry"]=pd.to_datetime(df["expiry"]).dt.normalize()
        df["strike"]=pd.to_numeric(df["strike"], errors="coerce")
        df=df[(df["underlying"]=="NIFTY") & (df["date"]>=START) & (df["date"]<=END)]
        df=df[df["option_type"].isin(["CE","PE"])]
        frames.append(df[["date","expiry","strike","option_type","open","high","low","close","volume","oi"]])
    return pd.concat(frames, ignore_index=True)

def load_spot():
    # 2021-05 onward: minute NIFTY index parquet.
    p=hf_hub_download(INDEX_REPO, "index/NIFTY.parquet", repo_type="dataset", token=HF_TOKEN)
    d=pd.read_parquet(p)
    d["timestamp"]=pd.to_datetime(d["timestamp"])
    d["date"]=d["timestamp"].dt.tz_localize(None).dt.normalize()
    d=d[(d["date"]>=max(START,pd.Timestamp("2021-05-27"))) & (d["date"]<=END)].sort_values("timestamp")
    spot=d.groupby("date").agg(open=("open","first"),high=("high","max"),low=("low","min"),close=("close","last")).reset_index()

    # 2017-2021 hourly fallback fills the period before 2021-05-27.
    if START < pd.Timestamp("2021-05-27"):
        files={
            "2020":"NIFTY_2017-2021.csv",
            "2021":"NIFTY_2017-2021.csv",
        }
        p2=hf_hub_download(EARLY_SPOT_REPO, files["2020"], repo_type="dataset", token=HF_TOKEN)
        e=pd.read_csv(p2)
        e["date"]=pd.to_datetime(e["date"]).dt.normalize()
        e=e[(e["date"]>=START)&(e["date"]<pd.Timestamp("2021-05-27"))]
        # Dataset contains multiple intraday observations; derive daily OHLC.
        for c in ["Open","High","Low","Close"]:
            e[c]=pd.to_numeric(e[c],errors="coerce")
        early=e.groupby("date").agg(open=("Open","first"),high=("High","max"),low=("Low","min"),close=("Close","last")).reset_index()
        spot=pd.concat([early,spot],ignore_index=True).drop_duplicates("date").sort_values("date")
    return spot

def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    opt=load_options()
    spot=load_spot()
    con=duckdb.connect(str(OUT))
    con.execute("DROP TABLE IF EXISTS bars")
    con.execute("""CREATE TABLE bars(
        instrument_type VARCHAR, underlying VARCHAR, date DATE, expiry DATE,
        strike DOUBLE, option_type VARCHAR, open DOUBLE, high DOUBLE, low DOUBLE,
        close DOUBLE, volume DOUBLE, oi DOUBLE)""")
    con.register("opt_df",opt)
    con.execute("""INSERT INTO bars
        SELECT 'OPT','NIFTY',date,expiry,strike,option_type,open,high,low,close,volume,oi
        FROM opt_df""")
    con.register("spot_df",spot)
    con.execute("""INSERT INTO bars
        SELECT 'INDEX','NIFTY',date,NULL,NULL,NULL,open,high,low,close,NULL,NULL
        FROM spot_df""")
    meta={
        "option_source_repo":OPTION_REPO,
        "index_source_repo":INDEX_REPO,
        "early_spot_source_repo":EARLY_SPOT_REPO,
        "start":str(START.date()),"end":str(END.date()),
        "option_rows":int(len(opt)),"spot_rows":int(len(spot)),
    }
    con.execute("DROP TABLE IF EXISTS metadata")
    con.execute("CREATE TABLE metadata(k VARCHAR,v VARCHAR)")
    for k,v in meta.items(): con.execute("INSERT INTO metadata VALUES (?,?)",[k,str(v)])
    con.close()
    sha=hashlib.sha256(OUT.read_bytes()).hexdigest()
    Path(str(OUT)+".sha256").write_text(sha+"  "+str(OUT.name)+"\n")
    Path("data/historical_manifest.json").write_text(json.dumps({**meta,"sha256":sha},indent=2))
    print(json.dumps({**meta,"sha256":sha},indent=2))

if __name__=="__main__":
    main()
