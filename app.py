import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# PRO CSS
st.set_page_config(page_title="TAPINU PRO - Trading Terminal", layout="wide", page_icon="💹")
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card { background: linear-gradient(135deg, #1f2937 0%, #111827 100%); padding:20px; border-radius:15px; border:1px solid #374151; }
    .buy-box { background: linear-gradient(135deg, #065f46 0%, #022c22 100%); padding:20px; border-radius:12px; border-left:5px solid #10b981; }
    .sell-box { background: linear-gradient(135deg, #7f1d1d 0%, #450a0a 100%); padding:20px; border-radius:12px; border-left:5px solid #ef4444; }
    h1 { font-weight:800; letter-spacing:-1px; }
</style>
""", unsafe_allow_html=True)

# HEADER
colh1, colh2 = st.columns([3,1])
with colh1:
    st.markdown("# 💹 TAPINU PRO TERMINAL")
    st.caption("BATCH-5 | Real-Time Market Intelligence | Institutional Grade")
with colh2:
    st.markdown("### 🟢 LIVE MARKET")

# SIDEBAR PRO
st.sidebar.markdown("## ⚙️ MARKET CONTROL")
ticker = st.sidebar.text_input("🔍 Search Global Asset", value="RELIANCE.NS", help="Ex: RELIANCE.NS, TCS.NS, AAPL, TSLA, BTC-USD, GC=F, NIFTY")
period_map = {"1 Month":"1mo","3 Months":"3mo","6 Months":"6mo","1 Year":"1y","2 Years":"2y","5 Years":"5y"}
period_label = st.sidebar.selectbox("📅 Timeframe", list(period_map.keys()), index=2)
period = period_map[period_label]
future_days = st.sidebar.slider("🔮 AI Forecast Days", 1, 30, 7)

st.sidebar.divider()
st.sidebar.markdown("### 💡 Quick Search")
st.sidebar.code("RELIANCE.NS | TCS.NS\nINFY.NS | HDFCBANK.NS\nAAPL | TSLA | BTC-USD\nGC=F Gold | NIFTY")

# DATA FETCH PRO
@st.cache_data(ttl=60)
def get_data(ticker, period):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    info = stock.info
    return hist, info

try:
    with st.spinner(f"Fetching {ticker} ..."):
        data, info = get_data(ticker, period)

    if data.empty:
        st.error(f"❌ {ticker} Not Found. Check Symbol Sir!")
        st.stop()

    # Metrics
    last = float(data["Close"].iloc[-1])
    prev = float(data["Close"].iloc[-2])
    change = last - prev
    pct = (change/prev)*100
    
    # Indicators
    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()
    data["MA200"] = data["Close"].rolling(200).mean()
    
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))
    
    ma20 = data["MA20"].iloc[-1]
    ma50 = data["MA50"].iloc[-1]
    rsi = data["RSI"].iloc[-1]
    volume = data["Volume"].iloc[-1]
    
    # BUY SELL LOGIC PRO
    score = 0
    reasons = []
    if last > ma20: 
        score+=1; reasons.append("Price > MA20 (Bullish)")
    else: 
        score-=1; reasons.append("Price < MA20 (Bearish)")
    if ma20 > ma50: 
        score+=1; reasons.append("MA20 > MA50 Golden Cross")
    else: 
        score-=1; reasons.append("MA20 < MA50 Death Cross")
    if rsi < 30: 
        score+=1; reasons.append(f"RSI {rsi:.1f} Oversold - Buy Zone")
    elif rsi > 70: 
        score-=1; reasons.append(f"RSI {rsi:.1f} Overbought - Sell Zone")
    else: 
        reasons.append(f"RSI {rsi:.1f} Neutral")

    # TOP METRICS
    m1,m2,m3,m4 = st.columns(4)
    m1.metric(f"{ticker} LIVE", f"
