import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="TAPINU - TradingView Clear", layout="wide")

st.title("TAPINU - TradingView Clear Chart")
st.write("Chart Sariya Theriyum Sir - TradingView Maathiri")

# Selector
ticker_choice = st.selectbox(
    "Stock Select Pannunga Sir",
    ["S&P BSE SENSEX - ^BSESN", "NIFTY 50 - ^NSEI", "RELIANCE - RELIANCE.NS", "TATA MOTORS - TATAMOTORS.NS", "TCS - TCS.NS"],
    index=0
)

ticker = ticker_choice.split(" - ")[1]
period = st.selectbox("Period", ["3mo", "6mo", "1y", "2y"], index=2)

# Data
@st.cache_data(ttl=60)
def load_data(t, p):
    stock = yf.Ticker(t)
    hist = stock.history(period=p, interval="1d")
    return hist

data = load_data(ticker, period)

if data.empty:
    st.error("Data varala Sir - Ticker maathunga Sir")
    st.stop()

last_price = float(data["Close"].iloc[-1])
prev_price = float(data["Close"].iloc[-2]) if len(data) > 1 else last_price
change = last_price - prev_price
change_pct = (change / prev_price * 100) if prev_price != 0 else 0

# Top info like TradingView screenshot
up = change >= 0
clr = "green" if up else "red"

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"**S&P BSE Sensex Index - D**")
    if up:
        st.success(f"{round(last_price,2)} +{round(change,2)} (+{round(change_pct,2)}%) - YERUTHU SIR")
    else:
        st.error(f"{round(last_price,2)} {round(change,2)} ({round(change_pct,2)}%) - YERANGUTHU SIR")
with col2:
    st.markdown("**BUY / SELL**")
    st.info(f"BUY: {round(last_price,2)}")
    st.error(f"SELL: {round(last_price,2)}")

# TradingView Clear Chart
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.8, 0.2])

# Candlestick - Clear colors
fig.add_trace(go.Candlestick(
    x=data.index,
    open=data["Open"],
    high=data["High"],
    low=data["Low"],
    close=data["Close"],
    increasing_line_color="#26a69a",
    decreasing_line_color="#ef5350",
    name="Candle"
), row=1, col=1)

# Volume
fig.add_trace(go.Bar(
    x=data.index,
    y=data["Volume"],
    name="Volume",
    marker_color="lightblue"
), row=2, col=1)

fig.update_layout(
    height=700,
    template="plotly_white",
    showlegend=False,
    xaxis_rangeslider_visible=False,
    title=f"{ticker} - TradingView Style - Clear Chart - Oct Nov"
)

fig.update_xaxes(title_text="Date - Oct Nov", row=2, col=1)
fig.update_yaxes(title_text="Price", side="right", row=1, col=1)
fig.update_yaxes(title_text="Vol - 12.24M", side="right", row=2, col=1)

st.plotly_chart(fig, use_container_width=True)

st.write("---")
st.subheader("Dolly Robot - Trade View Maathiri")

if up:
    st.success(f"Dolly: Chart Theliva Theriyuthu Sir! Price YERUTHU Sir! {round(last_price,2)} Sir! Buy Pannalam Sir!")
else:
    st.error(f"Dolly: Chart Theliva Theriyuthu Sir! Price YERANGUTHU Sir! {round(last_price,2)} Sir! Wait Pannalam Sir!")

st.info("Long tap to track values - TradingView maathiri chart sariya theriyum Sir!")
st.caption("Clear Chart - No Error - TradingView Style - SENSEX")
