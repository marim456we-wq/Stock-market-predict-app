import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta

# Try import tensorflow - if not available use simple logic
try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense
    TF_AVAILABLE = True
except:
    TF_AVAILABLE = False

st.set_page_config(page_title="TAPINU - AI Prediction", layout="wide")
st.markdown("## 🤖 TAPINU - GitHub Stock Prediction - AI Model")

# GITHUB REPO LOGIC - LSTM PREDICTION
# Source: github.com/adititanna/stock-market-intraday-predictor
# Source: github.com/TauricResearch/TradingAgents logic

st.markdown("**GitHub Top Repos Logic: LSTM + Technical Analysis + BUY/SELL**")

# Stock Input - World Any Stock
stock_input = st.text_input("🌍 Stock Symbol Type Pannunga Sir (GitHub style)", value="RELIANCE.NS", placeholder="RELIANCE.NS, TCS.NS, AAPL, ZOMATO.NS, ^BSESN")

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("RELIANCE 🇮🇳"): stock_input = "RELIANCE.NS"
with col2:
    if st.button("TCS 🇮🇳"): stock_input = "TCS.NS"
with col3:
    if st.button("SENSEX"): stock_input = "^BSESN"
with col4:
    if st.button("AAPL 🇺🇸"): stock_input = "AAPL"

symbol = stock_input.strip().upper()
if not symbol:
    symbol = "RELIANCE.NS"

st.write(f"**Predicting: {symbol}**")

# Fetch Data - GitHub method
@st.cache_data(ttl=300)
def get_data(sym):
    return yf.Ticker(sym).history(period="1y", interval="1d")

df = get_data(symbol)

if df.empty:
    st.error("Data varala Sir - Symbol check pannunga Sir")
    st.stop()

# Technical Indicators - GitHub: trading-signals repo
df["MA20"] = df["Close"].rolling(20).mean()
df["MA50"] = df["Close"].rolling(50).mean()
df["RSI"] = 100 - (100 / (1 + df["Close"].pct_change().rolling(14).mean()))
df["Upper"] = df["MA20"] + 2*df["Close"].rolling(20).std()
df["Lower"] = df["MA20"] - 2*df["Close"].rolling(20).std()

# LSTM Prediction Logic - From GitHub intraday-predictor
@st.cache_data(ttl=300)
def lstm_predict(data_close):
    try:
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(data_close.values.reshape(-1,1))
        
        # Prepare 60 days sequence
        seq_len = 60
        X = []
        for i in range(seq_len, len(scaled)):
            X.append(scaled[i-seq_len:i])
        X = np.array(X)
        
        if TF_AVAILABLE and len(X) > 0:
            # Simple LSTM Model - GitHub Code
            model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(seq_len,1)),
                LSTM(50),
                Dense(1)
            ])
            model.compile(optimizer='adam', loss='mse')
            # Train quickly - 3 epochs for demo (GitHub repo uses more)
            model.fit(X, scaled[seq_len:], epochs=3, batch_size=32, verbose=0)
            
            # Predict next 7 days
            last_seq = scaled[-seq_len:]
            preds = []
            curr = last_seq.copy()
            for _ in range(7):
                p = model.predict(curr.reshape(1, seq_len, 1), verbose=0)[0][0]
                preds.append(p)
                curr = np.append(curr[1:], [[p]], axis=0)
            
            preds = scaler.inverse_transform(np.array(preds).reshape(-1,1)).flatten()
            return preds
        else:
            # Fallback simple trend prediction if TF not available
            last_price = data_close.iloc[-1]
            trend = (data_close.iloc[-1] - data_close.iloc[-20]) / 20
            return 
