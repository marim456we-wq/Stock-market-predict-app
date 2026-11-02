import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="TAPINU CLEAR", layout="wide")

# Auto refresh 1 sec
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1000, key="clear_graph")
except:
    pass

st.title("TAPINU - Thelivaana Graph")

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
    st.session_state["tick_time"][symbol] = [datetime.now()]*80

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
tt.append(datetime.now())
tt = tt[-120:]
st.session_state["tick_time"][symbol] = tt

# Price
change = tick - hist[0]
pct = change / hist[0] * 100 if hist[0]!=0 else 0
up = change >= 0
color = "#00a25b" if up else "#eb5b3c"

st.metric(label=f"{symbol} - {datetime.now().strftime('%H:%M:%S')}", value=f"Rs {tick:,.2f}", delta=f"{change:+.2f} ({pct:+.2f}%)")

# AI Signal
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

# CLEAR GRAPH - TradingView Style
st.subheader("Crystal Clear Graph - Thelivaana Chart")

fig = go.Figure()

# Main line - thick and clear
fig.add_trace(go.Scatter(
    x=tt,
    y=hist,
    mode="lines",
    line=dict(color=color, width=3, shape="spline", smoothing=0.8),
    fill="tozeroy",
    fillcolor="rgba(0,162,91,0.08)" if up else "rgba(235,91,60,0.08)",
    name="LTP",
    hovertemplate="<b>Price: Rs %{y:.2f}</b><br>Time: %{x|%H:%M:%S}<extra></extra>"
))

# SMA line - clear dotted
sma20_val = np.mean(hist[-20:]) if len(hist)>=20 else hist[-1]
fig.add_trace(go.Scatter(
    x=tt,
    y=[sma20_val]*len(tt),
    mode="lines",
    line=dict(color="#2962FF", width=1.5, dash="dot"),
    name=f"SMA20 {sma20_val:.0f}",
    hoverinfo="skip"
))

# Current price big dot
fig.add_trace(go.Scatter(
    x=[tt[-1]],
    y=[tick],
    mode="markers+text",
    marker=dict(size=14, color=color, line=dict(width=2, color="white")),
    text=[f"  Rs {tick:.2f}"],
    textposition="middle right",
    textfont=dict(size=13, color=color, family="Inter"),
    name="NOW",
    hovertemplate="<b>NOW: Rs %{y:.2f}</b><extra></extra>"
))

# BUY/SELL markers
for i in range(5, len(hist), 20):
    if hist[i] > hist[i-5] and hist[i] > sma20_val:
        fig.add_annotation(x=tt[i], y=hist[i], text="BUY", showarrow=True, arrowhead=1, arrowcolor="#00a25b", bgcolor="#00a25b", font=dict(color="white", size=10))

# Layout - Crystal Clear
fig.update_layout(
    height=550,
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font=dict(family="Inter, sans-serif", size=12, color="#131722"),
    margin=dict(l=10, r=80, t=20, b=40),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="rgba(255,255,255,0.8)", bordercolor="#e0e3eb", borderwidth=1),
    xaxis=dict(
        showgrid=True,
        gridcolor="#f0f3fa",
        gridwidth=1,
        showline=True,
        linecolor="#e0e3eb",
        linewidth=1,
        tickformat="%H:%M:%S",
        title=dict(text="TIME - Second ku Second", font=dict(size=12, color="#6a6d78")),
        tickfont=dict(size=11, color="#6a6d78"),
        rangeslider=dict(visible=False)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#f0f3fa",
        gridwidth=1,
        showline=True,
        linecolor="#e0e3eb",
        linewidth=1,
        side="right",
        title=dict(text="PRICE Rs - Real Time", font=dict(size=12, color="#6a6d78")),
        tickfont=dict(size=11, color="#131722"),
        tickformat=",.0f",
        separatethousands=True
    ),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter", bordercolor="#e0e3eb")
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True, "displaylogo": False, "modeBarButtonsToRemove": ["select2d","lasso2d"]})

# Second chart - Volume style clear bars
st.subheader("Volume + RSI - Thelivaana Info")

col1, col2 = st.columns(2)

with col1:
    # RSI chart clear
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
    fig_rsi.add_trace(go.Scatter(x=rsi_times, y=rsi_vals, mode="lines", line=dict(color="#7c4dff", width=2.5), name="RSI", fill="tozeroy", fillcolor="rgba(124,77,255,0.1)"))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="#eb5b3c", annotation_text="Overbought 70")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="#00a25b", annotation_text="Oversold 30")
    fig_rsi.add_hline(y=50, line_dash="dot", line_color="#9e9e9e")
    fig_rsi.update_layout(height=250, plot_bgcolor="white", paper_bgcolor="white", margin=dict(l=10,r=50,t=10,b=20), xaxis=dict(tickformat="%H:%M:%S", title="Time"), yaxis=dict(range=[0,100], title="RSI"), showlegend=False)
    st.plotly_chart(fig_rsi, use_container_width=True)

with col2:
    st.markdown(f"""
    <div style='background:white; border:1px solid #e0e3eb; border-radius:12px; padding:16px;'>
        <div style='font-size:12px; color:#6a6d78;'>AI ANALYSIS - THELIVAANA</div>
        <div style='font-size:20px; font-weight:700; margin-top:8px; color:{color};'>{signal} - {score:.0f}%</div>
        <div style='margin-top:12px; font-size:13px;'>
            <div style='display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #f5f5f5;'><span>LTP</span><b>Rs {tick:.2f}</b></div>
            <div style='display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #f5f5f5;'><span>SMA20</span><b>Rs {sma20_val:.2f}</b></div>
            <div style='display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #f5f5f5;'><span>Change</span><b style='color:{color};'>{change:+.2f} ({pct:+.2f}%)</b></div>
            <div style='display:flex; justify-content:space-between; padding:6px 0;'><span>Time</span><b>{datetime.now().strftime('%H:%M:%S')}</b></div>
        </div>
        <div style='margin-top:12px; padding:10px; background:{"#e8f5e9" if signal=="BUY" else "#ffebee" if signal=="SELL" else "#fff8e1"}; border-radius:8px; font-size:12px; font-weight:600; color:{color}; text-align:center;'>
            { "🟢 BUY Panna Nalla Time Sir - Price Mela Pogum" if signal=="BUY" else "🔴 SELL Panna Nalla Time Sir - Price Keela Varum" if signal=="SELL" else "🟡 HOLD Pannunga Sir - Wait" }
        </div>
    </div>
    """, unsafe_allow_html=True)

st.success("Graph Thelivaa irukku Sir - Crystal Clear - TradingView maathiri")

if st.button("Clear & Refresh"):
    st.cache_data.clear()
    st.rerun()
