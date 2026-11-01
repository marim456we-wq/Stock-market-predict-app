import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="TAPINU - PRO Clear", layout="wide")

st.title("TAPINU - PRO Chart - Nalla Theriyum")
st.write("Jan 2026 to Oct 2026 - SENSEX Chart Nalla Varuthu Sir!")

ticker_choice = st.selectbox(
    "Stock",
    ["SENSEX - ^BSESN", "NIFTY - ^NSEI", "RELIANCE - RELIANCE.NS"],
    index=0
)
ticker = ticker_choice.split(" - ")[1]
period = st.selectbox("Period", ["1y", "2y", "6mo"], index=0)

@st.cache_data(ttl=60)
def load_data(t, p):
    s = yf.Ticker(t)
    return s.history(period=p, interval="1d")

data = load_data(ticker, period)
if data.empty:
    st.stop()

last = float(data["Close"].iloc[-1])
prev = float(data["Close"].iloc[-2])
chg = last - prev
chg_pct = (chg / prev * 100)

up = chg >= 0
color = "#26a69a" if up else "#ef5350"

# TOP BAR - Clear
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("SENSEX LIVE", f"{round(last,2)}", f"{round(chg,2)} ({round(chg_pct,2)}%)")
col2.metric("High", f"{round(float(data['High'].max()),2)}")
col3.metric("Low", f"{round(float(data['Low'].min()),2)}")
col4.metric("Date", f"{data.index[0].strftime('%b %Y')} to {data.index[-1].strftime('%b %Y')}")

if up:
    st.success(f"📈 YERUTHU SIR - {round(chg,2)} up Sir - Chart mela yeruthu Sir!")
else:
    st.error(f"📉 YERANGUTHU SIR - {round(chg,2)} down Sir - Chart keela yeranguthu Sir!")

# PRO CHART - Nalla Theriyum - Big Candles
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.75, 0.25])

# Candle - Big and Clear
fig.add_trace(go.Candlestick(
    x=data.index,
    open=data["Open"],
    high=data["High"],
    low=data["Low"],
    close=data["Close"],
    increasing_line_color="#26a69a",
    increasing_fillcolor="#26a69a",
    decreasing_line_color="#ef5350",
    decreasing_fillcolor="#ef5350",
    increasing_line_width=2,
    decreasing_line_width=2,
    whiskerwidth=0.3,
    name="SENSEX"
), row=1, col=1)

# MA lines for better view
fig.add_trace(go.Scatter(x=data.index, y=data["Close"].rolling(20).mean(), line=dict(color="#2962ff", width=2), name="MA20"), row=1, col=1)
fig.add_trace(go.Scatter(x=data.index, y=data["Close"].rolling(50).mean(), line=dict(color="#ff6d00", width=1.5, dash="dash"), name="MA50"), row=1, col=1)

# Volume - Perusa Nalla Theriyum
vol_colors = ["#26a69a" if c >= o else "#ef5350" for c, o in zip(data["Close"], data["Open"])]
fig.add_trace(go.Bar(x=data.index, y=data["Volume"], marker_color=vol_colors, name="Volume - 12.24M", opacity=0.8), row=2, col=1)

fig.update_layout(
    height=800,
    template="plotly_white",
    showlegend=True,
    xaxis_rangeslider_visible=False,
    title=f"{ticker} - TradingView PRO - Nalla Theriyum Chart",
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig.update_xaxes(showgrid=True, gridcolor="#e0e3eb", gridwidth=0.5, row=1, col=1)
fig.update_xaxes(title_text="Date - Jan 2026 to Oct 2026 - Oct Nov", showgrid=True, gridcolor="#e0e3eb", row=2, col=1)
fig.update_yaxes(title_text="Price - 72k to 86k", side="right", showgrid=True, gridcolor="#e0e3eb", row=1, col=1)
fig.update_yaxes(title_text="Vol - 12.24M", side="right", showgrid=False, row=2, col=1)

# Last price line
fig.add_hline(y=last, line_dash="dot", line_color=color, line_width=2, opacity=0.7, row=1, col=1, annotation_text=f" LIVE {round(last,2)} ")

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("Dolly Robot - Chart Analysis")

c1, c2 = st.columns(2)
with c1:
    st.info(f"**Chart Nalla Theriyutha?**\n\n- Jan 2026: 84k\n- Apr 2026: 72k (Yeranguthu)\n- Jul 2026: 78k (Yeruthu)\n- Oct 2026: 74k (Ippo {round(last,2)})\n\n**Full Clear Sir!**")
with c2:
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#667eea,#764ba2); padding:20px; border-radius:12px; color:white; text-align:center;'>
        <div style='font-size:30px;'>🤖</div>
        <b>Dolly: Chart Nalla Theriyuthu Sir!</b><br>
        SENSEX {round(last,2)} Sir!<br>
        {'Yeruthu Sir - BUY' if up else 'Yeranguthu Sir - WAIT'}<br>
        MA20, MA50 kooda varuthu Sir!
    </div>
    """, unsafe_allow_html=True)

st.caption("Nalla Theriyum Chart - Big Candle - MA20 MA50 - Volume Perusa - TradingView PRO")
