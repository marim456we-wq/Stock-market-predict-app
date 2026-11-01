import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

st.set_page_config(page_title="TAPINU + Cute Robot", layout="wide", page_icon="🤖")

# CUTE ROBOT CSS + FLOATING BUTTON
st.markdown("""
<style>
#robot-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9999;
}
#cute-robot {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 35px;
    cursor: pointer;
    box-shadow: 0 8px 25px rgba(102,126,234,0.5);
    animation: float 3s ease-in-out infinite;
    border: 3px solid white;
}
#cute-robot:hover {
    transform: scale(1.1);
    box-shadow: 0 12px 35px rgba(102,126,234,0.7);
}
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}
.robot-pulse {
    position: absolute;
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background: rgba(102,126,234,0.3);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    100% { transform: scale(1.5); opacity: 0; }
}
.chat-bubble {
    position: fixed;
    bottom: 100px;
    right: 20px;
    background: white;
    color: black;
    padding: 10px 15px;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    font-size: 12px;
    max-width: 200px;
    z-index: 9998;
    animation: bounce 1s infinite;
}
@keyframes bounce {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}
</style>

<div id="robot-container">
    <div class="robot-pulse"></div>
    <div id="cute-robot" onclick="document.getElementById('robot-chat').scrollIntoView({behavior: 'smooth'})">🤖</div>
</div>
<div class="chat-bubble">👋 Hi Sir! Enna Touch Pannunga Sir!</div>
""", unsafe_allow_html=True)

st.title("📈 TAPINU PRO - TradingView + Cute Robot Assistant")
st.caption("Cute Robot Side la Irukku Sir - Touch Pannunga Sir")

# SIDEBAR STOCKS
st.sidebar.title("📋 Stocks")
stock_list = {"RELIANCE":"RELIANCE.NS","TCS":"TCS.NS","INFY":"INFY.NS","HDFC":"HDFCBANK.NS","AAPL":"AAPL","BTC":"BTC-USD","GOLD":"GC=F"}
selected = st.sidebar.selectbox("Select Stock", list(stock_list.keys()), index=0)
manual = st.sidebar.text_input("Manual Search", value="")
ticker = manual.strip().upper() if manual.strip()!="" else stock_list[selected]
period = st.sidebar.selectbox("Period", ["1mo","3mo","6mo","1y"], index=2)

# TIME
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

@st.cache_data(ttl=30)
def get_data(t,p):
    s = yf.Ticker(t)
    h = s.history(period=p)
    return h

try:
    hist = get_data(ticker, period)
    if hist.empty:
        st.error("Not Found Sir")
        st.stop()
    
    hist["MA20"] = hist["Close"].rolling(20).mean()
    hist["MA50"] = hist["Close"].rolling(50).mean()
    delta = hist["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    hist["RSI"] = 100 - (100 / (1 + rs))

    last = float(hist["Close"].iloc[-1])
    ma20 = float(hist["MA20"].iloc[-1])
    ma50 = float(hist["MA50"].iloc[-1])
    rsi = float(hist["RSI"].iloc[-1])

    c1,c2,c3,c4 = st.columns(4)
    c1.metric(ticker+" LIVE", round(last,2))
    c2.metric("MA20", round(ma20,2))
    c3.metric("MA50", round(ma50,2))
    c4.metric("RSI", round(rsi,2))

    score = 0
    if last > ma20: score+=1
    else: score-=1
    if ma20 > ma50: score+=1
    else: score-=1
    if rsi < 35: score+=1
    elif rsi > 70: score-=1

    if score>=1:
        decision = "BUY"
        st.success("BUY SIGNAL - " + ticker)
    else:
        decision = "SELL"
        st.error("SELL SIGNAL - " + ticker)

    # CHART
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=hist.index, open=hist["Open"], high=hist["High"], low=hist["Low"], close=hist["Close"], name="Price"))
    fig.add_trace(go.Scatter(x=hist.index, y=hist["MA20"], line=dict(color="blue"), name="MA20"))
    fig.add_trace(go.Scatter(x=hist.index, y=hist["MA50"], line=dict(color="red"), name="MA50"))
    fig.update_layout(height=500, template="plotly_dark", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.write(e)
    decision = "HOLD"
    last = 0
    rsi = 50

# CUTE ROBOT CHAT SECTION - BOTTOM
st.divider()
st.markdown('<div id="robot-chat"></div>', unsafe_allow_html=True)

# ROBOT CHAT UI - CUTE DESIGN
st.markdown("""
### 🤖 Cute Robot Assistant - Touch Panni Pesunga Sir!
""")

col_robot, col_chat = st.columns([1,3])

with col_robot:
    st.markdown("""
    <div style="text-align:center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding:30px; border-radius:20px; color:white;">
        <div style="font-size:60px; animation: float 2s infinite;">🤖</div>
        <h3>TAPINU Robot</h3>
        <p>Hi Sir! 👋</p>
        <p style="font-size:12px;">Enna Kettaalum Solluven Sir!</p>
        <div style="background:rgba(255,255,255,0.2); padding:8px; border-radius:10px; margin-top:10px;">🟢 Online</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("#### Quick Touch Buttons:")
    if st.button("📈 Buy or Sell?"):
        st.session_state["q"] = "buy or sell"
    if st.button("🎯 Target Enna?"):
        st.session_state["q"] = "target"
    if st.button("⏰ Market Enna?"):
        st.session_state["q"] = "market"
    if st.button("💡 Idea Sollu"):
        st.session_state["q"] = "idea"

with col_chat:
    # Initialize chat
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role":"robot","text":"Vanakkam Sir! 🙏 Naan Unga Cute Robot Sir! " + ticker + " pathi enna venum kélunga Sir! Touch panna ready Sir! 🤖✨"}]
    
    # Show messages
    for msg in st.session_state["messages"]:
        if msg["role"] == "robot":
            st.markdown(f"<div style='background:#f0f0ff; padding:12px; border-radius:15px 15px 15px 0; margin:5px 0; border-left:4px solid #667eea;'><b>🤖 Robot:</b> {msg['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:#e8f5e9; padding:12px; border-radius:15px 15px 0 15px; margin:5px 0; text-align:right;'><b>Neenga:</b> {msg['text']}</div>", unsafe_allow_html=True)

    # Input
    user_input = st.text_input("Robot kitta Pesunga Sir...", value=st.session_state.get("q",""), key="user_input_box", placeholder="Ex: Buy pannalama Sell pannalama Sir?")
    
    if st.button("Send to Robot 🚀", type="primary") and user_input:
        st.session_state["messages"].append({"role":"user","text":user_input})
        ql = user_input.lower()
        
        # Robot Brain - Cute Responses
        if "buy" in ql or "sell" in ql or "enna" in ql:
            if decision == "BUY":
                resp = f"BUY PANNUNGA SIR! 🚀 {ticker} SEMMA BUY SIGNAL SIR! Live {round(last,2)} Sir - RSI {round(rsi,1)} Sir - Munnadi Yerum Sir! Naan Solla Buy Sir! 🤖💚"
            else:
                resp = f"SELL PANNUNGA SIR! 📉 {ticker} Sell Signal Sir! Live {round(last,2)} Sir - Market Koraiyum Sir - Sell Panni Profit Book Pannunga Sir! 🤖❤️"
        elif "target" in ql:
            resp = f"Target Sir? {ticker} ku Target {round(last*1.05,2)} Sir! Stop Loss {round(last*0.97,2)} Sir! 5% Profit Varum Sir! 🤖🎯"
        elif "market" in ql:
            resp = f"Market Ippo Open Sir! ⏰ Time {now.strftime('%H:%M:%S')} Sir! {ticker} Live {round(last,2)} Sir! Trading Pannalam Sir! 🤖📈"
        elif "idea" in ql or "tip" in ql:
            resp = f"Idea Ah Sir? 💡 {ticker} ku MA20 {round(ma20,2)} Sir - MA50 {round(ma50,2)} Sir - RSI {round(rsi,1)} Sir - Candle Chart Paathu Trade Pannunga Sir! 🤖✨"
        elif "hi" in ql or "hello" in ql or "vanakkam" in ql:
            resp = f"Vanakkam Sir! 🙏💖 Naan Unga Cute Robot Sir! Romba Santhosam Sir Neenga Pesunathu! {ticker} pathi enna venum Sir? 🤖😊"
        else:
            resp = f"Puriyuthu Sir! 🤖 {ticker} Live {round(last,2)} Sir - RSI {round(rsi,1)} Sir - {decision} Signal Sir - Vera enna venum Sir? Kelu Sir! 😊"

        st.session_state["messages"].append({"role":"robot","text":resp})
        st.session_state["q"] = ""
        st.rerun()

    if st.button("Clear Chat 🧹"):
        st.session_state["messages"] = []
        st.rerun()

st.divider()
st.caption("TAPINU + Cute Robot - Touch Panna Pesum Robot Sir 🤖")

# requirements
# streamlit, yfinance, pandas, plotly, pytz
