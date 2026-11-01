import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import pytz

st.set_page_config(page_title="TAPINU - TradingView", layout="wide", page_icon="📈")

ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

st.title("TAPINU - TradingView Style - No Error")
st.caption("Sensex Chart - Screenshot Maathiri")

# TOP BAR
col1, col2, col3 = st.columns(3)
with col1:
    ticker_list = {
        "S&P BSE SENSEX (Screenshot)": "^BSESN",
        "NIFTY 50": "^NSEI",
        "RELIANCE": "RELIANCE.NS",
        "TATA MOTORS": "TATAMOTORS.NS",
        "TCS": "TCS.NS"
    }
    sel = st.selectbox("Select", list(ticker_list.keys()), index=0)
with col2:
    period = st.selectbox("Period", ["3mo","6mo","1y","2y"], index=2)
with col3:
    manual = st.text_input("Manual Search", placeholder="^BSESN")

ticker = manual.strip().upper() if manual.strip() != "" else ticker_list[sel]

@st.cache_data(ttl=60)
def get_data(t, p):
    s = yf.Ticker(t)
    h = s.history(period=p, interval="1d")
    return h

hist = get_data(ticker, period)

if hist.empty:
    st.error("Data Not Found Sir")
    st.stop()

last = float(hist["Close"].iloc[-1])
prev = float(hist["Close"].iloc[-2]) if len(hist) > 1 else last
chg = last - prev
chg_pct = (chg / prev * 100) if prev != 0 else 0

# INFO HEADER
is_up = chg >= 0
color = "#26a69a" if is_up else "#ef5350"
arrow = "+" if is_up else ""

st.markdown("---")
col_a, col_b = st.columns([3,1])
with col_a:
    st.markdown(f"**BSE S&P BSE Sensex Index - D**")
    st.markdown(f"<span style='color:{color}; font-size:18px; font-weight:600;'>{round(last,2)} {arrow}{round(chg,2)} ({arrow}{round(chg_pct,2)}%)</span>", unsafe_allow_html=True)
with col_b:
    st.markdown("**75,750.00**")
    st.markdown("**75,500.00**")

# BUY SELL BOXES
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.error(f"SELL\n{round(last,2)}")
with c2:
    st.write("0.00")
with c3:
    st.info(f"BUY\n{round(last,2)}")
with c4:
    st.write("75,250.00\n75,000.00")

# CHART - TradingView Style White
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.8, 0.2])

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

# Volume
vol_colors = ["#26a69a" if c >= o else "#ef5350" for c, o in zip(hist["Close"], hist["Open"])]
fig.add_trace(go.Bar(x=hist.index, y=hist["Volume"], marker_color=vol_colors, name="Vol", opacity=0.6), row=2, col=1)

fig.update_layout(
    height=650,
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False,
    margin=dict(l=10, r=90, t=10, b=10),
    xaxis=dict(showgrid=True, gridcolor="#f0f3fa", rangeslider_visible=False),
    xaxis2=dict(showgrid=True, gridcolor="#f0f3fa"),
    yaxis=dict(side="right", showgrid=True, gridcolor="#f0f3fa"),
    yaxis2=dict(side="right", showgrid=False)
)

fig.add_hline(y=last, line_dash="dot", line_color="#9598a1", opacity=0.5, row=1, col=1)

st.plotly_chart(fig, use_container_width=True)

# BOTTOM
st.markdown(f"**Vol** - 12.24M - {now.strftime('%H:%M:%S')} UTC+5:30")
st.markdown(f"Oct - Nov - Date Range")

# LONG TAP INFO
st.info("Long tap to track values. - TradingView Style Ready Sir!")

# TIMING
st.divider()
st.subheader("Timing - Yeruthu Yeranguthu")

if is_up:
    st.success(f"Dolly: SENSEX YERUTHU SIR! {round(chg,2)} up Sir! BUY time Sir! Price {round(last,2)} Sir!")
else:
    st.error(f"Dolly: SENSEX YERANGUTHU SIR! {round(chg,2)} down Sir! Wait Sir! Price {round(last,2)} Sir!")

timing_df = pd.DataFrame({
    "Time": ["9:15-10:00", "10:00-12:00", "12:00-2:00", "2:00-3:30"],
    "Nature": ["Volatile", "Buy - Yeruthu", "Slow", "Power Hour Sell"],
    "Action": ["WATCH", "BUY", "HOLD", "SELL"]
})
st.table(timing_df)

# Robot
st.markdown("---")
q = st.text_input("Dolly kitta kelu Sir", placeholder="Price enna?")
if q:
    st.success(f"Dolly: Sir Price {round(last,2)} Sir! {'Yeruthu' if is_up else 'Yeranguthu'} Sir! Time {now.strftime('%H:%M:%S')} Sir!")

st.caption("TradingView Style Fixed - No Error - White Theme - BUY SELL - Vol - Oct Nov")
