import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="TAPINU - Line Only", layout="wide")

st.markdown("### 📈 TAPINU - Real Time Line - Candle Cancelled")

symbol_input = st.text_input("Stock Symbol", value="TCS.NS")
symbol = symbol_input.strip().upper()
if symbol == "":
    symbol = "TCS.NS"

c1, c2, c3, c4 = st.columns(4)
if c1.button("TCS"): symbol = "TCS.NS"
if c2.button("RELIANCE"): symbol = "RELIANCE.NS"
if c3.button("SENSEX"): symbol = "^BSESN"
if c4.button("NIFTY"): symbol = "^NSEI"

ticker = yf.Ticker(symbol)
daily = ticker.history(period="3mo", interval="1d")
intraday = ticker.history(period="1d", interval="5m")

if len(daily) == 0:
    st.error("Data not found")
    st.stop()

last_price = float(daily["Close"].iloc[-1])
prev = float(daily["Close"].iloc[-2]) if len(daily) > 1 else last_price
change = last_price - prev
pct = (change/prev*100) if prev != 0 else 0
is_up = change >= 0
color = "#26a69a" if is_up else "#ef5350"

# Price Card - Simple
st.markdown(f"""
<div style='background:white; border:1px solid #e0e3eb; border-radius:12px; padding:14px; display:flex; justify-content:space-between; align-items:center;'>
    <div>
        <div style='font-size:12px; color:#9598a1;'>NSE • {symbol}</div>
        <div style='font-size:30px; font-weight:700; color:#131722;'>{round(last_price,2)} <span style='font-size:16px; color:{color};'>▲ {round(change,2)} ({round(pct,2)}%)</span></div>
    </div>
    <div style='background:{color}; color:white; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:700;'>LIVE UP</div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# CANDLE CANCELLED - ONLY CLEAN LINE CHART
st.markdown(f"**{symbol} - Clean Line Chart - 3 Months**")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=daily.index,
    y=daily["Close"],
    mode="lines",
    line=dict(color=color, width=2.5, shape="spline", smoothing=0.9),
    fill="tozeroy",
    fillcolor=f"rgba({ '38,166,154' if is_up else '239,83,80'}, 0.15)",
    name="Price",
    hovertemplate="%{x}<br>Price: %{y:.2f}<extra></extra>"
))

fig.update_layout(
    height=450,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=10, r=60, t=10, b=30),
    showlegend=False,
    xaxis=dict(
        showgrid=True,
        gridcolor="#f0f3fa",
        rangeslider_visible=False,
        tickfont=dict(size=11, color="#9598a1"),
        linecolor="#e0e3eb"
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#f0f3fa",
        side="right",
        tickfont=dict(size=11, color="#131722"),
        linecolor="#e0e3eb"
    ),
    hovermode="x",
    hoverlabel=dict(bgcolor="white", bordercolor="#e0e3eb")
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# Today Live - If Available
if len(intraday) > 3:
    st.markdown(f"**Today Live - 5Min Line**")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=intraday.index,
        y=intraday["Close"],
        mode="lines",
        line=dict(color=color, width=2.2, shape="spline", smoothing=0.8),
        fill="tozeroy",
        fillcolor=f"rgba({ '38,166,154' if is_up else '239,83,80'}, 0.12)"
    ))
    fig2.update_layout(
        height=300,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=60, t=10, b=30),
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor="#f0f3fa", tickfont=dict(size=10, color="#9598a1"), tickformat="%H:%M"),
        yaxis=dict(showgrid=True, gridcolor="#f0f3fa", side="right", tickfont=dict(size=11)),
        hovermode="x"
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

if st.button("🔄 Refresh"):
    st.rerun()

st.caption("Candle Chart Cancelled - Only Clean Line Chart - Professional Look")
