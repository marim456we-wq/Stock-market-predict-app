import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime

st.set_page_config(page_title="BATCH-5 FINAL MASTER APP", layout="wide", page_icon="🚀")
st.markdown("<h1 style='text-align: center;'>🚀 BATCH-5 FINAL MASTER APP</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>World Stock | Real Time | Chatbot | Buy/Sell | No Error</p>", unsafe_allow_html=True)
st.divider()

st.sidebar.title("⚙️ BATCH-5 MASTER CONTROL")
st.sidebar.success("All Features Added Sir!")
ticker = st.sidebar.text_input("🔍 Search Any Stock", value="RELIANCE.NS")
period = st.sidebar.selectbox("Period", ["1mo","3mo","6mo","1y"], index=2)
future_days = st.sidebar.slider("Predict Days", 1, 30, 7)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Vanakkam Sir! Naan Final Master Chatbot Sir! World Stock, Real Time, Buy/Sell Ellame Theriyum Sir!"}]

col1, col2 = st.columns([2,1])

with col1:
    try:
        try:
            live_ticker = yf.Ticker(ticker)
            live_price = live_ticker.fast_info['last_price']
            st.metric(f"REAL TIME LIVE {ticker}", f"{live_price:.2f}", f"Updated {datetime.datetime.now().strftime('%H:%M:%S')}")
        except:
            live_price = 0
            st.write("Live Price Loading Sir...")

        data = yf.download(ticker, period=period, progress=False)
        if data.empty:
            st.error(f"{ticker} Not Found Sir!")
        else:
            data["MA20"] = data["Close"].rolling(20).mean()
            data["MA50"] = data["Close"].rolling(50).mean()
            delta = data["Close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            data["RSI"] = 100 - (100 / (1 + rs))
            
            last_close = float(data["Close"].iloc[-1])
            ma20 = float(data["MA20"].iloc[-1]) if not pd.isna(data["MA20"].iloc[-1]) else last_close
            ma50 = float(data["MA50"].iloc[-1]) if not pd.isna(data["MA50"].iloc[-1]) else last_close
            rsi = float(data["RSI"].iloc[-1]) if not pd.isna(data["RSI"].iloc[-1]) else 50

            buy = 0
            sell = 0
            if ma20 > ma50: buy+=1
            else: sell+=1
            if rsi < 30: buy+=1
            elif rsi > 70: sell+=1
            if last_close > ma20: buy+=1
            else: sell+=1

            if buy > sell:
                st.success(f"🟢 BUY SIGNAL - BUY {ticker} - {buy} vs {sell}")
                st.balloons()
            elif sell > buy:
                st.error(f"🔴 SELL SIGNAL - SELL {ticker} - {sell} vs {buy}")
            else:
                st.warning(f"🟡 HOLD SIGNAL - WAIT - {buy} vs {sell}")

            st.write(f"MA20: {ma20:.2f} | MA50: {ma50:.2f} | RSI: {rsi:.2f}")
            st.line_chart(data[["Close","MA20","MA50"]].dropna())
            st.dataframe(data.tail(10), use_container_width=True)

            st.subheader(f"Next {future_days} Days Prediction")
            data['Days'] = range(len(data))
            X = np.array(data['Days']).reshape(-1, 1)
            y = data['Close'].values
            model = LinearRegression()
            model.fit(X, y)
            future = np.array(range(len(data), len(data)+future_days)).reshape(-1,1)
            pred = model.predict(future)
            st.dataframe(pd.DataFrame({"Day": range(1, future_days+1), "Predicted Price": pred}), use_container_width=True)
            
            csv = data.to_csv().encode('utf-8')
            st.download_button("Download CSV", csv, f"{ticker}.csv")

    except Exception as e:
        st.error(f"Error Sir: {e}")

with col2:
    st.subheader("🤖 Customer Chatbot")
    for msg in st.session
