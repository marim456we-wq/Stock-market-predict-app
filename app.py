import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="TAPINU PRO", layout="wide")
st.title("TAPINU PRO TERMINAL")
st.caption("BATCH-5 Professional")
st.divider()

st.sidebar.title("MARKET CONTROL")
ticker = st.sidebar.text_input("Search Stock", value="RELIANCE.NS")
period = st.sidebar.selectbox("Period", ["1mo","3mo","6mo","1y"], index=2)
days = st.sidebar.slider("Forecast", 1, 20, 7)

@st.cache_data(ttl=60)
def get_data(t, p):
    s = yf.Ticker(t)
    h = s.history(period=p)
    return h

try:
    data = get_data(ticker, period)
    if data.empty:
        st.error("Not Found")
        st.stop()
    
    last = float(data["Close"].iloc[-1])
    prev = float(data["Close"].iloc[-2])
    ch = last - prev
    pct = (ch/prev)*100
    
    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))
    
    ma20 = data["MA20"].iloc[-1]
    ma50 = data["MA50"].iloc[-1]
    rsi = data["RSI"].iloc[-1]
    
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("LIVE PRICE", round(last,2), str(round(pct,2))+"%")
    c2.metric("MA20", round(ma20,2))
    c3.metric("MA50", round(ma50,2))
    c4.metric("RSI", round(rsi,2))
    
    if last > ma20 and ma20 > ma50:
        st.success("BUY SIGNAL - " + ticker + " STRONG BUY")
        st.balloons()
    elif last < ma20:
        st.error("SELL SIGNAL - " + ticker + " SELL")
    else:
        st.warning("HOLD - " + ticker)
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index, open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"]))
    fig.add_trace(go.Scatter(x=data.index, y=data["MA20"], line=dict(color="blue"), name="MA20"))
    fig.add_trace(go.Scatter(x=data.index, y=data["MA50"], line=dict(color="red"), name="MA50"))
    fig.update_layout(height=500, template="plotly_dark", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("AI Prediction")
    dr = data.reset_index()
    dr["D"] = range(len(dr))
    X = np.array(dr["D"]).reshape(-1,1)
    y = dr["Close"].values
    m = LinearRegression()
    m.fit(X,y)
    fut = np.array(range(len(dr), len(dr)+days)).reshape(-1,1)
    pr = m.predict(fut)
    st.write(pr)

except Exception as e:
    st.write("Error:")
    st.write(e)

st.write("TAPINU PRO READY")
