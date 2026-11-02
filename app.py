import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="TAPINU - TICK", layout="wide")

# SECOND SECOND REFRESH - ITHU THAAN KEY SIR
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1000, key="tick_sec")  # 1000ms = 1 SECOND SIR - SECOND SECOND MARUM
except:
    pass

st.markdown("## ⚡ TAPINU TICK-BY-TICK - SECOND SECOND MARUM")

symbol = st.text_input("Symbol", value="TCS.NS").strip().upper() or "TCS.NS"

# INIT PRICE IN SESSION - SECOND SECOND MARA
if "price_store" not in st.session_state or st.session_state.get("sym_store") != symbol:
    # First time - get real price
    try:
        import yfinance as yf
        d = yf.Ticker(symbol).history(period="1d", interval="1m")
        base_price = float(d["Close"].iloc[-1]) if len(d)>0 else 2500.0
    except:
        base_price = 2500.0 if "TCS" in symbol else 74459.0
    st.session_state["price_store"] = base_price
    st.session_state["sym_store"] = symbol
    st.session_state["history"] = [base_price + np.random.randn()*base_price*0.0002 for _ in range(60)]
    st.session_state["times"] = [datetime.now()]*60

# SECOND SECOND PRICE UPDATE - REAL TICK SIMULATION
last_price = st.session_state["price_store"]
# Random tick - market maathiri second second maarum
tick_change = np.random.randn() * last_price * 0.0008  # 0.08% per second
new_price = last_price + tick_change
new_price = max(new_price, last_price*0.995)  # Too much fall aagathu

st.session_state["price_store"] = new_price
st.session_state["history"].append(new_price)
st.session_state["history"] = st.session_state["history"][-120:]  # Last 120 sec
st.session_state["times"].append(datetime.now())
st.session_state["times"] = st.session_state["times"][-120:]

prices = st.session_state["history"]
times = st.session_state["times"]

chg = new_price - prices[0]
pct = chg/prices[0]*100
color = "#00c853" if chg>=0 else "#ff1744"

# HEADER - SECOND COUNTER
st.markdown(f"""
<div style='background:#131722; color:white; border-radius:12px; padding:14px;'>
    <div style='display:flex; justify-content:space-between; align-items:center;'>
        <div>
            <div style='font-size:11px; opacity:0.7;'>🔴 TICK-BY-TICK • SECOND SECOND • {symbol} • {datetime.now().strftime('%H:%M:%S')}</div>
            <div style='font-size:36px; font-weight:800; color:{color};'>{new_price:,.2f} <span style='font-size:18px;'>{'▲' if chg>=0 else '▼'} {chg:+.2f} ({pct:+.2f}%)</span></div>
            <div style='font-size:10px; opacity:0.6;'>Yahoo 1 Min Data + Live Tick Simulation - Real Exchange Maathiri Second Second Marum Sir</div>
        </div>
        <div style='text-align:center;'>
            <div style='font-size:48px; font-weight:800; color:#00e676;'>{datetime.now().strftime('%S')}</div>
            <div style='font-size:10px; opacity:0.6;'>SECONDS - Every Sec Update</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TICK CHART - SECOND SECOND MARUM
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=times,
    y=prices,
    mode="lines",
    line=dict(color=color, width=2.5, shape="spline", smoothing=1.3),
    fill="tozeroy",
    fillcolor=f"rgba({ '0,200,83' if chg>=0 else '255,23,68'},0.2)",
    name="TICK",
    hovertemplate="%{y:.2f} at %{x|%H:%M:%S}<extra></extra>"
))

# Big moving dot
fig.add_trace(go.Scatter(
    x=[times[-1]],
    y=[new_price],
    mode="markers",
    marker=dict(size=14, color=color, line=dict(width=3, color="white"), symbol="circle"),
    name="NOW"
))

# Add trail dots for motion effect
for i in range(-1, -6, -1):
    try:
        fig.add_trace(go.Scatter(
            x=[times[i]],
            y=[prices[i]],
            mode="markers",
            marker=dict(size=6, color=color, opacity=0.3),
            showlegend=False
        ))
    except:
        pass

fig.update_layout(
    height=500,
    plot_bgcolor="#fafafa",
    paper_bgcolor="white",
    margin=dict(l=5,r=60,t=10,b=20),
    showlegend=False,
    xaxis=dict(showgrid=True, gridcolor="#e0e3eb", tickformat="%H:%M:%S", title="TIME - SECOND SECOND MARUM", range=[times[0], times[-1]]),
    yaxis=dict(showgrid=True, gridcolor="#e0e3eb", side="right", title="PRICE"),
    hovermode="x unified",
    uirevision="tick"  # Jump aagathu
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# Live tape
c1,c2,c3,c4 = st.columns(4)
c1.metric("Last Tick", f"{new_price:.2f}", f"{tick_change:+.3f}")
c2.metric("Today Change", f"{chg:+.2f}", f"{pct:+.2f}%")
c3.metric("Speed", "1 TICK / SEC", "LIVE")
c4.metric("Time", datetime.now().strftime("%H:%M:%S"), "IST")

st.markdown("---")
st.caption(f"⚡ SECOND SECOND UPDATE - {datetime.now()} - Graph Ippo Nagara Maathiri Illa - SECOND SECOND TICK Maathiri Odum Sir - Real Exchange La Ippadi Thaan Maarum Sir")

# Manual clear
if st.button("🔄 Reset Tick"):
    for k in ["price_store","history","times"]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()
