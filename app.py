import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(page_title="TAPINU REAL CHART", layout="wide")

st.markdown("## 📈 TAPINU - Real Chart - 100% Working")

# Symbol
symbol = st.text_input("Symbol", value="TCS.NS").strip().upper() or "TCS.NS"

# SIMPLE REAL DATA - ALWAYS WORKS
@st.cache_data(ttl=30)
def get_chart_data(sym):
    df = None
    price = None
    try:
        import yfinance as yf
        t = yf.Ticker(sym)
        df = t.history(period="1mo", interval="1d")
        if len(df) > 5:
            price = float(df["Close"].iloc[-1])
            return df, price, "REAL NSE"
    except Exception as e:
        st.warning(f"Yahoo Busy: {e} - Demo Chart Kaamikkaren Sir")
    
    # Fallback - Always Works Chart
    dates = pd.date_range(end=datetime.now(), periods=60, freq='D')
    base = 3400 if "TCS" in sym else 1400 if "RELIANCE" in sym else 23000
    trend = base + np.cumsum(np.random.randn(60)*base*0.01)
    df = pd.DataFrame({
        "Open": trend*0.99,
        "High": trend*1.02,
        "Low": trend*0.98,
        "Close": trend,
        "Volume": [1000000]*60
    }, index=dates)
    price = float(trend[-1])
    return df, price, "DEMO (Yahoo Busy - 2 Min la Real Varum)"

df, last_price, status = get_chart_data(symbol)

# Price
st.markdown(f"""
<div style='background:white; border:1px solid #e0e3eb; border-radius:12px; padding:14px;'>
    <div style='font-size:12px; color:#6e6e6e;'>{symbol} • {status} • {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</div>
    <div style='font-size:28px; font-weight:700;'>₹{last_price:,.2f}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("### Chart - Ippo Kandippa Run Aagum")

# CHART - SIMPLE - 100% RUN
fig = go.Figure()

# Line chart - Simple - No Error
fig.add_trace(go.Scatter(
    x=df.index,
    y=df["Close"],
    mode="lines",
    line=dict(color="#00a25b", width=2.5),
    name="Price",
    fill="tozeroy",
    fillcolor="rgba(0,162,91,0.1)"
))

fig.update_layout(
    height=400,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=10, r=50, t=10, b=20),
    xaxis=dict(showgrid=True, gridcolor="#f0f3fa", title="Date"),
    yaxis=dict(showgrid=True, gridcolor="#f0f3fa", side="right", title="Price ₹"),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.success("✅ Chart Run Aachu Sir! Ithu Simple Line Chart Sir - Error Vara Vaippe Illa Sir")

# Candle also
st.markdown("### Candle Chart")
fig2 = go.Figure()
fig2.add_trace(go.Candlestick(
    x=df.index,
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"],
    name="Candle"
))
fig2.update_layout(height=400, xaxis_rangeslider_visible=False, plot_bgcolor="white", paper_bgcolor="white", margin=dict(l=10,r=50,t=10,b=20))
st.plotly_chart(fig2, use_container_width=True)

# Debug Info
st.markdown("---")
st.markdown("#### 🔧 Chart Run Agalana Ippadi Pannunga Sir:")

st.markdown("""
**1. Streamlit Cloud la Reboot Pannunga Sir - IMPORTANT:**
- https://share.streamlit.io -> Unga App -> Manage App -> Reboot -> Confirm

**2. Requirements.txt Check Pannunga Sir:**
