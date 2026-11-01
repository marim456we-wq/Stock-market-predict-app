import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="TAPINU - TradingView Exact", layout="wide", page_icon="📈")

# TradingView Exact Style - No Extra
st.markdown("""
<style>
.main {background-color: white;}
.stApp {background-color: white;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h4 style='color:#131722; margin:0px;'>📈 TAPINU - TradingView Exact Chart</h4>", unsafe_allow_html=True)

# Simple Selector
col1, col2 = st.columns(2)
with col1:
    ticker_map = {
        "S&P BSE SENSEX": "^BSESN",
        "NIFTY 50": "^NSEI", 
        "RELIANCE": "RELIANCE.NS",
        "TATA MOTORS": "TATAMOTORS.NS",
        "TCS": "TCS.NS",
        "INFY": "INFY.NS"
    }
    sel_name = st.selectbox("Stock", list(ticker_map.keys()), index=0)
with col2:
    period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y"], index=3)

ticker = ticker_map[sel_name]

@st.cache_data(ttl=60)
def get_data(t, p):
    h = yf.Ticker(t).history(period=p, interval="1d")
    return h

df = get_data(ticker, period)

if df.empty:
    st.error("Data illa Sir")
    st.stop()

last = float(df["Close"].iloc[-1])
prev = float(df["Close"].iloc[-2]) if len(df) > 1 else last
chg = last - prev
pct = (chg/prev*100) if prev != 0 else 0

# Top like TradingView - BSE SENSEX
is_up = chg >= 0
c_color = "#26a69a" if is_up else "#ef5350"

st.markdown(f"""
<div style='background:white; border-bottom:1px solid #e0e3eb; padding:10px 0px;'>
    <span style='background:#2962ff; color:white; padding:2px 8px; border-radius:50%; font-size:11px; font-weight:bold;'>BSE</span>
    <span style='font-weight:700; font-size:16px; color:#131722; margin-left:8px;'>S&P BSE Sensex Index</span>
    <span style='background:#f0f3fa; padding:2px 8px; border-radius:10px; font-size:12px; color:#131722; margin-left:8px;'>- D</span>
    <br>
    <span style='color:{c_color}; font-size:15px; font-weight:500;'>{round(last,2)} {'+' if is_up else ''}{round(chg,2)} ({'+' if is_up else ''}{round(pct,2)}%)</span>
</div>
""", unsafe_allow_html=True)

# EXACT TRADINGVIEW CANDLE CHART - Clean
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df.index,
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"],
    increasing_line_color="#26a69a",
    increasing_fillcolor="#26a69a",
    decreasing_line_color="#ef5350",
    decreasing_fillcolor="#ef5350",
    whiskerwidth=0.2,
    name="Price"
))

fig.update_layout(
    height=600,
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis=dict(
        showgrid=True,
        gridcolor="#f0f3fa",
        gridwidth=1,
        rangeslider_visible=False,
        showspikes=False,
        tickfont=dict(color="#9598a1", size=11),
        linecolor="#e0e3eb",
        type="date"
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#f0f3fa",
        gridwidth=1,
        side="right",
        showspikes=True,
        spikemode="across",
        tickfont=dict(color="#131722", size=12),
        linecolor="#e0e3eb",
        tickformat=".2f"
    ),
    margin=dict(l=5, r=75, t=5, b=20),
    showlegend=False,
    hovermode="x unified",
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
)

# Last price dotted line
fig.add_hline(y=last, line_dash="dot", line_color="#9598a1", line_width=1, opacity=0.6)

st.plotly_chart(fig, use_container_width=True)

# Bottom like TradingView
st.markdown("""
<div style='background:white; border-top:1px solid #e0e3eb; padding:8px 0px; display:flex; justify-content:space-between; color:#9598a1; font-size:12px;'>
    <span>↗ TradingView</span>
    <span style='margin-left:auto;'>Date Range ▼</span>
</div>
""", unsafe_allow_html=True)

# Simple Info
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Last", round(last,2), f"{round(chg,2)} ({round(pct,2)}%)")
c2.metric("Open", round(float(df["Open"].iloc[-1]),2))
c3.metric("High", round(float(df["High"].iloc[-1]),2))
c4.metric("Low", round(float(df["Low"].iloc[-1]),2))

if is_up:
    st.success(f"YERUTHU SIR 📈 - {sel_name} {round(last,2)} - Green Candle Sir")
else:
    st.error(f"YERANGUTHU SIR 📉 - {sel_name} {round(last,2)} - Red Candle Sir")

st.caption("100% TradingView Exact - White BG - Green #26a69a - Red #ef5350 - Right Price Scale - Dotted Line")
