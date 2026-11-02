import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="TAPINU - LIVE MOVING", layout="wide")

# AUTO REFRESH - GRAPH NAGARA VAikkum
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=30000, key="live_refresh")  # 30 Sec ku Oru Vaati Auto Refresh - Graph Nagarum Sir
except:
    st.caption("Install pannunga Sir - Auto refresh ku")

st.markdown("## 🔴 TAPINU LIVE - Graph Nagara Maathiri")

symbol_input = st.text_input("Symbol", value="TCS.NS")
symbol = symbol_input.strip().upper() or "TCS.NS"

# LIVE DATA - 1 Minute Interval - Nagara Graph
@st.cache_data(ttl=20)  # 20 Sec Thaan Cache - Live Ku
def get_live_moving_data(sym):
    try:
        import yfinance as yf
        t = yf.Ticker(sym)
        # LIVE MOVING DATA - 1m ku
        intraday = t.history(period="1d", interval="1m")  # ITHU THAAN LIVE NAGARUM DATA SIR
        daily = t.history(period="3mo", interval="1d")
        if len(intraday) > 5:
            return intraday, daily, True, "LIVE MOVING"
        if len(daily) > 10:
            return daily.tail(100), daily, False, "Market Closed - Last Data"
    except Exception as e:
        pass
    # Fallback - Moving simulation
    dates = pd.date_range(end=datetime.now(), periods=100, freq='1min')
    base = 2500 if "TCS" in sym else 74459
    prices = base + np.cumsum(np.random.randn(100)*base*0.0005)
    df = pd.DataFrame({"Close":prices, "Open":prices*0.999, "High":prices*1.001, "Low":prices*0.999}, index=dates)
    return df, df, False, "SIMULATION - Yahoo Busy"

live_data, daily_data, is_live, status = get_live_moving_data(symbol)

last = float(live_data["Close"].iloc[-1])
prev = float(live_data["Close"].iloc[-2]) if len(live_data)>1 else last
chg = last-prev
pct = chg/prev*100 if prev!=0 else 0
color = "#00c853" if chg>=0 else "#ff1744"

# Price with LIVE dot
st.markdown(f"""
<div style='background:white; border:2px solid {color}; border-radius:12px; padding:14px;'>
    <div style='display:flex; justify-content:space-between; align-items:center;'>
        <div>
            <div style='font-size:12px; color:#6a6d78;'><span style='background:red; color:white; padding:2px 6px; border-radius:4px; animation: blink 1s infinite;'>● LIVE</span> {symbol} • {status} • {datetime.now().strftime('%H:%M:%S')}</div>
            <div style='font-size:32px; font-weight:800;'>{last:,.2f} <span style='font-size:16px; color:{color};'>{'▲' if chg>=0 else '▼'} {chg:+.2f} ({pct:+.2f}%)</span></div>
            <div style='font-size:11px; color:#9598a1;'>Graph 30 Sec ku Oru Vaati Auto Nagaram Sir - Page Refresh Panna Thevai Illa</div>
        </div>
        <div style='text-align:right;'><div style='font-size:11px; color:#9598a1;'>LAST UPDATE</div><div style='font-size:14px; font-weight:700; color:{color};'>{datetime.now().strftime('%H:%M:%S')}</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# MOVING CHART - Main
st.markdown("### 📈 LIVE MOVING CHART - Nagara Graph")

fig = go.Figure()

# Smooth animated line
fig.add_trace(go.Scatter(
    x=live_data.index,
    y=live_data["Close"],
    mode="lines",
    line=dict(color=color, width=2.5, shape="spline", smoothing=1),
    fill="tozeroy",
    fillcolor=f"rgba({ '0,200,83' if chg>=0 else '255,23,68'},0.15)",
    name="LIVE Price",
    hovertemplate="%{y:.2f}<extra></extra>"
))

# Last point big dot - moving effect
fig.add_trace(go.Scatter(
    x=[live_data.index[-1]],
    y=[last],
    mode="markers",
    marker=dict(size=12, color=color, line=dict(width=2, color="white")),
    name="Current"
))

fig.update_layout(
    height=450,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=5,r=60,t=10,b=20),
    showlegend=False,
    xaxis=dict(showgrid=True, gridcolor="#f0f3fa", tickformat="%H:%M:%S", title="Time - Live Moving"),
    yaxis=dict(showgrid=True, gridcolor="#f0f3fa", side="right"),
    hovermode="x unified",
    uirevision="live"  # ITHU IMPORTANT SIR - GRAPH JUMP AAGATHU - SMOOTH AH NAGARUM
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# Extra - Market Open Check
import pytz
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist)
market_open = 9 <= now_ist.hour < 16 and now_ist.weekday() < 5

if market_open and is_live:
    st.success(f"✅ Market OPEN Sir - {now_ist.strftime('%H:%M:%S')} IST - Graph Ippo Live Ah Nagarum Sir - 1 Min Data Sir")
else:
    st.warning(f"⏰ Market CLOSED Sir - {now_ist.strftime('%H:%M:%S')} IST - Monday to Friday 9:15 AM to 3:30 PM Thaan Live Nagarum Sir - Ippo Last Data Kaamikkuthu Sir")

if st.button("🔄 Ippo Udaney Graph A Attu - Manual Refresh"):
    st.cache_data.clear()
    st.rerun()

st.caption("TAPINU LIVE MOVING • 1 Minute Data • Auto Refresh 30 Sec • Market Hours 9:15-15:30 IST • Graph Smooth Ah Nagarum")
