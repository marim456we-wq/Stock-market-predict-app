import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime, time

st.set_page_config(page_title="BATCH-5 FINAL MASTER APP", layout="wide", page_icon="🚀")
st.markdown("<h1 style='text-align: center;'>🚀 BATCH-5 FINAL MASTER APP</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>World Stock | Real Time | Chatbot | Buy/Sell | No Error</p>", unsafe_allow_html=True)
st.divider()

# Sidebar
st.sidebar.title("⚙️ BATCH-5 MASTER CONTROL")
st.sidebar.success("All Features Added Sir!")

ticker = st.sidebar.text_input("🔍 Search Any Stock (World)", value="RELIANCE.NS", help="RELIANCE.NS, TCS.NS, AAPL, TSLA, GC=F (Gold), BTC-USD")
period = st.sidebar.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)
future_days = st.sidebar.slider("Predict Days", 1, 30, 7)

# Chatbot init
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Vanakkam Sir! Naan Final Master Chatbot Sir! World Stock, Real Time, Buy/Sell Ellame Theriyum Sir! Enna Venum Kelu Sir!"}]

# Main Layout
col1, col2 = st.columns([2, 1])

with col1:
    try:
        # REAL TIME
        try:
            live_ticker = yf.Ticker(ticker)
            live_price = live_ticker.fast_info['last_price']
            st.metric(f"🔴 REAL TIME LIVE {ticker}", f"{live_price:.2f}", f"Updated {datetime.datetime.now().strftime('%H:%M:%S')}")
        except:
            st.write("Live Price Loading Sir...")

        data = yf.download(ticker, period=period, progress=False)
        if data.empty:
            st.error(f"❌ {ticker} Not Found Sir! Check Spelling Sir!")
        else:
            # Indicators
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

            # Buy/Sell
            buy = 0
            sell = 0
            if ma20 > ma50: buy+=1
            else: sell+=1
            if rsi < 30: buy+=1
            elif rsi > 70: sell+=1
            if last_close > ma20: buy+=1
            else: sell+=1

            if buy > sell:
                st.success(f"🟢 BUY SIGNAL SIR! BUY {ticker} Sir! ({buy} vs {sell})")
            elif sell > buy:
                st.error(f"🔴 SELL SIGNAL SIR! SELL {ticker} Sir! ({sell} vs {buy})")
            else:
                st.warning(f"🟡 HOLD SIR! WAIT SIR! ({buy} vs {sell})")

            st.write(f"MA20: {ma20:.2f} | MA50: {ma50:.2f} | RSI: {rsi:.2f}")
            st.line_chart(data[["Close","MA20","MA50"]].dropna())
            st.dataframe(data.tail(10), use_container_width=True)

            # Prediction
            st.subheader(f"🔮 Next {future_days} Days Prediction")
            data['Days'] = range(len(data))
            X = np.array(data['Days']).reshape(-1, 1)
            y = data['Close'].values
            model = LinearRegression()
            model.fit(X, y)
            future = np.array(range(len(data), len(data)+future_days)).reshape(-1,1)
            pred = model.predict(future)
            st.dataframe(pd.DataFrame({"Day": range(1, future_days+1), "Predicted Price": pred}), use_container_width=True)
            
            csv = data.to_csv().encode('utf-8')
            st.download_button("📥 Download CSV", csv, f"{ticker}.csv")

    except Exception as e:
        st.error(f"Error Sir: {e}")

with col2:
    st.subheader("🤖 Customer Chatbot (All Features)")
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    if prompt := st.chat_input("Kelunga Sir..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        q = prompt.lower()
        if "buy" in q or "sell" in q:
            ans = f"Trader Sir! {ticker} ku {'BUY' if buy>sell else 'SELL' if sell>buy else 'HOLD'} Signal Sir! Live Price {live_price:.2f} Sir!"
        elif "real time" in q:
            ans = f"Yes Sir Real Time Sir! {ticker} Live Price {live_price:.2f} Sir! Update {datetime.datetime.now().strftime('%H:%M:%S')} Sir!"
        elif "gold" in q:
            ans = "GC=F Type Pannunga Sir Gold Varum Sir!"
        elif "reliance" in q:
            ans = "RELIANCE.NS Type Pannunga Sir!"
        else:
            ans = f"Super Sir! {prompt
