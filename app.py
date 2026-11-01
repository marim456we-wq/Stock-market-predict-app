import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

st.set_page_config(page_title="TAPINU - Full Chart", layout="wide", page_icon="📈")
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

st.title("📈 TAPINU PRO - Full Chart Fixed")
st.caption("Month mattum illa Sir - Full Year Varum Sir!")

# TOP TIMEFRAME SELECTOR LIKE TRADINGVIEW
st.markdown("### ⏰ Timeframe Select Pannunga Sir - Month mattum illa Sir!")

col_tf1, col_tf2, col_tf3, col_tf4 = st.columns([2,2,2,2])
with col_tf1:
    period = st.selectbox("Period - Ethana Naal Chart Venum?", ["1mo (1 Month)","3mo (3 Months)","6mo (6 Months)","1y (1 Year)","2y (2 Years)","5y (5 Years)","MAX"], index=3)
with col_tf2:
    interval = st.selectbox("Candle Type", ["1d (Daily)","1wk (Weekly)","1mo (Monthly)"], index=0)
with col_tf3:
    ticker_list = {"RELIANCE":"RELIANCE.NS","TATA MOTORS":"TATAMOTORS.NS","TCS":"TCS.NS","INFY":"INFY.NS","TRENT":"TRENT.NS","BTC":"BTC-USD"}
    sel = st.selectbox("Stock", list(ticker_list.keys()), index=0)
with col_tf4:
    manual = st.text_input("Manual Search", placeholder="TCS.NS")

ticker = manual.strip().upper() if manual.strip()!="" else ticker_list[sel]

# Convert period
period_map = {"1mo (1 Month)":"1mo","3mo (3 Months)":"3mo","6mo (6 Months)":"6mo","1y (1 Year)":"1y","2y (2 Years)":"2y","5y (5 Years)":"5y","MAX":"max"}
interval_map = {"1d (Daily)":"1d","1wk (Weekly)":"1wk","1mo (Monthly)":"1mo"}

p = period_map[period]
inter = interval_map[interval]

st.info(f"Selected: {ticker} - {period} - {interval} - Full Chart Varum Sir!")

@st.cache_data(ttl=30)
def get_data(t, per, inter):
    s = yf.Ticker(t)
    h = s.history(period=per, interval=inter)
    return h

try:
    hist = get_data(ticker, p, inter)
    if hist.empty:
        st.error("Data Not Found Sir")
        st.stop()
    
    # Indicators - Need enough data
    hist["MA20"] = hist["Close"].rolling(20).mean()
    hist["MA50"] = hist["Close"].rolling(50).mean()
    hist["MA200"] = hist["Close"].rolling(200).mean()
    hist["MA100"] = hist["Close"].rolling(100).mean()
    
    last = float(hist["Close"].iloc[-1])
    first = float(hist["Close"].iloc[0])
    total_change = ((last-first)/first)*100
    
    # TOP METRICS
    c1,c2,c3,c4 = st.columns(4)
    c1.metric(ticker+" LIVE", round(last,2), f"{round(total_change,2)}% {p}")
    c2.metric("Start Price", round(first,2))
    c3.metric("High", round(float(hist["High"].max()),2))
    c4.metric("Low", round(float(hist["Low"].min()),2))

    # TIMING ANALYSIS TABLE
    st.divider()
    st.subheader(f"⏰ Timing la Trade - {period} Full Chart Analysis")
    
    # Chart with full range
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=hist.index, 
        open=hist["Open"], 
        high=hist["High"], 
        low=hist["Low"], 
        close=hist["Close"],
        name="Price",
        increasing_line_color="#26a69a",
        decreasing_line_color="#ef5350"
    ))
    fig.add_trace(go.Scatter(x=hist.index, y=hist["MA20"], line=dict(color="#2962ff", width=1.5), name="MA20 (20 Days)"))
    fig.add_trace(go.Scatter(x=hist.index, y=hist["MA50"], line=dict(color="#ff6d00", width=1.5), name="MA50 (50 Days)"))
    fig.add_trace(go.Scatter(x=hist.index, y=hist["MA200"], line=dict(color="#ab47bc", width=1, dash="dash"), name="MA200 (200 Days)"))
    
    fig.update_layout(
        height=600,
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        title=f"{ticker} - {period} - Full Chart (Month mattum illa Sir, Full Year Sir!)",
        yaxis_title="Price",
        xaxis_title="Date",
        plot_bgcolor="#131722",
        paper_bgcolor="#131722"
    )
    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(step="all", label="ALL")
            ]),
            bgcolor="#1e222d",
            activecolor="#2962ff"
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.success(f"✅ Ippo {period} Full Chart Varuthu Sir! Month mattum illa Sir - {len(hist)} Candles Varuthu Sir!")

    # TIMING TABLE - Month wise performance
    st.subheader("📅 Month Wise Yeruthu Yeranguthu")
    hist_month = hist.copy()
    hist_month["YearMonth"] = hist_month.index.to_period("M")
    monthly = hist_month.groupby("YearMonth").agg({"Close":["first","last"],"High":"max","Low":"min"})
    monthly.columns = ["OpenMonth","CloseMonth","High","Low"]
    monthly["Change%"] = ((monthly["CloseMonth"]-monthly["OpenMonth"])/monthly["OpenMonth"]*100).round(2)
    monthly["Signal"] = monthly["Change%"].apply(lambda x: "📈 YERUTHU" if x>0 else "📉 YERANGUTHU")
    st.dataframe(monthly.tail(12), use_container_width=True)

    # Timing logic for today
    st.divider()
    st.subheader("⏰ Today Timing - Entha Time la Enna Pannanum")
    timing_data = {
        "Time": ["9:15-10:00", "10:00-11:30", "11:30-12:30", "12:30-2:00", "2:00-3:30"],
        "Market Nature": ["🔥 High Volatile - Gap Up/Down", "📈 Trending Up - Best Buy", "😴 Slow - Sideways", "😴 Lunch Low Volume", "⚡ Power Hour - Sell/Buy"],
        "Action": ["WATCH - Risk", "BUY - Yeruthu", "HOLD - Wait", "WAIT - Yeranguthu Chance", "SELL/BUY - Final Move"],
        "What Happens": ["Morning la price perusa yerum/yerangum", "10:30 ku aprom stable ah yerum", "Madhiyam slow ah irukkum", "Lunch time la volume kammi", "Last hour la perusa move varum"]
    }
    st.table(pd.DataFrame(timing_data))

    # Cute Robot
    st.divider()
    col_r1, col_r2 = st.columns([1,3])
    with col_r1:
        st.markdown(f"<div style='background:linear-gradient(135deg,#667eea,#764ba2); padding:20px; border-radius:15px; color:white; text-align:center;'><div style='font-size:50px;'>🤖</div><b>Robot</b><br>{now.strftime('%H:%M:%S')}<br>Chart: {period}</div>", unsafe_allow_html=True)
    with col_r2:
        q = st.text_input("Robot kitta chart pathi kelu Sir", placeholder="Full chart varutha?")
        if q:
            st.success(f"Full Chart Varuthu Sir! {period} la {len(hist)} candles irukku Sir! {ticker} {round(total_change,2)}% change Sir! MA20, MA50, MA200 ellam varuthu Sir! 🤖📈")

except Exception as e:
    st.error("Error")
    st.write(e)

st.caption("Month mattum illa Sir - Full Year, 5 Years varaikkum paarkalam Sir - TradingView maathiri Sir!")
