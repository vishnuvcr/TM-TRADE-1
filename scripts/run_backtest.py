#!/usr/bin/env python3
import argparse, json, math, os, hashlib
from dataclasses import dataclass, asdict
from datetime import timedelta
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import norm

R = 0.065
Q = 0.0
SLIPPAGE_BPS = 10.0
LOT_OLD = 75
LOT_NEW = 65
LOT_CHANGE_DATE = pd.Timestamp("2026-01-06")
NSE_TXN = 0.0003553
SEBI_FEE = 0.000001
STAMP = 0.00003
GST = 0.18
BROKER_ORDER = 10.0
STT_OLD = 0.0010
STT_NEW = 0.0015

@dataclass
class Leg:
    expiry: pd.Timestamp
    strike: int
    opt: str
    side: int
    entry_date: pd.Timestamp
    entry_raw: float
    entry_exec: float

    def pnl(self, mark, lot):
        return self.side * (mark - self.entry_exec) * lot

def lot_size(d):
    return LOT_NEW if pd.Timestamp(d) >= LOT_CHANGE_DATE else LOT_OLD

def first_trading_on_or_after(days, d):
    x = pd.Timestamp(d)
    a = days[days >= x]
    return a[0] if len(a) else None

def next_trading(days, d):
    a = days[days > pd.Timestamp(d)]
    return a[0] if len(a) else None

def first_friday_on_or_after(days, d):
    x = pd.Timestamp(d)
    a = days[(days >= x) & (days.dayofweek == 4)]
    return a[0] if len(a) else None

def exec_price(raw, side):
    slip = SLIPPAGE_BPS / 10000.0
    return raw * (1 + slip) if side == 1 else raw * (1 - slip)

def bs_price(S, K, T, sigma, typ):
    if T <= 0:
        return max(S-K,0.0) if typ == "CE" else max(K-S,0.0)
    if sigma <= 1e-8:
        return max(S-K,0.0) if typ == "CE" else max(K-S,0.0)
    st = sigma * math.sqrt(T)
    d1 = (math.log(max(S,1e-12)/K) + (R-Q+0.5*sigma*sigma)*T) / st
    d2 = d1 - st
    if typ == "CE":
        return S*math.exp(-Q*T)*norm.cdf(d1) - K*math.exp(-R*T)*norm.cdf(d2)
    return K*math.exp(-R*T)*norm.cdf(-d2) - S*math.exp(-Q*T)*norm.cdf(-d1)

def implied_vol(price, S, K, T, typ):
    intrinsic = max(S-K,0.0) if typ=="CE" else max(K-S,0.0)
    if T <= 0:
        return 0.0001
    px = max(float(price), intrinsic + 1e-6)
    def f(sig):
        return bs_price(S,K,T,sig,typ)-px
    lo, hi = 1e-5, 5.0
    try:
        if f(hi) < 0:
            return 5.0
        return float(brentq(f, lo, hi, maxiter=100))
    except Exception:
        return 0.30

class Backtester:
    def __init__(self, db_path, start, end, entry_mode="next_open"):
        self.con = duckdb.connect(db_path, read_only=True)
        self.start = pd.Timestamp(start)
        self.end = pd.Timestamp(end)
        self.entry_mode = entry_mode
        self._cache = {}

        self.index = self.con.execute(
            """SELECT date, open, high, low, close
               FROM bars
               WHERE instrument_type='INDEX' AND underlying='NIFTY'
                 AND date BETWEEN ? AND ?
               ORDER BY date""", [self.start.date(), self.end.date()]
        ).fetchdf()
        self.index["date"] = pd.to_datetime(self.index["date"])
        self.index = self.index.set_index("date")
        self.days = self.index.index

        self.expiries = self.con.execute(
            """SELECT DISTINCT expiry
               FROM bars
               WHERE instrument_type='OPT' AND underlying='NIFTY'
                 AND expiry BETWEEN ? AND ?
               ORDER BY expiry""", [self.start.date(), (self.end + pd.Timedelta(days=120)).date()]
        ).fetchdf()["expiry"]
        self.expiries = pd.to_datetime(self.expiries).sort_values().reset_index(drop=True)
        self.monthly = self.expiries.to_frame(name="expiry")
        self.monthly["ym"] = self.monthly["expiry"].dt.to_period("M")
        self.monthly = self.monthly.groupby("ym", as_index=False)["expiry"].max()["expiry"].sort_values().reset_index(drop=True)

    def option_series(self, expiry, strike, opt):
        key = (pd.Timestamp(expiry), int(strike), opt)
        if key in self._cache:
            return self._cache[key]
        df = self.con.execute(
            """SELECT date, open, high, low, close
               FROM bars
               WHERE instrument_type='OPT' AND underlying='NIFTY'
                 AND expiry=? AND strike=? AND option_type=?
               ORDER BY date""", [pd.Timestamp(expiry).date(), int(strike), opt]
        ).fetchdf()
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date")
        self._cache[key] = df
        return df

    def common_atm_strike(self, date, near_exp, far_exp, spot):
        df = self.con.execute(
            """SELECT expiry, strike, option_type
               FROM bars
               WHERE instrument_type='OPT' AND underlying='NIFTY'
                 AND expiry IN (?,?) AND date=?
                 AND option_type IN ('CE','PE') AND open IS NOT NULL
               GROUP BY expiry, strike, option_type""",
            [pd.Timestamp(near_exp).date(), pd.Timestamp(far_exp).date(), pd.Timestamp(date).date()]
        ).fetchdf()
        if df.empty:
            return None
        sets = {}
        for ex in [pd.Timestamp(near_exp), pd.Timestamp(far_exp)]:
            s_ce = set(df[(df.expiry==ex.date()) & (df.option_type=="CE")]["strike"].astype(int))
            s_pe = set(df[(df.expiry==ex.date()) & (df.option_type=="PE")]["strike"].astype(int))
            sets[ex] = s_ce & s_pe
        common = sets[pd.Timestamp(near_exp)] & sets[pd.Timestamp(far_exp)]
        if not common:
            return None
        return int(min(common, key=lambda k: abs(k-float(spot))))

    def make_legs(self, entry_date, near_exp, far_exp, use_open=True):
        spot = float(self.index.loc[entry_date, "open" if use_open else "close"])
        k = self.common_atm_strike(entry_date, near_exp, far_exp, spot)
        if k is None:
            return None, "no_common_atm"
        legs=[]
        for exp in [near_exp, far_exp]:
            for opt in ["CE","PE"]:
                side = -1 if exp == near_exp else 1
                s = self.option_series(exp,k,opt)
                col = "open" if use_open else "close"
                if s.empty or entry_date not in s.index or pd.isna(s.loc[entry_date,col]):
                    return None, f"missing_entry_{exp.date()}_{k}_{opt}"
                raw=float(s.loc[entry_date,col])
                legs.append(Leg(pd.Timestamp(exp), k, opt, side, pd.Timestamp(entry_date), raw, exec_price(raw,side)))
        return legs, None

    def mark_position(self, legs, date):
        lot = lot_size(date)
        pnl=0.0
        for l in legs:
            s=self.option_series(l.expiry,l.strike,l.opt)
            if s.empty:
                return None
            sub=s[s.index<=date]
            if sub.empty:
                return None
            raw=float(sub.iloc[-1]["close"])
            pnl += l.pnl(raw, lot)
        return pnl

    def costs(self, legs, exit_date):
        # Costs are charged on each executed leg order at entry and exit.
        # Premium turnover is used for exchange/SEBI/stamp/STT.
        orders = 0
        cost = 0.0
        for l in legs:
            # Entry
            orders += 1
            v_in = abs(l.entry_exec) * lot_size(l.entry_date)
            cost += v_in * (NSE_TXN + SEBI_FEE)
            if l.side == 1:
                cost += v_in * STAMP
            else:
                cost += v_in * (STT_NEW if pd.Timestamp(l.entry_date)>=pd.Timestamp("2026-04-01") else STT_OLD)
            # Exit
            orders += 1
            s=self.option_series(l.expiry,l.strike,l.opt)
            raw=float(s[s.index<=exit_date].iloc[-1]["close"])
            v_out=abs(raw) * lot_size(exit_date)
            cost += v_out * (NSE_TXN + SEBI_FEE)
            if l.side == -1:
                cost += v_out * (STT_NEW if pd.Timestamp(exit_date)>=pd.Timestamp("2026-04-01") else STT_OLD)
            else:
                cost += v_out * STAMP
        brokerage = orders * BROKER_ORDER
        gst = GST * (brokerage + self.exchange_cost_basis(legs, exit_date))
        return cost + brokerage + gst

    def exchange_cost_basis(self, legs, exit_date):
        total=0.0
        for l in legs:
            v1=abs(l.entry_exec)*lot_size(l.entry_date)
            s=self.option_series(l.expiry,l.strike,l.opt)
            raw=float(s[s.index<=exit_date].iloc[-1]["close"])
            v2=abs(raw)*lot_size(exit_date)
            total += (v1+v2)*NSE_TXN
        return total

    def breakevens(self, legs, date):
        S=float(self.index.loc[date,"close"])
        params=[]
        for l in legs:
            s=self.option_series(l.expiry,l.strike,l.opt)
            if s.empty: return None
            row=s[s.index<=date]
            if row.empty: return None
            px=float(row.iloc[-1]["close"])
            T=max((pd.Timestamp(l.expiry)-pd.Timestamp(date)).days/365.0, 1/3650)
            iv=implied_vol(px,S,l.strike,T,l.opt)
            params.append((l.side,l.opt,l.strike,T,iv,l.entry_exec))
        def pnl_at(x):
            lot=lot_size(date)
            return sum(side*(bs_price(x,k,T,iv,opt)-entry)*lot for side,opt,k,T,iv,entry in params)
        grid=np.arange(max(0.5*S,S-0.25*S), 1.25*S, 25.0)
        vals=np.array([pnl_at(float(x)) for x in grid])
        roots=[]
        for i in range(len(grid)-1):
            a,b=grid[i],grid[i+1]
            fa,fb=vals[i],vals[i+1]
            if fa==0: roots.append(a)
            elif fa*fb<0:
                try: roots.append(brentq(pnl_at,a,b,maxiter=100))
                except Exception: pass
        roots=sorted(set(round(float(x),2) for x in roots))
        if len(roots)>=2:
            return roots[0], roots[-1]
        return None

    def run_segmented_trade(self, kind, near_exp, far_exp, entry_date, target, hard_end):
        rows=[]
        current_entry=pd.Timestamp(entry_date)
        segment_no=0
        adjust_limit = (current_entry + pd.Timedelta(days=7)) if kind=="monthly" else first_friday_on_or_after(self.days, current_entry+pd.Timedelta(days=1))
        while current_entry is not None and current_entry < hard_end:
            use_open = True
            legs, err=self.make_legs(current_entry,near_exp,far_exp,use_open=use_open)
            if legs is None:
                rows.append({"kind":kind,"segment":segment_no,"entry_date":str(current_entry.date()),"status":"SKIP","reason":err})
                return rows, current_entry, "data_gap"
            lot=lot_size(current_entry)
            prev_be=None
            exit_date=None
            exit_reason=None
            last_eval=current_entry
            eval_days=self.days[(self.days>=current_entry)&(self.days<=hard_end)]
            for d in eval_days[1:]:
                pnl=self.mark_position(legs,d)
                if pnl is None:
                    exit_date=d; exit_reason="data_gap"; break
                # Target first
                if pnl >= target:
                    exit_date=d; exit_reason="target"; break
                be=self.breakevens(legs,d)
                spot=float(self.index.loc[d,"close"])
                breached=False
                if be:
                    lo,hi=be
                    breached=(spot<lo or spot>hi)
                    prev_inside=True
                    if prev_be:
                        pspot=float(self.index.loc[last_eval,"close"])
                        prev_inside=(prev_be[0] <= pspot <= prev_be[1])
                    else:
                        prev_inside=True
                    breached = breached and prev_inside
                if breached:
                    if d <= adjust_limit and next_trading(self.days,d) is not None and next_trading(self.days,d) < hard_end:
                        exit_date=d; exit_reason="adjustment"; break
                    else:
                        exit_date=d; exit_reason="breakeven_exit"; break
                if d >= hard_end:
                    exit_date=d; exit_reason="time_exit"; break
                prev_be=be
                last_eval=d
            if exit_date is None:
                exit_date=eval_days[-1]
                exit_reason="time_exit"
            # gross and net
            raw_exit_prices={}
            gross=0.0
            for l in legs:
                s=self.option_series(l.expiry,l.strike,l.opt)
                raw=float(s[s.index<=exit_date].iloc[-1]["close"])
                raw_exit_prices[(l.expiry.date(),l.strike,l.opt)]=raw
                gross += l.pnl(raw, lot)
            costs=self.costs(legs,exit_date)
            net=gross-costs
            rows.append({
                "kind":kind,"segment":segment_no,
                "entry_date":str(current_entry.date()),"exit_date":str(exit_date.date()),
                "near_expiry":str(pd.Timestamp(near_exp).date()),"far_expiry":str(pd.Timestamp(far_exp).date()),
                "strike":int(legs[0].strike),"lot_size":int(lot),
                "gross_pnl":round(gross,2),"costs":round(costs,2),"net_pnl":round(net,2),
                "exit_reason":exit_reason,"days_held":int((exit_date-current_entry).days),
            })
            if exit_reason=="adjustment":
                new_entry=next_trading(self.days,exit_date)
                if new_entry is None or new_entry>=hard_end:
                    return rows, exit_date, "adjustment_no_reentry"
                current_entry=new_entry
                segment_no += 1
                # New segment target resets, but the original hard deadline does not.
                adjust_limit=(current_entry + pd.Timedelta(days=7)) if kind=="monthly" else first_friday_on_or_after(self.days,current_entry+pd.Timedelta(days=1))
                continue
            return rows, exit_date, exit_reason
        return rows, current_entry, "no_entry"

    def run(self):
        trades=[]
        for i in range(len(self.monthly)-2):
            m0,m1,m2=self.monthly.iloc[i],self.monthly.iloc[i+1],self.monthly.iloc[i+2]
            if m1 < self.start or m0 > self.end: continue
            monthly_entry=next_trading(self.days,m0)
            if monthly_entry is None or monthly_entry>self.end: continue
            hard=first_friday_on_or_after(self.days,monthly_entry+pd.Timedelta(days=7))
            if hard is None: continue
            hard=min(hard,self.end)
            rs, exit_day, _=self.run_segmented_trade("monthly",m1,m2,monthly_entry,3000.0,hard)
            trades.extend(rs)
            if not rs or not exit_day: continue

            cursor=next_trading(self.days,exit_day)
            next_monthly=m1
            while cursor is not None and cursor < next_monthly and cursor<=self.end:
                fut=[x for x in self.expiries if x>cursor]
                if len(fut)<3: break
                near,far=fut[1],fut[2]
                dte=(pd.Timestamp(near)-pd.Timestamp(cursor)).days
                if dte < 9 or dte > 18: break
                hard_b=first_trading_on_or_after(self.days,cursor+pd.Timedelta(days=7))
                if hard_b is None: break
                # Do not allow a time exit on/after the next monthly expiry.
                if hard_b>=next_monthly:
                    hard_b=first_trading_on_or_after(self.days,next_monthly-pd.Timedelta(days=1))
                    if hard_b is None or hard_b<=cursor: break
                rs, b_exit, _=self.run_segmented_trade("biweekly",near,far,cursor,1600.0,hard_b)
                trades.extend(rs)
                if not rs or not b_exit: break
                cursor=next_trading(self.days,b_exit)
        df=pd.DataFrame(trades)
        if not df.empty:
            df=df[df.status!="SKIP"] if "status" in df.columns else df
        return df

def bootstrap_ci(x, n=2000, seed=42):
    x=np.asarray(x,dtype=float)
    if len(x)==0: return [None,None,None]
    rng=np.random.default_rng(seed)
    means=np.empty(n)
    for i in range(n):
        means[i]=rng.choice(x,size=len(x),replace=True).mean()
    return [float(np.mean(x)),float(np.quantile(means,0.025)),float(np.quantile(means,0.975))]

def summarize(df):
    if df.empty:
        return {"trades":0}
    x=df["net_pnl"].astype(float)
    wins=x[x>0]; losses=x[x<0]
    eq=x.cumsum()
    dd=eq-eq.cummax()
    daily=df.groupby("exit_date")["net_pnl"].sum().sort_index()
    if len(daily)>=2:
        ret=daily/120000.0
        sharpe=float(ret.mean()/ret.std(ddof=1)*math.sqrt(252)) if ret.std(ddof=1)>0 else None
        downside=ret[ret<0].std(ddof=1)
        sortino=float(ret.mean()/downside*math.sqrt(252)) if downside and not math.isnan(downside) else None
    else:
        sharpe=sortino=None
    months=df.assign(month=pd.to_datetime(df["exit_date"]).dt.to_period("M")).groupby("month")["net_pnl"].sum()
    return {
        "trades":int(len(df)),
        "wins":int((x>0).sum()),
        "losses":int((x<0).sum()),
        "win_rate":float((x>0).mean()),
        "total_net_pnl":float(x.sum()),
        "avg_net_pnl":float(x.mean()),
        "median_net_pnl":float(x.median()),
        "profit_factor":float(wins.sum()/abs(losses.sum())) if len(losses) else None,
        "max_drawdown":float(dd.min()),
        "max_drawdown_pct_on_120k":float(dd.min()/120000.0),
        "sharpe_proxy":sharpe,
        "sortino_proxy":sortino,
        "bootstrap_mean_ci":bootstrap_ci(x),
        "worst_trade":float(x.min()),
        "best_trade":float(x.max()),
        "avg_holding_days":float(pd.to_numeric(df["days_held"]).mean()),
        "adjustments":int((df["exit_reason"]=="adjustment").sum()),
        "monthly_return_min":float(months.min()/120000.0) if len(months) else None,
        "monthly_return_max":float(months.max()/120000.0) if len(months) else None,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--db", default="data/market_data.duckdb")
    ap.add_argument("--start", default="2025-09-01")
    ap.add_argument("--end", default="2026-07-28")
    ap.add_argument("--out", default="results")
    ap.add_argument("--entry-mode", default="next_open")
    args=ap.parse_args()

    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    p=Path(args.db)
    manifest={"db":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None}
    Path(out/"data_manifest.json").write_text(json.dumps(manifest,indent=2))

    bt=Backtester(args.db,args.start,args.end,args.entry_mode)
    df=bt.run()
    if df.empty:
        raise SystemExit("No trades could be reconstructed from available data.")
    df.to_csv(out/"trade_ledger.csv",index=False)

    summary=summarize(df)
    summary["period_start"]=args.start
    summary["period_end"]=args.end
    summary["entry_mode"]=args.entry_mode
    summary["slippage_bps"]=SLIPPAGE_BPS
    summary["nse_option_txn_pct"]=NSE_TXN*100
    summary["sebi_fee_pct"]=SEBI_FEE*100
    summary["stamp_pct_buy"]=STAMP*100
    summary["stt_pct_sell_through_2026_03_31"]=STT_OLD*100
    summary["stt_pct_sell_from_2026_04_01"]=STT_NEW*100
    summary["brokerage_per_order"]=BROKER_ORDER
    summary["capital_proxy"]=120000
    Path(out/"summary.json").write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
    print("\nTRADES")
    print(df.to_string(index=False))

if __name__=="__main__":
    main()
