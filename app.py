import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date, timedelta
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="BATCH-5 Stock Predict", layout="wide")

st.markdown("<h1 style='text-align: center;'>BATCH-5 Stock Market Predict</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Stock Prediction App</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Predict Future Stock Prices</p>", unsafe_allow_html=True)
st.divider()

# Sidebar
st.sidebar.header("Configuration")
ticker = st.sidebar.selectbox("Select Stock", ["AAPL", "TSLA", "GOOGL", "MSFT", "TCS.NS", "INFY.NS"])
period = st.sidebar.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y"])

# Download Data
data = yf.download(ticker, period=period)
st.subheader(f"{ticker} Stock Data")
st.line_chart(data["Close"])
st.dataframe(data.tail())

# Prediction
st.subheader("Prediction")
data['Days'] = range(len(data))
X = np.array(data['Days']).reshape(-1, 1)
y = data['Close'].values

model = LinearRegression()
model.fit(X, y)

future_days = st.sidebar.slider("Days to Predict", 1, 30, 7)
future = np.array(range(len(data), len(data)+future_days)).reshape(-1, 1)
pred = model.predict(future)

st.write(f"Next {future_days} Days Prediction:")
st.write(pred)
st.success("App Live Successfully! Tamil Selvi Mam Ku Anuppa Ready!")
