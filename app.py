
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="TAPINU PRO",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: #080d18;
    color: #ffffff;
}
[data-testid="stSidebar"] {
    background: #101827;
}
.block-container {
    padding-top: 1.5rem;
    max-width: 1500px;
}
.metric-card {
    background: #111c2e;
    border: 1px solid #26364d;
    padding: 17px;
    border-radius: 12px;
    margin-bottom: 10px;
}
.metric-label {
    color: #9aacc3;
    font-size: 13px;
}
.metric-value {
    color: white;
    font-size: 25px;
    font-weight: bold;
}
.metric-change {
    color: #00d69a;
    font-size: 13px;
}
div.stButton > button {
    background: #1677ff;
    color: white;
    border-radius: 8px;
    border: none;
    width: 100%;
}
h1, h2, h3 {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("# 📈 TAPINU PRO")
st.caption("PROFESSIONAL MARKET ANALYTICS PLATFORM")

st.markdown("---")

# ---------------- DATA ----------------
@st.cache_data(ttl=60)
def get_market_data(symbol, period, interval):
    df = yf.download(
        symbol,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False
    )

    if df.empty:
        return pd.DataFrame()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df.dropna()

def indicators(df):
    df = df.copy()

    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()

    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/14, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["RSI"] = 100 - (100 / (1 + rs))

    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()

    df["MACD"] = ema12 - ema26
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return df

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ CONTROL PANEL")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Market Chart",
        "Watchlist",
        "Portfolio",
        "Customer Care"
    ]
)

symbol = st.sidebar.text_input(
    "Stock Symbol",
    "RELIANCE.NS"
).strip().upper()

period = st.sidebar.selectbox(
    "Chart Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=2
)

interval = st.sidebar.selectbox(
    "Time Interval",
    ["1d", "1h", "30m", "15m", "5m"],
    index=0
)

# ---------------- MARKET ----------------
@st.cache_data(ttl=60)
def get_quote(symbol):
    ticker = yf.Ticker(symbol)
    return ticker.history(period="5d", interval="1d", auto_adjust=True)

def show_market(symbol):
    df = get_quote(symbol)

    if df.empty:
        st.error("Market data unavailable. Check the symbol.")
        return

    current = float(df["Close"].iloc[-1])
    previous = float(df["Close"].iloc[-2]) if len(df) > 1 else current

    change = current - previous
    percent = (change / previous * 100) if previous else 0

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""<div class="metric-card">
            <div class="metric-label">CURRENT PRICE</div>
            <div class="metric-value">₹{current:,.2f}</div>
            </div>""",
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""<div class="metric-card">
            <div class="metric-label">PRICE CHANGE</div>
            <div class="metric-value">{change:+,.2f}</div>
            </div>""",
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""<div class="metric-card">
            <div class="metric-label">CHANGE %</div>
            <div class="metric-value">{percent:+.2f}%</div>
            </div>""",
            unsafe_allow_html=True
        )

# ---------------- CHART ----------------
def show_chart(symbol):
    df = get_market_data(symbol, period, interval)

    if df.empty:
        st.error("Unable to load chart data.")
        return

    df = indicators(df)

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Candlestick"
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["SMA20"],
        name="SMA 20",
        line=dict(color="#00c8ff", width=1.5)
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["SMA50"],
        name="SMA 50",
        line=dict(color="#ffb000", width=1.5)
    ))

    fig.update_layout(
        template="plotly_dark",
        height=570,
        paper_bgcolor="#080d18",
        plot_bgcolor="#080d18",
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h")
    )

    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)

    with left:
        st.subheader("RSI Indicator")
        rsi_fig = go.Figure()
        rsi_fig.add_trace(go.Scatter(
            x=df.index, y=df["RSI"], name="RSI"
        ))
        rsi_fig.add_hline(y=70, line_dash="dash")
        rsi_fig.add_hline(y=30, line_dash="dash")
        rsi_fig.update_layout(
            template="plotly_dark",
            height=250,
            paper_bgcolor="#080d18",
            plot_bgcolor="#080d18"
        )
        st.plotly_chart(rsi_fig, use_container_width=True)

    with right:
        st.subheader("MACD Indicator")
        macd_fig = go.Figure()
        macd_fig.add_trace(go.Scatter(
            x=df.index, y=df["MACD"], name="MACD"
        ))
        macd_fig.add_trace(go.Scatter(
            x=df.index, y=df["Signal"], name="Signal"
        ))
        macd_fig.update_layout(
            template="plotly_dark",
            height=250,
            paper_bgcolor="#080d18",
            plot_bgcolor="#080d18"
        )
        st.plotly_chart(macd_fig, use_container_width=True)

    st.subheader("Market Data")
    st.dataframe(df.tail(20), use_container_width=True)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("Market Dashboard")
    st.caption("Market data is supplied by Yahoo Finance.")

    show_market(symbol)

    st.markdown("---")
    st.subheader("Technical Analysis")

    df = get_market_data(symbol, period, interval)

    if not df.empty:
        df = indicators(df)
        st.metric("RSI (14)", round(float(df["RSI"].iloc[-1]), 2))
        st.metric("MACD", round(float(df["MACD"].iloc[-1]), 3))

        rsi = df["RSI"].iloc[-1]

        if pd.notna(rsi):
            if rsi > 70:
                st.warning("RSI indicates a potentially overbought market.")
            elif rsi < 30:
                st.info("RSI indicates a potentially oversold market.")
            else:
                st.success("RSI is in the middle range.")

    st.markdown("---")
    st.info("Analytics only. These indicators are not guaranteed trading signals.")

# ---------------- MARKET CHART ----------------
elif page == "Market Chart":
    st.title("Advanced Trading Chart")
    show_chart(symbol)

# ---------------- WATCHLIST ----------------
elif page == "Watchlist":

    st.title("My Watchlist")

    default_symbols = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS",
        "BTC-USD",
        "ETH-USD"
    ]

    for item in default_symbols:
        try:
            data = get_quote(item)
            if not data.empty:
                price = float(data["Close"].iloc[-1])
                st.markdown(
                    f"""<div class="metric-card">
                    <b>{item}</b>
                    <span style="float:right">₹{price:,.2f}
                    </span></div>""",
                    unsafe_allow_html=True
                )
        except Exception:
            st.write(item, "Data unavailable")

# ---------------- PAPER PORTFOLIO ----------------
elif page == "Portfolio":

    st.title("Demo Portfolio")
    st.caption("Virtual portfolio for educational tracking. No real trades.")

    if "demo_cash" not in st.session_state:
        st.session_state.demo_cash = 100000.0

    if "demo_holdings" not in st.session_state:
        st.session_state.demo_holdings = {}

    st.metric("Virtual Cash", f"₹{st.session_state.demo_cash:,.2f}")

    stock = st.text_input("Demo Stock Symbol", "RELIANCE.NS").upper()
    quantity = st.number_input("Quantity", min_value=1, value=1)

    if st.button("Add Demo Holding"):
        try:
            data = get_quote(stock)
            if data.empty:
                st.error("Price unavailable")
            else:
                price = float(data["Close"].iloc[-1])
                cost = price * quantity

                if cost <= st.session_state.demo_cash:
                    holdings = st.session_state.demo_holdings
                    holdings[stock] = holdings.get(stock, 0) + quantity
                    st.session_state.demo_cash -= cost
                    st.success("Demo holding added.")
                else:
                    st.error("Not enough virtual cash.")
        except Exception:
            st.error("Unable to fetch price.")

    st.subheader("Your Demo Holdings")
    if st.session_state.demo_holdings:
        for name, qty in st.session_state.demo_holdings.items():
            st.write(f"**{name}** — {qty} units")
    else:
        st.write("No demo holdings yet.")

# ---------------- CUSTOMER CARE ----------------
elif page == "Customer Care":

    st.title("🤖 TAPINU AI Customer Care")
    st.caption("Automated help assistant - basic demo version.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_message = st.chat_input("Ask TAPINU support...")

    if user_message:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message
        })

        msg = user_message.lower()

        if "chart" in msg:
            answer = "Open Market Chart to see candlestick charts and indicators."
        elif "watchlist" in msg:
            answer = "Open Watchlist to monitor selected market symbols."
        elif "portfolio" in msg:
            answer = "Open Portfolio to manage your virtual demo holdings."
        elif "rsi" in msg:
            answer = "RSI is a momentum indicator, commonly measured from 0 to 100."
        elif "macd" in msg:
            answer = "MACD is a technical indicator based on moving averages."
        elif "price" in msg or "market" in msg:
            answer = "Choose a stock symbol in the sidebar and open Dashboard."
        elif "hello" in msg or "hi" in msg:
            answer = "Hello! Welcome to TAPINU PRO Support. How can I help?"
        else:
            answer = "Thanks for contacting TAPINU Support. Please ask about charts, market data, RSI, MACD, watchlists or demo portfolio."

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "TAPINU PRO © 2026 | Educational Market Analytics | "
    "Yahoo Finance data may be delayed or unavailable. "
    "Not financial advice."
)

