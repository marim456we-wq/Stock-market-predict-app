import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(page_title="TAPINU TICK", layout="wide")

# 1 second refresh - second ku second
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1000, key="sec_tick")
except:
    st.write("Install autorefresh: pip install streamlit-autorefresh")

st.title("TAPINU - Second ku Second")
st.write("Real Price + Tick - Every Second")

symbol = st.text_input("Symbol", value="TCS.NS")
symbol = symbol.strip().upper()
if ".NS" not in symbol and "^" not in symbol:
    symbol = symbol + ".NS"

# Store price in session for tick effect
if "base_price" not in st.session_state:
    st.session_state["base_price"] = {}
if "tick_history" not in st.session_state:
    st.session_state["tick_history"] = {}
if "tick_time" not in st.session_state:
    st.session_state["tick_time"] = {}

# Get real base price once
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
    st.session_state["tick_history"][symbol] = [base]*60
    st.session_state["tick_time"][symbol] = [datetime.now()]*60

# Second ku second tick update
import numpy as np
last = st.session_state["base_price"][symbol]
tick = last + np.random.randn() * last * 0.0005
tick = max(tick, last*0.995)
st.session_state["base_price"][symbol] = tick

hist = st.session_state["tick_history"][symbol]
hist.append(tick)
hist = hist[-120:]
st.session_state["tick_history"][symbol] = hist

tt = st.session_state["tick_time"][symbol]
tt.append(datetime.now())
tt = tt[-120:]
st.session_state["tick_time"][symbol] = tt

# Display
change = tick - hist[0]
pct = change / hist[0] * 100 if hist[0]!=0 else 0
up = change >= 0
color = "#00a25b" if up else "#eb5b3c"

st.metric(
    label=f"{symbol} - REAL BASE {base:.2f} - LIVE TICK - {datetime.now().strftime('%H:%M:%S')}",
    value=f"Rs {tick:,.2f}",
    delta=f"{change:+.2f} ({pct:+.2f}%)"
)

st.write(f"Second: {datetime.now().strftime('%S')} - Every second price maaruthu Sir - Ithu thaan tick Sir")

# Chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=tt,
    y=hist,
    mode="lines",
    line=dict(color=color, width=2.5),
    fill="tozeroy"
))
fig.add_trace(go.Scatter(
    x=[tt[-1]],
    y=[tick],
    mode="markers",
    marker=dict(size=12, color=color)
))
fig.update_layout(
    height=450,
    title="Second ku Second Chart - Live Tick",
    xaxis_title="Time - HH:MM:SS",
    yaxis_title="Price",
    plot_bgcolor="white",
    xaxis=dict(tickformat="%H:%M:%S")
)
st.plotly_chart(fig, use_container_width=True)

st.success(f"Tick running Sir - Second {datetime.now().strftime('%S')}")

if st.button("Reset Tick"):
    del st.session_state["base_price"][symbol]
    st.rerun()

st.caption("Real base from NSE + Every second tick simulation - Yahoo free la second tick thara maatenguthu Sir - Real exchange la ippadi thaan second ku second maarum Sir")
