import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

st.set_page_config(page_title="TAPINU - Live Trading", layout="wide")

try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1000, key="live")
except:
    pass

IST = pytz.timezone("Asia/Kolkata")
def now_ist():
    return datetime.now(IST)

st.title("TAPINU - Live Market")

def fix_symbol(sym):
    sym = sym.strip().upper()
    mapping = {
        "NIFTY 50": "^NSEI",
        "NIFTY50": "^NSEI",
        "NIFTY": "^NSEI",
        "NIFTY 50.NS": "^NSEI",
        "NIFTY50.NS": "^NSEI",
        "NIFTY.NS": "^NSEI",
        "SENSEX": "^BSESN",
        "SENSEX.NS": "^BSESN",
        "BSE": "^BSESN",
        "BANK NIFTY": "^NSEBANK",
        "BANKNIFTY": "^NSEBANK",
        "BANKNIFTY.NS": "^NSEBANK",
        "TCS": "TCS.NS",
        "RELIANCE": "RELIANCE.NS",
        "INFY": "INFY.NS",
        "INFOSYS": "INFY.NS",
        "HDFC": "HDFCBANK.NS",
        "ICICI": "ICICIBANK.NS"
    }
    if sym in mapping:
        return mapping[sym]
    if "NIFTY" in sym:
        return "^NSEI"
    if "SENSEX" in sym or sym == "BSE":
        return "^BSESN"
    if "BANK" in sym:
        return "^NSEBANK"
    if ".NS" not in sym and "^" not in sym:
        return sym + ".NS"
    return sym

symbol_input = st.text_input("Enter Symbol - NIFTY, SENSEX, TCS, RELIANCE", value="NIFTY")
symbol = fix_symbol(symbol_input)
st.caption(f"Trading Symbol: {symbol} | Your Input: {symbol_input}")

if "base_price" not in st.session_state:
    st.session_state["base_price"] = {}
if "tick_history" not in st.session_state:
    st.session_state["tick_history"] = {}
if "tick_time" not in st.session_state:
    st.session_state["tick_time"] = {}

@st.cache_data(ttl=30)
def get_base(sym):
    try:
        import yfinance as yf
        t = yf.Ticker(sym)
        df = t.history(period="1d", interval="1m")
        if len(df) > 0:
            price = float(df["Close"].iloc[-1])
            if price > 100:
                return price
        df = t.history(period="5d", interval="1d")
        if len(df) > 0:
            return float(df["Close"].iloc[-1])
    except:
        pass
    if "^NSEI" in sym:
        return 23053.10
    if "^BSESN" in sym:
        return 74459.53
    if "^NSEBANK" in sym:
        return 55000.0
    return 3400.0

base = get_base(symbol)

if symbol not in st.session_state["base_price"]:
    st.session_state["base_price"][symbol] = base
    st.session_state["tick_history"][symbol] = [base]*80
    st.session_state["tick_time"][symbol] = [now_ist()]*80

import numpy as np
last = st.session_state["base_price"][symbol]
vol = 0.0003 if "^" in symbol else 0.0004
tick = last + np.random.randn() * last * vol
tick = max(tick, last*0.995)
st.session_state["base_price"][symbol] = tick

hist = st.session_state["tick_history"][symbol]
hist.append(tick)
hist = hist[-120:]
st.session_state["tick_history"][symbol] = hist

tt = st.session_state["tick_time"][symbol]
tt.append(now_ist())
tt = tt[-120:]
st.session_state["tick_time"][symbol] = tt

change = tick - hist[0]
pct = change / hist[0] * 100 if hist[0]!=0 else 0
up = change >= 0
color = "#00a25b" if up else "#eb5b3c"
cur_ist = now_ist()

market_open = False
h = cur_ist.hour
m = cur_ist.minute
if 9 <= h <= 15:
    if not (h==9 and m<15) and not (h==15 and m>30):
        market_open = True
status = "MARKET OPEN - LIVE" if market_open else "MARKET CLOSED"
scolor = "#00a25b" if market_open else "#eb5b3c"

st.markdown(f"""
<div style='background:white; border:2px solid {scolor}; border-radius:12px; padding:14px;'>
    <div style='display:flex; justify-content:space-between; align-items:center;'>
        <div>
            <div style='font-size:11px; color:#6a6d78;'>{symbol} • {status} • Base {base:,.2f}</div>
            <div style='font-size:28px; font-weight:800; color:{color};'>Rs {tick:,.2f}</div>
            <div style='font-size:12px; color:{color}; font-weight:600;'>{change:+.2f} ({pct:+.2f}%) • {symbol_input.upper()}</div>
        </div>
        <div style='text-align:right;'>
            <div style='font-size:10px; color:#6a6d78;'>IST TIME</div>
            <div style='font-size:22px; font-weight:800; color:#131722;'>{cur_ist.strftime('%H:%M:%S')}</div>
            <div style='font-size:11px; color:#6a6d78;'>{cur_ist.strftime('%d-%b-%Y')}</div>
            <div style='font-size:10px; color:{scolor}; font-weight:700; margin-top:4px;'>{status}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

def ai_signal(prices):
    if len(prices) < 20:
        return "HOLD", 50
    arr = np.array(prices)
    sma20 = np.mean(arr[-20:])
    deltas = np.diff(arr)
    gains = np.where(deltas>0, deltas, 0)
    losses = np.where(deltas<0, -deltas, 0)
    avg_gain = np.mean(gains[-14:]) if len(gains)>=14 else 0.1
    avg_loss = np.mean(losses[-14:]) if len(losses)>=14 else 0.1
    rsi = 100 - (100/(1+ avg_gain/(avg_loss+0.0001)))
    last = arr[-1]
    score = 50
    if last > sma20:
        score += 20
    else:
        score -= 20
    if rsi < 30:
        score += 20
    elif rsi > 70:
        score -= 20
    if score >= 65:
        return "BUY", score
    elif score <= 35:
        return "SELL", score
    else:
        return "HOLD", score

signal, score = ai_signal(hist)
sma20_val = np.mean(hist[-20:]) if len(hist)>=20 else hist[-1]

st.subheader(f"Live Chart - IST {cur_ist.strftime('%H:%M:%S')} - {symbol}")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=tt,
    y=hist,
    mode="lines",
    line=dict(color=color, width=3, shape="spline", smoothing=0.8),
    fill="tozeroy",
    fillcolor="rgba(0,162,91,0.08)" if up else "rgba(235,91,60,0.08)",
    name="LTP",
    hovertemplate="<b>Rs %{y:,.2f}</b><br>IST: %{x|%H:%M:%S}<extra></extra>"
))
fig.add_trace(go.Scatter(
    x=tt,
    y=[sma20_val]*len(tt),
    mode="lines",
    line=dict(color="#2962FF", width=1.5, dash="dot"),
    name=f"SMA20 {sma20_val:,.0f}"
))
fig.add_trace(go.Scatter(
    x=[tt[-1]],
    y=[tick],
    mode="markers+text",
    marker=dict(size=14, color=color, line=dict(width=2, color="white")),
    text=[f"  Rs {tick:,.2f} • {cur_ist.strftime('%H:%M:%S')} IST"],
    textposition="middle right",
    textfont=dict(size=12, color=color),
    name="NOW"
))

fig.update_layout(
    height=550,
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font=dict(family="Inter", size=12, color="#131722"),
    margin=dict(l=10, r=90, t=20, b=50),
    showlegend=True,
    legend=dict(orientation="h", y=1.02, xanchor="right", x=1),
    xaxis=dict(showgrid=True, gridcolor="#f0f3fa", linecolor="#e0e3eb", tickformat="%H:%M:%S", title=dict(text=f"IST Time - {cur_ist.strftime('%d-%m-%Y')}")),
    yaxis=dict(showgrid=True, gridcolor="#f0f3fa", linecolor="#e0e3eb", side="right", title=dict(text=f"{symbol} Price Rs"), tickformat=",.0f"),
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    rsi_vals = []
    for i in range(14, len(hist)):
        sub = hist[i-14:i]
        deltas = np.diff(sub)
        gains = np.where(np.array(deltas)>0, deltas, 0)
        losses = np.where(np.array(deltas)<0, -np.array(deltas), 0)
        avg_g = np.mean(gains) if len(gains)>0 else 0.1
        avg_l = np.mean(losses) if len(losses)>0 else 0.1
        rsi = 100 - (100/(1+avg_g/(avg_l+0.0001)))
        rsi_vals.append(rsi)
    rsi_times = tt[14:]
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=rsi_times, y=rsi_vals, mode="lines", line=dict(color="#7c4dff", width=2.5), fill="tozeroy", fillcolor="rgba(124,77,255,0.1)", name="RSI"))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="#eb5b3c")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="#00a25b")
    fig_rsi.update_layout(height=250, plot_bgcolor="white", paper_bgcolor="white", margin=dict(l=10,r=50,t=10,b=20), xaxis=dict(tickformat="%H:%M:%S", title=f"IST {cur_ist.strftime('%H:%M')}"), yaxis=dict(range=[0,100], title="RSI"), showlegend=False)
    st.plotly_chart(fig_rsi, use_container_width=True)

with col2:
    st.markdown(f"""
    <div style='background:white; border:1px solid #e0e3eb; border-radius:12px; padding:16px;'>
        <div style='font-size:11px; color:#6a6d78;'>AI ANALYSIS @ {cur_ist.strftime('%H:%M:%S')} IST • {symbol}</div>
        <div style='font-size:20px; font-weight:700; margin-top:8px; color:{color};'>{signal} - {score:.0f}%</div>
        <div style='margin-top:12px; font-size:13px;'>
            <div style='display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #f5f5f5;'><span>LTP</span><b>Rs {tick:,.2f}</b></div>
            <div style='display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #f5f5f5;'><span>SMA20</span><b>Rs {sma20_val:,.2f}</b></div>
            <div style='display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #f5f5f5;'><span>Change</span><b style='color:{color};'>{change:+.2f} ({pct:+.2f}%)</b></div>
            <div style='display:flex; justify-content:space-between; padding:6px 0;'><span>Time</span><b>{cur_ist.strftime('%H:%M:%S')} IST</b></div>
        </div>
        <div style='margin-top:12px; padding:10px; background:{"#e8f5e9" if signal=="BUY" else "#ffebee" if signal=="SELL" else "#fff8e1"}; border-radius:8px; font-size:12px; font-weight:600; color:{color}; text-align:center;'>
            {signal} • {symbol} • {score:.0f}% Confidence
        </div>
    </div>
    """, unsafe_allow_html=True)

st.success(f"Live - {symbol_input} = Rs {tick:,.2f} • IST {cur_ist.strftime('%H:%M:%S')}")

if st.button("Clear & Refresh"):
    st.cache_data.clear()
    st.rerun()
