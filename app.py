import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="TAPINU - Beautiful", layout="wide")

st.markdown("### 📈 TAPINU - Clean TradingView Chart")

symbol_input = st.text_input("Stock", value="TCS.NS")
symbol = symbol_input.strip().upper()
if symbol == "":
    symbol = "TCS.NS"

# Quick
c1, c2, c3, c4, c5 = st.columns(5)
if c1.button("TCS"): symbol = "TCS.NS"
if c2.button("RELIANCE"): symbol = "RELIANCE.NS"
if c3.button("SENSEX"): symbol = "^BSESN"
if c4.button("NIFTY"): symbol = "^NSEI"
if c5.button("ZOMATO"): symbol = "ZOMATO.NS"

# Get Data - No Cache Issue
ticker = yf.Ticker(symbol)
daily = ticker.history(period="6mo", interval="1d")
intraday = ticker.history(period="1d", interval="5m")

if len(daily) == 0:
    st.error("Data not found")
    st.stop()

last_price = float(daily["Close"].iloc[-1])
prev = float(daily["Close"].iloc[-2]) if len(daily) > 1 else last_price
change = last_price - prev
pct = (change/prev*100) if prev != 0 else 0
is_up = change >= 0
color = "#26a69a" if is_up else "#ef5350"

# BIG BEAUTIFUL PRICE CARD - Clean
st.markdown(f"""
<div style='background:white; border:1px solid #e0e3eb; border-radius:12px; padding:16px;'>
    <div style='display:flex; justify-content:space-between; align-items:center;'>
        <div>
            <div style='font-size:13px; color:#9598a1; font-weight:500;'>NSE • {symbol} • REAL TIME</div>
            <div style='font-size:32px; font-weight:700; color:#131722; margin-top:4px;'>{round(last_price,2)} <span style='font-size:20px; color:{color};'>{'▲' if is_up else '▼'} {round(change,2)} ({round(pct,2)}%)</span></div>
        </div>
        <div style='text-align:right;'>
            <div style='background:{color}; color:white; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:700;'>{'LIVE UP' if is_up else 'LIVE DOWN'}</div>
            <div style='font-size:11px; color:#9598a1; margin-top:6px;'>O {round(float(daily["Open"].iloc[-1]),2)} H {round(float(daily["High"].iloc[-1]),2)} L {round(float(daily["Low"].iloc[-1]),2)}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# BEAUTIFUL CHART - FIXED - NO CUT
fig = go.Figure()

# Candle - Clean
fig.add_trace(go.Candlestick(
    x=daily.index,
    open=daily["Open"],
    high=daily["High"],
    low=daily["Low"],
    close=daily["Close"],
    increasing_line_color="#26a69a",
    increasing_fillcolor="#26a69a",
    decreasing_line_color="#ef5350",
    decreasing_fillcolor="#ef5350",
    whiskerwidth=0.6,
    name="Price"
))

fig.update_layout(
    height=520,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=5, r=60, t=10, b=30),
    showlegend=False,
    xaxis=dict(
        showgrid=True,
        gridcolor="#f0f3fa",
        gridwidth=1,
        rangeslider_visible=False,
        showspikes=False,
        type="date",
        tickfont=dict(size=11, color="#9598a1"),
        linecolor="#e0e3eb"
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#f0f3fa",
        gridwidth=1,
        side="right",
        tickfont=dict(size=11, color="#131722"),
        linecolor="#e0e3eb",
        fixedrange=False
    ),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="white", bordercolor="#e0e3eb", font=dict(color="#131722"))
)

# Hide modebar icons overlapping - clean config
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False})

# INTRADAY BEAUTIFUL LINE CHART - NO CUT
if len(intraday) > 5:
    st.markdown(f"#### ⚡ Today Live - {symbol} - 5Min")
    
    fig2 = go.Figure()
    
    # Smooth line with gradient fill - beautiful
    fig2.add_trace(go.Scatter(
        x=intraday.index,
        y=intraday["Close"],
        mode="lines",
        line=dict(color=color, width=2.2, shape="spline", smoothing=0.8),
        fill="tozeroy",
        fillcolor=f"rgba({ '38,166,154' if is_up else '239,83,80'}, 0.12)",
        name="Live"
    ))
    
    fig2.update_layout(
        height=320,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=5, r=60, t=10, b=30),
        showlegend=False,
        xaxis=dict(
            showgrid=True,
            gridcolor="#f0f3fa",
            tickfont=dict(size=10, color="#9598a1"),
            linecolor="#e0e3eb",
            tickformat="%H:%M"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f0f3fa",
            side="right",
            tickfont=dict(size=11, color="#131722"),
            linecolor="#e0e3eb"
        ),
        hovermode="x",
        hoverlabel=dict(bgcolor="white", bordercolor="#e0e3eb")
    )
    
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# Refresh
if st.button("🔄 Refresh Live Price"):
    st.cache_data.clear()
    st.rerun()

st.caption("Beautiful Clean Chart - No Cut - TradingView Style - No Icons Overlap - Professional")
