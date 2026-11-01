import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime

st.set_page_config(page_title="BATCH-5 FINAL APP", layout="wide")
st.title("BATCH-5 FINAL MASTER APP")
st.write("World Stock | Real Time | Chatbot | Buy Sell | No Error")
st.divider()

st.sidebar.title("Control")
ticker = st.sidebar.text_input("Search Stock", value="RELIANCE.NS")
period = st.sidebar.selectbox("Period", ["1mo","3mo","6mo","1y"], index=2)
future_days = st.sidebar.slider("Predict Days", 1, 20, 5)

# Real time price
try:
    live = yf.Ticker(ticker)
    price = live.fast_info["last_price"]
    st.metric(f"LIVE {ticker}", f"{price}")
except:
    price = 0
    st.write("Loading...")

# Download data
data = yf.download(ticker, period=period, progress=False)

if data.empty:
    st.error("Not Found")
else:
    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()
    
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))
    
    last = float(data["Close"].iloc[-1])
    ma20 = float(data["MA20"].iloc[-1]) if not pd.isna(data["MA20"].iloc[-1]) else last
    ma50 = float(data["MA50"].iloc[-1]) if not pd.isna(data["MA50"].iloc[-1]) else last
    rsi = float(data["RSI"].iloc[-1]) if not pd.isna(data["RSI"].iloc[-1]) else 50
    
    buy = 0
    sell = 0
    if ma20 > ma50:
        buy = buy + 1
    else:
        sell = sell + 1
    if rsi < 30:
        buy = buy + 1
    elif rsi > 70:
        sell = sell + 1
    if last > ma20:
        buy = buy + 1
    else:
        sell = sell + 1
    
    if buy > sell:
        st.success(f"BUY SIGNAL {ticker} BUY {buy} vs {sell}")
    elif sell > buy:
        st.error(f"SELL SIGNAL {ticker} SELL {sell} vs {buy}")
    else:
        st.warning(f"HOLD SIGNAL {ticker} HOLD")
    
    st.write(f"MA20 {ma20:.2f} MA50 {ma50:.2f} RSI {rsi:.2f}")
    st.line_chart(data[["Close","MA20","MA50"]])
    st.dataframe(data.tail(10))
    
    # Prediction
    st.subheader("Prediction")
    data["Days"] = range(len(data))
    X = np.array(data["Days"]).reshape(-1, 1)
    y = data["Close"].values
    model = LinearRegression()
    model.fit(X, y)
    future = np.array(range(len(data), len(data)+future_days)).reshape(-1, 1)
    pred = model.predict(future)
    st.write(pred)
    
    # Chatbot Simple
    st.divider()
    st.subheader("Customer Chatbot")
    user_q = st.text_input("Kelu Sir")
    if user_q:
        q = user_q.lower()
        if "buy" in q:
            if buy > sell:
                st.write(f"BUY Sir {ticker}")
            else:
                st.write(f"SELL Sir {ticker}")
        elif "gold" in q:
            st.write("GC=F Type Pannunga Sir Gold")
        elif "real" in q:
            st.write(f"Real Time Price {price} Sir")
        else:
            st.write(f"Super Sir {ticker} Search Pannunga Sir")

st.divider()
st.write("BATCH-5 FINAL APP READY")
