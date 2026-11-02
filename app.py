
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ================= CONFIG =================

st.set_page_config(
    page_title="TAPINU | TradingView",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= DESIGN =================

st.markdown("""
<style>
.stApp {
    background: #0b0e11;
    color: #eaecef;
}
header[data-testid="stHeader"] {
    background: #0b0e11;
}
.block-container {
    padding-top: 1.2rem;
    max-width: 1600px;
}
[data-testid="stSidebar"] {
    background: #131722;
}
.metric-card {
    background: #131722;
    border: 1px solid #252a36;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 8px;
}
.small-label {
    color: #848e9c;
    font-size: 13px;
}
.price {
    color: #eaecef;
    font-size: 25px;
    font-weight: bold;
}
.green {color: #0ecb81;}
.red {color: #f6465d;}
h1, h2, h3 {
    color: #eaecef !important;
}
div[data-testid="stMetric"] {
    background: #131722;
    border: 1px solid #252a36;
    padding: 12px;
    border-radius: 10px;
}
.stTabs [data-baseweb="tab"] {
    color: #d1d4dc;
}
</style>
""", unsafe_allow_html=True)

# ================= SYMBOLS =================

symbols = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN",
    "BANK NIFTY": "^NSEBANK",
    "TCS": "TCS.NS",
    "RELIANCE": "RELIANCE.NS",
    "INFOSYS": "INFY.NS",
    "HDFC BANK": "HDFCBANK.NS",
    "ICICI BANK": "ICICIBANK.NS",
    "WIPRO": "WIPRO.NS",
    "TATA MOTORS": "TMPV.NS"
}

# ================= DATA =================

@st.cache_data(ttl=300)
def get_data(symbol, period="1y"):
    try:
        df = yf.download(
            symbol,
            period=period,
            interval="1d",
            auto_adjust=True,
            progress=False
        )

        if df.empty:
            return pd.DataFrame()

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.dropna()

        if "Close" not in df.columns:
            return pd.DataFrame()

        for col in ["Open", "High", "Low", "Close", "Volume"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["Close"])

        df["EMA20"] = df["Close"].ewm(span=20).mean()
        df["SMA50"] = df["Close"].rolling(50).mean()
        df["SMA200"] = df["Close"].rolling(200).mean()

        delta = df["Close"].diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / loss.replace(0, np.nan)

        df["RSI"] = 100 - (100 / (1 + rs))
        df["RSI"] = df["RSI"].fillna(50)

        return df

    except Exception:
        return pd.DataFrame()


# ================= HEADER =================

st.markdown("""
# 📈 TAPINU
### ADVANCED INDIAN STOCK MARKET TERMINAL
""")

st.caption(
    "Market data: Yahoo Finance | Daily data may be delayed"
)

# ================= SIDEBAR =================

st.sidebar.title("📊 TAPINU MENU")

selected_name = st.sidebar.selectbox(
    "Select Market / Stock",
    list(symbols.keys())
)

period_option = st.sidebar.selectbox(
    "Chart Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=3
)

show_ema = st.sidebar.checkbox("EMA 20", True)
show_sma50 = st.sidebar.checkbox("SMA 50", True)
show_sma200 = st.sidebar.checkbox("SMA 200", True)

st.sidebar.markdown("---")
st.sidebar.caption("TAPINU | Market Intelligence")

symbol = symbols[selected_name]

# ================= LOAD DATA =================

with st.spinner("Loading market data..."):
    df = get_data(symbol, period_option)

if df.empty or len(df) < 2:
    st.error("Market data unavailable. Please try again later.")
    st.stop()

latest = float(df["Close"].iloc[-1])
previous = float(df["Close"].iloc[-2])

change = latest - previous
change_pct = (change / previous) * 100 if previous else 0

# ================= MARKET CARDS =================

st.subheader("Market Overview")

market_cols = st.columns(4)

for i, name in enumerate(
    ["NIFTY 50", "SENSEX", "TCS", "RELIANCE"]
):
    market_symbol = symbols[name]
    market_df = get_data(market_symbol, "5d")

    with market_cols[i]:
        if not market_df.empty and len(market_df) >= 2:
            price = float(market_df["Close"].iloc[-1])
            old = float(market_df["Close"].iloc[-2])
            pct = ((price - old) / old) * 100 if old else 0

            st.metric(
                name,
                f"₹{price:,.2f}" if name not in
                ["NIFTY 50", "SENSEX"] else f"{price:,.2f}",
                f"{pct:+.2f}%"
            )
        else:
            st.metric(name, "Unavailable", "—")

st.markdown("---")

# ================= STOCK DETAILS =================

st.subheader(f"📈 {selected_name}")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Current / Latest Close", f"{latest:,.2f}")
c2.metric("Change", f"{change:+,.2f}", f"{change_pct:+.2f}%")

high = float(df["High"].iloc[-1]) if "High" in df else latest
low = float(df["Low"].iloc[-1]) if "Low" in df else latest

c3.metric("Day High", f"{high:,.2f}")
c4.metric("Day Low", f"{low:,.2f}")

# ================= MAIN CHART =================

st.subheader("Advanced Chart")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df.index,
    y=df["Close"],
    name="Price",
    mode="lines",
    line=dict(color="#2962ff", width=2.5)
))

if show_ema:
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["EMA20"],
        name="EMA 20",
        line=dict(color="#ffb74d", width=1.5)
    ))

if show_sma50:
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["SMA50"],
        name="SMA 50",
        line=dict(color="#e040fb", width=1.5)
    ))

if show_sma200:
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["SMA200"],
        name="SMA 200",
        line=dict(color="#00bfa5", width=1.5)
    ))

fig.update_layout(
    height=520,
    template="plotly_dark",
    paper_bgcolor="#131722",
    plot_bgcolor="#131722",
    margin=dict(l=10, r=10, t=35, b=10),
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Price",
    legend=dict(orientation="h", y=1.08),
    xaxis=dict(
        showgrid=True,
        gridcolor="#252a36"
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#252a36",
        side="right"
    )
)

st.plotly_chart(fig, use_container_width=True)

# ================= RSI =================

st.subheader("RSI Indicator")

rsi_fig = go.Figure()

rsi_fig.add_trace(go.Scatter(
    x=df.index,
    y=df["RSI"],
    name="RSI 14",
    line=dict(color="#ab47bc", width=2)
))

rsi_fig.add_hline(
    y=70,
    line_dash="dash",
    line_color="#f6465d"
)

rsi_fig.add_hline(
    y=30,
    line_dash="dash",
    line_color="#0ecb81"
)

rsi_fig.update_layout(
    height=220,
    template="plotly_dark",
    paper_bgcolor="#131722",
    plot_bgcolor="#131722",
    margin=dict(l=10, r=10, t=20, b=10),
    yaxis=dict(range=[0, 100])
)

st.plotly_chart(rsi_fig, use_container_width=True)

# ================= MARKET ANALYSIS =================

st.markdown("---")
st.subheader("🤖 TAPINU AI Market Analysis")

rsi = float(df["RSI"].iloc[-1])
ema = float(df["EMA20"].iloc[-1])

if latest > ema and rsi < 70:
    signal = "BULLISH"
    explanation = "Price is above EMA20 and RSI is below 70."
elif latest < ema and rsi > 30:
    signal = "BEARISH"
    explanation = "Price is below EMA20 and RSI is above 30."
else:
    signal = "NEUTRAL"
    explanation = "Indicators show mixed conditions."

a, b, c = st.columns(3)

a.metric("Trend Indicator", signal)
b.metric("RSI Value", f"{rsi:.2f}")
c.metric("EMA 20", f"{ema:,.2f}")

st.info(explanation)

st.caption(
    "These are rule-based educational indicators, not personalized "
    "investment advice or guaranteed BUY/SELL recommendations."
)

# ================= 7 DAY FORECAST =================

st.markdown("---")
st.subheader("🔮 7-Day Experimental AI Forecast")

if len(df) >= 30:

    prices = df["Close"].tail(30).values
    x = np.arange(len(prices))

    slope, intercept = np.polyfit(x, prices, 1)

    future_x = np.arange(len(prices), len(prices) + 8)
    predicted = slope * future_x + intercept

    future_dates = pd.bdate_range(
        start=df.index[-1] + pd.Timedelta(days=1),
        periods=8
    )

    forecast_fig = go.Figure()

    forecast_fig.add_trace(go.Scatter(
        x=df.index[-30:],
        y=prices,
        name="Historical Price",
        line=dict(color="#2962ff", width=2)
    ))

    forecast_fig.add_trace(go.Scatter(
        x=future_dates,
        y=predicted,
        name="Experimental Projection",
        line=dict(color="#f0b90b", width=2, dash="dash")
    ))

    forecast_fig.update_layout(
        height=350,
        template="plotly_dark",
        paper_bgcolor="#131722",
        plot_bgcolor="#131722",
        hovermode="x unified"
    )

    st.plotly_chart(
        forecast_fig,
        use_container_width=True
    )

    st.write(
        f"Illustrative final projection: ₹{predicted[-1]:,.2f}"
    )

    st.warning(
        "This is a simple linear-regression projection, not a reliable "
        "prediction of future prices. Actual prices may differ significantly."
    )

else:
    st.warning("Not enough historical data for forecasting.")

# ================= MARKET DATA TABLE =================

st.markdown("---")
st.subheader("📋 Stock Market Watchlist")

watchlist_data = []

for name, ticker in symbols.items():

    stock_df = get_data(ticker, "5d")

    if stock_df.empty or len(stock_df) < 2:
        continue

    p = float(stock_df["Close"].iloc[-1])
    old = float(stock_df["Close"].iloc[-2])
    pct = ((p - old) / old) * 100 if old else 0

    watchlist_data.append({
        "Stock": name,
        "Latest Close": round(p, 2),
        "Change %": round(pct, 2),
        "RSI": round(float(stock_df["RSI"].iloc[-1]), 2)
    })

if watchlist_data:
    st.dataframe(
        pd.DataFrame(watchlist_data),
        use_container_width=True,
        hide_index=True
    )

# ================= FOOTER =================

st.markdown("---")

st.caption(
    "TAPINU © 2026 | Built with Streamlit + Python + Yahoo Finance"
)

st.caption(
    "Educational market analysis only. Data availability and accuracy "
    "depend on the data provider. No guaranteed returns."
            )
        
