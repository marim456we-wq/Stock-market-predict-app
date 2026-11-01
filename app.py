import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="TAPINU - Real Time", layout="wide")

# Auto Refresh Every 10 Seconds - Real Time
st.markdown("# 📈 TAPINU - REAL TIME LIVE PRICE")

# Stock Input
col_a, col_b = st.columns([2,1])
with col_a:
    symbol_input = st.text_input("Stock Symbol - Real Time", value="RELIANCE.NS", placeholder="RELIANCE.NS, TCS.NS, ^BSESN, AAPL, ZOMATO.NS")
with col_b:
    refresh_sec = st.selectbox("Auto Refresh", [5, 10, 30, 60], index=1)

symbol = symbol_input.strip().upper()
if symbol == "":
    symbol = "RELIANCE.NS"

# Quick Buttons
c1, c2, c3, c4, c5, c6 = st.columns(6)
if c1.button("RELIANCE"): symbol = "RELIANCE.NS"
if c2.button("TCS"): symbol = "TCS.NS"
if c3.button("SENSEX"): symbol = "^BSESN"
if c4.button("NIFTY"): symbol = "^NSEI"
if c5.button("ZOMATO"): symbol = "ZOMATO.NS"
if c6.button("AAPL"): symbol = "AAPL"

st.write(f"Live: {symbol} - Time: {datetime.now().strftime('%H:%M:%S')} - Auto Refresh {refresh_sec}s")

# REAL TIME DATA - 1 Day Intraday + 1 Year History
@st.cache_data(ttl=10)
def get_realtime(sym):
    ticker = yf.Ticker(sym)
    # Real time price - fast
    try:
        info = ticker.fast_info
        last_price = float(info.last_price)
    except:
        hist = ticker.history(period="1d", interval="1m")
        if len(hist) > 0:
            last_price = float(hist["Close"].iloc[-1])
        else:
            last_price = 0.0
    
    # Intraday today - 1 min
    intraday = ticker.history(period="1d", interval="1m")
    # 1 year daily for candle
    daily = ticker.history(period="1y", interval="1d")
    
    return last_price, intraday, daily

last_price, intraday_df, daily_df = get_realtime(symbol)

if len(daily_df) == 0:
    st.error("Data not found Sir - Symbol check pannunga")
    st.stop()

# Calculate Change
prev_close = float(daily_df["Close"].iloc[-2]) if len(daily_df) > 1 else last_price
change = last_price - prev_close
pct = (change / prev_close * 100) if prev_close != 0 else 0.0
is_up = change >= 0
color = "#26a69a" if is_up else "#ef5350"
arrow = "▲" if is_up else "▼"

# REAL TIME PRICE CARD - Big Display
st.markdown(f"""
<div style='background:{"#e8f5e9" if is_up else "#ffebee"}; border:2px solid {color}; padding:20px; border-radius:12px; text-align:center;'>
    <div style='font-size:14px; color:#6a6d78;'>REAL TIME LIVE - {symbol}</div>
    <div style='font-size:42px; font-weight:800; color:{color}; margin:10px 0;'>{round(last_price,2)} {arrow}</div>
    <div style='font-size:18px; font-weight:600; color:{color};'>{round(change,2)} ({round(pct,2)}%) {'YERUTHU' if is_up else 'YERANGUTHU'}</div>
    <div style='font-size:12px; color:#6a6d78; margin-top:8px;'>Last Update: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} IST | Auto Refresh {refresh_sec}s</div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# Metrics Row
m1, m2, m3, m4 = st.columns(4)
high_day = float(daily_df["High"].iloc[-1]) if len(daily_df) > 0 else last_price
low_day = float(daily_df["Low"].iloc[-1]) if len(daily_df) > 0 else last_price
open_day = float(daily_df["Open"].iloc[-1]) if len(daily_df) > 0 else last_price

m1.metric("Open Today", round(open_day,2))
m2.metric("High Today", round(high_day,2))
m3.metric("Low Today", round(low_day,2))
m4.metric("Prev Close", round(prev_close,2))

# TWO CHARTS - Real Time Intraday + Daily Candle
tab1, tab2 = st.tabs(["⚡ REAL TIME TODAY - 1 Min Live", "📊 Daily Candle - 1 Year"])

with tab1:
    if len(intraday_df) > 0:
        fig_live = go.Figure()
        fig_live.add_trace(go.Scatter(
            x=intraday_df.index,
            y=intraday_df["Close"],
            line=dict(color=color, width=2),
            fill="tozeroy",
            fillcolor=f"rgba({ '38,166,154' if is_up else '239,83,80'},0.2)",
            name="Live Price"
        ))
        fig_live.update_layout(
            height=400,
            title=f"{symbol} - Today Real Time - Last {round(last_price,2)}",
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(showgrid=True, gridcolor="#f0f3fa"),
            yaxis=dict(showgrid=True, gridcolor="#f0f3fa", side="right"),
            margin=dict(l=10, r=80, t=40, b=20)
        )
        st.plotly_chart(fig_live, use_container_width=True)
    else:
        st.write("Market closed Sir - Intraday data not available now Sir - Daily chart paarkalam Sir")

with tab2:
    daily_df["MA20"] = daily_df["Close"].rolling(20).mean()
    
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Candlestick(
        x=daily_df.index,
        open=daily_df["Open"],
        high=daily_df["High"],
        low=daily_df["Low"],
        close=daily_df["Close"],
        increasing_line_color="#26a69a",
        decreasing_line_color="#ef5350",
        name="Daily"
    ))
    fig_daily.add_trace(go.Scatter(
        x=daily_df.index,
        y=daily_df["MA20"],
        line=dict(color="#2962ff", width=1),
        name="MA20"
    ))
    fig_daily.update_layout(
        height=500,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_rangeslider_visible=False,
        xaxis=dict(showgrid=True, gridcolor="#f0f3fa"),
        yaxis=dict(showgrid=True, gridcolor="#f0f3fa", side="right")
    )
    st.plotly_chart(fig_daily, use_container_width=True)

# Auto Refresh Logic
st.markdown(f"""
<div style='background:#f0f3fa; padding:10px; border-radius:8px; text-align:center;'>
    🔄 Auto Refresh: Page ah {refresh_sec} second ku oru thadava refresh panna browser refresh button click pannunga Sir<br>
    Real Time ku Streamlit Cloud la manual refresh thaan best Sir - Market open la live price varum Sir
</div>
""", unsafe_allow_html=True)

# Manual Refresh Button
if st.button("🔄 Refresh Now - Live Price Update Pannunga Sir"):
    st.cache_data.clear()
    st.rerun()

st.caption(f"Real Time Live Price - {symbol} - {round(last_price,2)} - Auto Refresh {refresh_sec}s - TAPINU")

# Real time list
st.markdown("### 🌍 World Live Prices - Quick Watch")
watchlist = ["RELIANCE.NS", "TCS.NS", "^BSESN", "^NSEI", "ZOMATO.NS", "AAPL"]
live_data = []
for w_sym in watchlist:
    try:
        w_ticker = yf.Ticker(w_sym)
        w_price = float(w_ticker.fast_info.last_price)
        w_prev = w_ticker.history(period="2d")["Close"].iloc[-2] if len(w_ticker.history(period="2d")) > 1 else w_price
        w_chg = w_price - float(w_prev)
        w_pct = (w_chg / float(w_prev) * 100) if w_prev != 0 else 0
        live_data.append({"Symbol": w_sym, "Price": round(w_price,2), "Change": round(w_chg,2), "Pct%": round(w_pct,2)})
    except:
        pass

if live_data:
    st.dataframe(pd.DataFrame(live_data), use_container_width=True)
