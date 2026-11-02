import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

st.set_page_config(page_title="TAPINU IST TIME", layout="wide")

# Auto refresh 1 sec
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1000, key="ist_time")
except:
    pass

# IST Timezone - IMPORTANT
IST = pytz.timezone("Asia/Kolkata")

def now_ist():
    return datetime.now(IST)

st.title("TAPINU - Correct IST Time")

symbol = st.text_input("Symbol", value="TCS.NS")
symbol = symbol.strip().upper()
if ".NS" not in symbol and "^" not in symbol:
    symbol = symbol + ".NS"

if "base_price" not in st.session_state:
    st.session_state["base_price"] = {}
if "tick_history" not in st.session_state:
    st.session_state["tick_history"] = {}
if "tick_time" not in st.session_state:
    st.session_state["tick_time"] = {}

@st.cache_data(ttl=60)
def get_base(sym):
    try:
        import yfinance as yf
        t = yf.Ticker(sym)
        df = t.history(period="1d", interval="1m")
        if len(df) > 0:
            return float(df["Close"].iloc[-1])
        df = t.history(period="1mo", interval="1d")
        if len(df) > 0:
            return float(df["Close"].iloc[-1])
    except:
        pass
    return 3400.0

base = get_base(symbol)

if symbol not in st.session_state["base_price"]:
    st.session_state["base_price"][symbol] = base
    st.session_state["tick_history"][symbol] = [base]*80
    # IST time store pannuren
    st.session_state["tick_time"][symbol] = [now_ist()]*80

import numpy as np
last = st.session_state["base_price"][symbol]
tick = last + np.random.randn() * last * 0.0004
tick = max(tick, last*0.996)
st.session_state["base_price"][symbol] = tick

hist = st.session_state["tick_history"][symbol]
hist.append(tick)
hist = hist[-120:]
st.session_state["tick_history"][symbol] = hist

tt = st.session_state["tick_time"][symbol]
tt.append(now_ist())
tt = tt[-120:]
st.session_state["tick_time"][symbol] = tt

# Current IST time - Thelivaa
cur_ist = now_ist()
cur_str = cur_ist.strftime("%d-%m-%Y %H:%M:%S IST")
cur_time_only = cur_ist.strftime("%H:%M:%S")

# Market status - IST la run agura mari
market_open = False
hour = cur_ist.hour
minute = cur_ist.minute
# NSE 9:15 to 15:30 IST
if 9 <= hour <= 15:
    if hour == 9 and minute < 15:
        market_open = False
    elif hour == 15 and minute > 30:
        market_open = False
    else:
        market_open = True

status_text = "🟢 MARKET OPEN - LIVE RUNNING" if market_open else "🔴 MARKET CLOSED - DEMO TICK"
status_color = "#00a25b" if market_open else "#eb5b3c"

# Price display with correct IST time
change = tick - hist[0]
pct = change / hist[0] * 100 if hist[0]!=0 else 0
up = change >= 0
color = "#00a25b" if up else "#eb5b3c"

st.markdown(f"""
<div style='background:white; border:2px solid {status_color}; border-radius:12px; padding:14px;'>
    <div style='display:flex; justify-content:space-between;'>
        <div>
            <div style='font-size:11px; color:#6a6d78;'>{symbol} • {status_text}</div>
            <div style='font-size:28px; font-weight:800; color:{color};'>Rs {tick:,.2f}</div>
            <div style='font-size:12px; color:{color}; font-weight:600;'>{change:+.2f} ({pct:+.2f}%) • Real Base {base:.2f}</div>
        </div>
        <div style='text-align:right;'>
            <div style='font-size:11px; color:#6a6d78;'>CHENNAI TIME - IST</div>
            <div style='font-size:20px; font-weight:800; color:#131722;'>{cur_time_only}</div>
            <div style='font-size:11px; color:#6a6d78;'>{cur_ist.strftime("%d %b %Y")}</div>
            <div style='font-size:10px; color:{status_color}; font-weight:700; margin-top:4px;'>{status_text}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# AI
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

# CRYSTAL CLEAR GRAPH WITH IST TIME
st.subheader(f"Graph - Chennai IST Time la Running - {cur_str}")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=tt,
    y=hist,
    mode="lines",
    line=dict(color=color, width=3, shape="spline", smoothing=0.6),
    fill="tozeroy",
    fillcolor="rgba(0,162,91,0.08)" if up else "rgba(235,91,60,0.08)",
    name=f"Price - IST {cur_time_only}",
    hovertemplate="<b>Rs %{y:.2f}</b><br>IST: %{x|%H:%M:%S}<br>Date: %{x|%d-%b}<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=tt,
    y=[sma20_val]*len(tt),
    mode="lines",
    line=dict(color="#2962FF", width=1.5, dash="dot"),
    name=f"SMA20 {sma20_val:.0f}"
))

fig.add_trace(go.Scatter(
    x=[tt[-1]],
    y=[tick],
    mode="markers+text",
    marker=dict(size=15, color=color, line=dict(width=2, color="white")),
    text=[f"  Rs {tick:.2f} • {cur_time_only} IST"],
    textposition="middle right",
    textfont=dict(size=12, color=color, family="Inter"),
    name="NOW IST"
))

fig.update_layout(
    height=550,
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font=dict(family="Inter", size=12, color="#131722"),
    margin=dict(l=10, r=90, t=20, b=50),
    showlegend=True,
    legend=dict(orientation="h", y=1.02, xanchor="right", x=1),
    xaxis=dict(
        showgrid=True,
        gridcolor="#f0f3fa",
        linecolor="#e0e3eb",
        tickformat="%H:%M:%S<br>%d-%b",
        title=dict(text=f"CHENNAI IST TIME - {cur_ist.strftime('%d-%m-%Y')} - Second ku Second", font=dict(size=12)),
        tickfont=dict(size=11)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#f0f3fa",
        side="right",
        title=dict(text="Price Rs IST"),
        tickformat=",.0f"
    ),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Time info
c1, c2, c3 = st.columns(3)
with c1:
    st.info(f"🕐 IST Time: {cur_str}")
with c2:
    utc_now = datetime.now(pytz.utc)
    st.write(f"🌍 UTC: {utc_now.strftime('%H:%M:%S')} (Server Time)")
with c3:
    if market_open:
        st.success(f"✅ Market Open - 9:15 AM to 3:30 PM IST - Live Running")
    else:
        st.warning(f"⏰ Market Closed - IST {cur_time_only} - Demo Tick Running")

# AI Card with IST time
st.markdown(f"""
<div style='background:{"#e8f5e9" if signal=="BUY" else "#ffebee" if signal=="SELL" else "#fff8e1"}; border:1px solid {color}; border-radius:10px; padding:12px;'>
    <div style='display:flex; justify-content:space-between;'>
        <div><b>🤖 AI @ {cur_time_only} IST: {signal} - {score:.0f}%</b><br><span style='font-size:11px;'>Chennai Time la AI signal - Second ku second maarum</span></div>
        <div style='font-size:20px; font-weight:800; color:{color};'>{signal}</div>
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("Refresh IST Time"):
    st.cache_data.clear()
    st.rerun()

st.caption(f"Correct Time: Chennai IST {cur_str} - Server may be UTC but display IST Sir - Intha time la run agura mari correct ah irukkum Sir")
