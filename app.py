import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import pytz

st.set_page_config(page_title="TAPINU - PRO TradingView", layout="wide", page_icon="💎")

st.markdown("""
<style>
.main {background: white;}
.stApp {background: white;}
</style>
""", unsafe_allow_html=True)

ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

# TOP BAR LIKE SCREENSHOT - SENSEX + Icons
st.markdown("""
<div style='background:white; border-bottom:1px solid #e0e3eb; padding:8px 15px; display:flex; align-items:center; gap:15px; overflow-x:auto;'>
    <span style='background:#8b9a5c; color:white; width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold;'>S</span>
    <span style='background:#f0f3fa; padding:6px 15px; border-radius:20px; font-weight:600; color:#131722;'>SENSEX</span>
    <span style='font-size:18px;'>◍◍</span>
    <span style='font-size:18px; border:1px solid #e0e3eb; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center;'>+</span>
    <span style='font-weight:600;'>D</span>
    <span style='font-size:18px;'>◍◍</span>
    <span style='font-size:16px;'>📊 Ind</span>
</div>
""", unsafe_allow_html=True)

# MAIN LAYOUT - LEFT TOOLS + CHART
col_tools, col_chart = st.columns([0.7, 9.3])

with col_tools:
    st.markdown("""
    <div style='background:white; border-right:1px solid #e0e3eb; height:750px; display:flex; flex-direction:column; align-items:center; gap:18px; padding-top:15px;'>
        <div style='font-size:22px; color:#6a6d78; background:#f0f3fa; padding:8px; border-radius:6px;'>┼</div>
        <div style='font-size:20px; color:#6a6d78;'>╱</div>
        <div style='font-size:18px; color:#6a6d78;'>☰◍</div>
        <div style='font-size:18px; color:#6a6d78;'>◐◍</div>
        <div style='font-size:18px; color:#6a6d78;'>◍─</div>
        <div style='font-size:18px; color:#6a6d78;'>✎</div>
        <div style='font-size:20px; color:#6a6d78;'>T</div>
        <div style='font-size:18px; color:#6a6d78;'>☺</div>
        <div style='font-size:18px; color:#6a6d78;'>📏</div>
        <div style='font-size:18px; color:#6a6d78;'>⊕</div>
        <div style='font-size:18px; color:#6a6d78;'>🧲</div>
        <div style='font-size:18px; color:#6a6d78;'>✏️🔒</div>
        <div style='font-size:18px; color:#6a6d78;'>🔓</div>
        <div style='font-size:18px; color:#6a6d78;'>👁️</div>
        <div style='font-size:18px; color:#6a6d78;'>🗑️</div>
        <div style='font-size:18px; color:#6a6d78;'>◍</div>
    </div>
    """, unsafe_allow_html=True)

with col_chart:
    # TICKER SELECT
    ticker_list = {"S&P BSE SENSEX":"^BSESN","NIFTY 50":"^NSEI","RELIANCE":"RELIANCE.NS","TATA MOTORS":"TATAMOTORS.NS","TCS":"TCS.NS"}
    sel = st.selectbox("Select", list(ticker_list.keys()), index=0, label_visibility="collapsed")
    
    ticker = ticker_list[sel]
    
    @st.cache_data(ttl=60)
    def get_data(t):
        s = yf.Ticker(t)
        h = s.history(period="1y", interval="1d")
        return h
    
    hist = get_data(ticker)
    if hist.empty:
        st.stop()
    
    last = float(hist["Close"].iloc[-1])
    prev = float(hist["Close"].iloc[-2])
    chg = last - prev
    chg_pct = (chg/prev*100)
    
    # TOP INFO LIKE SCREENSHOT - SENSEX + BUY SELL BOXES
    st.markdown(f"""
    <div style='background:white; padding:10px 15px;'>
        <div style='display:flex; align-items:center; gap:8px;'>
            <span style='background:#0052CC; color:white; padding:2px 7px; border-radius:50%; font-size:11px; font-weight:bold;'>BSE</span>
            <span style='font-weight:700; font-size:16px; color:#131722;'>S&P BSE Sensex Index</span>
            <span style='background:#f0f3fa; padding:2px 10px; border-radius:12px; font-size:12px;'>- D</span>
            <span style='margin-left:auto; font-weight:600; color:#131722;'>75,750.00</span>
        </div>
        <div style='display:flex; align-items:center; gap:15px; margin-top:5px;'>
            <span style='color:{"#26a69a" if chg>=0 else "#ef5350"}; font-size:15px; font-weight:500;'>{round(last,2)} {'+' if chg>=0 else ''}{round(chg,2)} ({'+' if chg>=0 else ''}{round(chg_pct,2)}%)</span>
            <span style='margin-left:auto; font-weight:600;'>75,500.00</span>
        </div>
        <div style='display:flex; gap:10px; margin-top:8px;'>
            <div style='border:1px solid #ef5350; color:#ef5350; padding:5px 15px; border-radius:6px; text-align:center; font-size:12px; background:#fff0f0;'>
                <div>{round(last,2)}</div><div>SELL</div>
            </div>
            <div style='color:#6a6d78; font-size:12px; padding-top:10px;'>0.00</div>
            <div style='border:1px solid #2962ff; color:#2962ff; padding:5px 15px; border-radius:6px; text-align:center; font-size:12px; background:#f0f6ff;'>
                <div>{round(last,2)}</div><div>BUY</div>
            </div>
            <div style='margin-left:auto; font-weight:600; color:#6a6d78; font-size:14px;'>75,250.00<br><br>75,000.00</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # MAIN CHART WITH VOLUME - Like Screenshot
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.8, 0.2])
    
    # Candlestick
    fig.add_trace(go.Candlestick(
        x=hist.index,
        open=hist["Open"],
        high=hist["High"],
        low=hist["Low"],
        close=hist["Close"],
        increasing_line_color="#26a69a",
        increasing_fillcolor="#26a69a",
        decreasing_line_color="#ef5350",
        decreasing_fillcolor="#ef5350",
        name="Price"
    ), row=1, col=1)
    
    # Volume bars - bottom like screenshot
    colors = ["#26a69a" if c>=o else "#ef5350" for c,o in zip(hist["Close"], hist["Open"])]
    fig.add_trace(go.Bar(x=hist.index, y=hist["Volume"], marker_color=colors, name="Volume", opacity=0.6), row=2, col=1)
    
    fig.update_layout(
        height=650,
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        margin=dict(l=10, r=90, t=5, b=10),
        xaxis=dict(showgrid=True, gridcolor="#f0f3fa", rangeslider_visible=False, showticklabels=False),
        xaxis2=dict(showgrid=True, gridcolor="#f0f3fa", tickformat="%b", tickfont=dict(size=13, color="#131722", family="Arial Black")),
        yaxis=dict(side="right", showgrid=True, gridcolor="#f0f3fa", tickfont=dict(color="#131722", size=12, weight="bold"), showspikes=True),
        yaxis2=dict(side="right", showgrid=False, showticklabels=False),
        hovermode="x unified"
    )
    
    # Current price line green box like screenshot
    fig.add_hline(y=last, line_dash="dot", line_color="#9598a1", line_width=1, opacity=0.5, row=1, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Bottom bar like screenshot
    st.markdown(f"""
    <div style='background:white; border-top:1px solid #e0e3eb; padding:8px 15px; display:flex; justify-content:space-between; align-items:center; color:#6a6d78; font-size:13px;'>
        <span style='display:flex; align-items:center; gap:5px;'><span style='font-weight:bold; font-size:16px;'>↗</span> TradingView</span>
        <span style='background:#e0e3eb; padding:5px 10px; border-radius:12px; display:flex; gap:5px;'><span>⚡</span></span>
        <span style='background:#26a69a; color:white; padding:3px 10px; border-radius:4px;'>12.24 M</span>
    </div>
    <div style='background:white; border-top:1px solid #e0e3eb; padding:8px 15px; display:flex; justify-content:space-between; color:#6a6d78; font-size:13px;'>
        <span>Oct</span><span>Nov</span><span style='margin-left:auto;'></span>
    </div>
    <div style='background:#f8f9fd; border-top:1px solid #e0e3eb; padding:8px 15px; display:flex; justify-content:space-between; color:#131722; font-size:13px;'>
        <span>Date Range ▼</span>
        <span>{now.strftime('%H:%M:%S')} UTC+5:30</span>
    </div>
    """, unsafe_allow_html=True)
    
    # LONG TAP POPUP LIKE SCREENSHOT
    st.markdown("""
    <div style='background:#2962ff; color:white; padding:12px 15px; border-radius:8px; display:flex; align-items:center; gap:15px; margin-top:10px;'>
        <div style='
