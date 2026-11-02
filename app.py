
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# ==================================================
# TAPINU ULTIMATE PRO
# ==================================================

st.set_page_config(
    page_title="TAPINU ULTIMATE PRO",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- THEME --------------------

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
    max-width: 1800px;
    padding-top: 1rem;
}
[data-testid="stSidebar"] {
    background: #131722;
}
[data-testid="stMetric"] {
    background: #131722;
    border: 1px solid #252a36;
    padding: 13px;
    border-radius: 10px;
}
div[data-testid="stTabs"] button {
    color: #eaecef;
}
.pro-card {
    background: #131722;
    border: 1px solid #252a36;
    border-radius: 12px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- SYMBOLS --------------------

STOCKS = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN",
    "BANK NIFTY": "^NSEBANK",
    "TCS": "TCS.NS",
    "RELIANCE": "RELIANCE.NS",
    "INFOSYS": "INFY.NS",
    "HDFC BANK": "HDFCBANK.NS",
    "ICICI BANK": "ICICIBANK.NS",
    "WIPRO": "WIPRO.NS",
    "ITC": "ITC.NS",
    "SBIN": "SBIN.NS",
    "BHARTI AIRTEL": "BHARTIARTL.NS",
    "TATA STEEL": "TATASTEEL.NS",
    "MARUTI": "MARUTI.NS",
    "LT": "LT.NS",
    "AXIS BANK": "AXISBANK.NS",
    "KOTAK BANK": "KOTAKBANK.NS",
    "TITAN": "TITAN.NS",
    "BAJFINANCE": "BAJFINANCE.NS",
    "SUN PHARMA": "SUNPHARMA.NS"
}

SECTORS = {
    "IT": ["TCS", "INFOSYS", "WIPRO"],
    "BANKING": ["HDFC BANK", "ICICI BANK", "SBIN", "AXIS BANK"],
    "AUTO": ["MARUTI"],
    "ENERGY": ["RELIANCE"],
    "FMCG": ["ITC"],
    "METALS": ["TATA STEEL"],
    "PHARMA": ["SUN PHARMA"]
}

# -------------------- DATA ENGINE --------------------

@st.cache_data(ttl=300)
def load_stock(symbol, period, interval):

    try:
        data = yf.download(
            symbol,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False
        )

        if data.empty:
            return pd.DataFrame()

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data = data.loc[:, ~data.columns.duplicated()]
        data = data.dropna(subset=["Close"]).copy()

        for col in ["Open", "High", "Low", "Close", "Volume"]:
            if col not in data.columns:
                if col == "Volume":
                    data[col] = 0
                else:
                    return pd.DataFrame()
            data[col] = pd.to_numeric(data[col], errors="coerce")

        data = data.dropna(subset=["Close"])

        close = data["Close"]

        # Moving averages
        data["EMA20"] = close.ewm(span=20, adjust=False).mean()
        data["EMA50"] = close.ewm(span=50, adjust=False).mean()
        data["SMA200"] = close.rolling(200).mean()

        # RSI
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(alpha=1/14, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1/14, adjust=False).mean()

        rs = avg_gain / avg_loss.replace(0, np.nan)
        data["RSI"] = 100 - (100 / (1 + rs))
        data["RSI"] = data["RSI"].fillna(50)

        # MACD
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()

        data["MACD"] = ema12 - ema26
        data["SIGNAL"] = data["MACD"].ewm(
            span=9, adjust=False
        ).mean()
        data["HIST"] = data["MACD"] - data["SIGNAL"]

        # Bollinger Bands
        middle = close.rolling(20).mean()
        std = close.rolling(20).std()

        data["BB_UPPER"] = middle + 2 * std
        data["BB_LOWER"] = middle - 2 * std

        # Returns
        data["RETURN"] = close.pct_change() * 100

        return data

    except Exception:
        return pd.DataFrame()


# -------------------- SIDEBAR --------------------

st.sidebar.markdown("# 📈 TAPINU")
st.sidebar.caption("ULTIMATE PRO TERMINAL")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Advanced Chart",
        "Stock Screener",
        "Sector Heatmap",
        "AI Lab",
        "Paper Portfolio",
        "Price Alerts"
    ]
)

st.sidebar.markdown("---")

selected = st.sidebar.selectbox(
    "Select Stock",
    list(STOCKS.keys()),
    index=0
)

timeframes = {
    "1 Minute": ("1d", "1m"),
    "5 Minutes": ("5d", "5m"),
    "15 Minutes": ("1mo", "15m"),
    "1 Hour": ("6mo", "1h"),
    "1 Day": ("1y", "1d"),
    "1 Week": ("5y", "1wk")
}

selected_tf = st.sidebar.selectbox(
    "Chart Timeframe",
    list(timeframes.keys()),
    index=4
)

period, interval = timeframes[selected_tf]

st.sidebar.caption(
    "Intraday availability depends on Yahoo Finance."
)

# -------------------- HEADER --------------------

st.markdown("# 📈 TAPINU ULTIMATE PRO")
st.caption(
    "INDIAN MARKET INTELLIGENCE • ADVANCED ANALYTICS"
)

st.markdown(
    f"Last dashboard refresh: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

# -------------------- MAIN DATA --------------------

symbol = STOCKS[selected]
df = load_stock(symbol, period, interval)

if df.empty:
    st.error("Market data unavailable. Try another stock or timeframe.")
    st.stop()

latest = float(df["Close"].iloc[-1])
previous = float(df["Close"].iloc[-2]) if len(df) > 1 else latest
change = latest - previous
change_pct = (change / previous * 100) if previous else 0

# -------------------- CHART ENGINE --------------------

def create_chart(data, chart_type="Candlestick",
                 ema20=True, ema50=True,
                 sma200=False, bollinger=False):

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.75, 0.25]
    )

    if chart_type == "Candlestick":
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name="Price",
                increasing_line_color="#0ecb81",
                decreasing_line_color="#f6465d"
            ),
            row=1, col=1
        )
    elif chart_type == "Area":
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                name="Price",
                fill="tozeroy",
                line=dict(color="#2962ff", width=2)
            ),
            row=1, col=1
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                name="Price",
                line=dict(color="#2962ff", width=2)
            ),
            row=1, col=1
        )

    indicators = [
        (ema20, "EMA20", "#ffb74d"),
        (ema50, "EMA50", "#ab47bc"),
        (sma200, "SMA200", "#00bfa5")
    ]

    for enabled, column, color in indicators:
        if enabled:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data[column],
                    name=column,
                    line=dict(color=color, width=1.3)
                ),
                row=1, col=1
            )

    if bollinger:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["BB_UPPER"],
                name="BB Upper",
                line=dict(color="#78909c", width=1, dash="dot")
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["BB_LOWER"],
                name="BB Lower",
                line=dict(color="#78909c", width=1, dash="dot")
            ),
            row=1, col=1
        )

    colors = np.where(
        data["Close"] >= data["Open"],
        "#0ecb81",
        "#f6465d"
    )

    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["Volume"],
            name="Volume",
            marker_color=colors
        ),
        row=2, col=1
    )

    fig.update_layout(
        template="plotly_dark",
        height=650,
        paper_bgcolor="#131722",
        plot_bgcolor="#131722",
        margin=dict(l=10, r=10, t=35, b=10),
        hovermode="x unified",
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", y=1.04),
        dragmode="pan"
    )

    fig.update_xaxes(
        gridcolor="#252a36",
        showgrid=True,
        rangeselector=dict(
            buttons=[
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(step="all", label="ALL")
            ]
        ),
        row=1, col=1
    )

    fig.update_yaxes(
        gridcolor="#252a36",
        side="right"
    )

    return fig


# ==================================================
# PAGE 1: DASHBOARD
# ==================================================

if page == "Dashboard":

    st.subheader("Market Overview")

    names = ["NIFTY 50", "SENSEX", "BANK NIFTY", "TCS"]

    cols = st.columns(4)

    for col, name in zip(cols, names):

        market = load_stock(STOCKS[name], "5d", "1d")

        with col:
            if len(market) >= 2:
                p = float(market["Close"].iloc[-1])
                old = float(market["Close"].iloc[-2])
                pct = (p - old) / old * 100 if old else 0
                col.metric(name, f"{p:,.2f}", f"{pct:+.2f}%")
            else:
                col.metric(name, "Unavailable")

    st.markdown("---")

    st.subheader(f"{selected} • Market Chart")

    st.metric(
        "Latest Available Price",
        f"₹{latest:,.2f}",
        f"{change_pct:+.2f}%"
    )

    st.plotly_chart(
        create_chart(df, "Candlestick"),
        use_container_width=True
    )

    st.subheader("Technical Indicators")

    a, b, c, d = st.columns(4)

    a.metric("RSI", f"{df['RSI'].iloc[-1]:.2f}")
    b.metric("MACD", f"{df['MACD'].iloc[-1]:.2f}")
    c.metric("EMA 20", f"{df['EMA20'].iloc[-1]:,.2f}")
    d.metric("EMA 50", f"{df['EMA50'].iloc[-1]:,.2f}")

    st.subheader("Market Watchlist")

    rows = []

    for name, ticker in STOCKS.items():

        stock = load_stock(ticker, "5d", "1d")

        if len(stock) >= 2:
            p = float(stock["Close"].iloc[-1])
            old = float(stock["Close"].iloc[-2])

            rows.append({
                "Stock": name,
                "Price": round(p, 2),
                "Change %": round((p-old)/old*100, 2)
            })

    if rows:
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# PAGE 2: ADVANCED CHART
# ==================================================

elif page == "Advanced Chart":

    st.subheader("Professional Chart Terminal")

    chart_type = st.selectbox(
        "Chart Style",
        ["Candlestick", "Line", "Area"]
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        ema20 = st.checkbox("EMA 20", True)

    with c2:
        ema50 = st.checkbox("EMA 50", True)

    with c3:
        sma200 = st.checkbox("SMA 200", False)

    with c4:
        bollinger = st.checkbox("Bollinger Bands", False)

    st.plotly_chart(
        create_chart(
            df,
            chart_type,
            ema20,
            ema50,
            sma200,
            bollinger
        ),
        use_container_width=True,
        config={
            "scrollZoom": True,
            "displaylogo": False,
            "responsive": True,
            "modeBarButtonsToAdd": ["drawline", "drawrect", "eraseshape"]
        }
    )

    st.subheader("MACD Analysis")

    macd_fig = go.Figure()

    macd_fig.add_trace(go.Scatter(
        x=df.index,
        y=df["MACD"],
        name="MACD",
        line=dict(color="#2962ff")
    ))

    macd_fig.add_trace(go.Scatter(
        x=df.index,
        y=df["SIGNAL"],
        name="Signal",
        line=dict(color="#ffb74d")
    ))

    macd_fig.update_layout(
        template="plotly_dark",
        height=280,
        paper_bgcolor="#131722",
        plot_bgcolor="#131722"
    )

    st.plotly_chart(macd_fig, use_container_width=True)

    st.subheader("RSI Analysis")

    rsi_fig = go.Figure()

    rsi_fig.add_trace(go.Scatter(
        x=df.index,
        y=df["RSI"],
        name="RSI",
        line=dict(color="#ab47bc", width=2)
    ))

    rsi_fig.add_hline(y=70, line_dash="dash")
    rsi_fig.add_hline(y=30, line_dash="dash")

    rsi_fig.update_layout(
        template="plotly_dark",
        height=250,
        paper_bgcolor="#131722",
        plot_bgcolor="#131722",
        yaxis=dict(range=[0, 100])
    )

    st.plotly_chart(rsi_fig, use_container_width=True)


# ==================================================
# PAGE 3: STOCK SCREENER
# ==================================================

elif page == "Stock Screener":

    st.subheader("🔎 Advanced Stock Screener")

    screen_rows = []

    with st.spinner("Scanning stocks..."):

        for name, ticker in STOCKS.items():

            stock = load_stock(ticker, "1y", "1d")

            if len(stock) < 2:
                continue

            p = float(stock["Close"].iloc[-1])
            old = float(stock["Close"].iloc[-2])
            pct = (p-old)/old*100 if old else 0
            rsi = float(stock["RSI"].iloc[-1])

            screen_rows.append({
                "Stock": name,
                "Price": round(p, 2),
                "Change %": round(pct, 2),
                "RSI": round(rsi, 2),
                "EMA20": round(float(stock["EMA20"].iloc[-1]), 2),
                "EMA50": round(float(stock["EMA50"].iloc[-1]), 2)
            })

    if screen_rows:

        screen_df = pd.DataFrame(screen_rows)

        filter_type = st.selectbox(
            "Screening Filter",
            [
                "All Stocks",
                "Top Gainers",
                "Top Losers",
                "RSI Below 30",
                "RSI Above 70",
                "Above EMA20"
            ]
        )

        if filter_type == "Top Gainers":
            screen_df = screen_df.sort_values(
                "Change %", ascending=False
            )

        elif filter_type == "Top Losers":
            screen_df = screen_df.sort_values(
                "Change %", ascending=True
            )

        elif filter_type == "RSI Below 30":
            screen_df = screen_df[screen_df["RSI"] < 30]

        elif filter_type == "RSI Above 70":
            screen_df = screen_df[screen_df["RSI"] > 70]

        elif filter_type == "Above EMA20":
            screen_df = screen_df[
                screen_df["Price"] > screen_df["EMA20"]
            ]

        st.dataframe(
            screen_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("No screening data available.")


# ==================================================
# PAGE 4: SECTOR HEATMAP
# ==================================================

elif page == "Sector Heatmap":

    st.subheader("Market Sector Heatmap")

    heat_rows = []

    for sector, members in SECTORS.items():

        for name in members:

            stock = load_stock(STOCKS[name], "5d", "1d")

            if len(stock) >= 2:

                p = float(stock["Close"].iloc[-1])
                old = float(stock["Close"].iloc[-2])

                pct = (p-old)/old*100 if old else 0

                heat_rows.append({
                    "Sector": sector,
                    "Stock": name,
                    "Change": round(pct, 2)
                })

    if heat_rows:

        heat_df = pd.DataFrame(heat_rows)

        fig = go.Figure(go.Treemap(
            labels=heat_df["Stock"],
            parents=heat_df["Sector"],
            values=[1] * len(heat_df),
            marker=dict(
                colors=heat_df["Change"],
                colorscale=[
                    [0, "#f6465d"],
                    [0.5, "#252a36"],
                    [1, "#0ecb81"]
                ],
                cmid=0,
                colorbar=dict(title="Change %")
            ),
            customdata=heat_df[["Change"]],
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Change: %{customdata[0]:.2f}%"
                "<extra></extra>"
            )
        ))

        fig.update_layout(
            template="plotly_dark",
            height=550,
            paper_bgcolor="#131722"
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(heat_df, use_container_width=True)

    else:
        st.warning("Sector data unavailable.")


# ==================================================
# PAGE 5: AI LAB
# ==================================================

elif page == "AI Lab":

    st.subheader("🤖 TAPINU AI Research Lab")

    st.caption(
        "Experimental statistical analysis, not guaranteed predictions."
    )

    if len(df) >= 30:

        prices = df["Close"].tail(60).dropna().values
        x = np.arange(len(prices))

        slope, intercept = np.polyfit(x, prices, 1)

        future_x = np.arange(len(prices), len(prices)+8)
        predicted = slope*future_x + intercept

        future_dates = pd.bdate_range(
            start=df.index[-1] + pd.Timedelta(days=1),
            periods=8
        )

        forecast = go.Figure()

        forecast.add_trace(go.Scatter(
            x=df.index[-len(prices):],
            y=prices,
            name="Historical",
            line=dict(color="#2962ff", width=2)
        ))

        forecast.add_trace(go.Scatter(
            x=future_dates,
            y=predicted,
            name="Experimental Projection",
            line=dict(color="#f0b90b", dash="dash", width=2)
        ))

        forecast.update_layout(
            template="plotly_dark",
            height=400,
            paper_bgcolor="#131722",
            plot_bgcolor="#131722"
        )

        st.plotly_chart(forecast, use_container_width=True)

        rsi = float(df["RSI"].iloc[-1])
        ema = float(df["EMA20"].iloc[-1])
        macd = float(df["MACD"].iloc[-1])
        signal_line = float(df["SIGNAL"].iloc[-1])

        trend_score = 0

        if latest > ema:
            trend_score += 1

        if macd > signal_line:
            trend_score += 1

        if rsi > 50:
            trend_score += 1

        st.metric("Trend Conditions", f"{trend_score}/3")
        st.metric("Current RSI", f"{rsi:.2f}")

        st.write("### Research interpretation")

        if trend_score == 3:
            st.success("Positive indicator alignment")
        elif trend_score == 0:
            st.warning("Negative indicator alignment")
        else:
            st.info("Mixed indicator conditions")

        st.write(
            f"Illustrative 7-session final projection: "
            f"₹{predicted[-1]:,.2f}"
        )

        st.warning(
            "Linear regression is a simple statistical baseline. "
            "It is not a validated AI trading model. Forecasts can be wrong."
        )

    else:
        st.warning("Insufficient historical data.")


# ==================================================
# PAGE 6: PAPER PORTFOLIO
# ==================================================

elif page == "Paper Portfolio":

    st.subheader("💼 Paper Portfolio Tracker")

    st.info(
        "Practice tracking hypothetical investments. "
        "This does not place re
