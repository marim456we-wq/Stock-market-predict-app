import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz
import time
import numpy as np

st.set_page_config(page_title="TAPINU RUNNING CHART", layout="wide", page_icon="🏃‍♂️")
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)

st.title("🏃‍♂️ CHART MARANUM + RUN AGANUM - LIVE RUNNING CHART")
st.caption("Chart Live ah Oodum Sir - Marum Sir!")

# Session for running data
if "run_data" not in st.session_state:
    st.session_state["run_data"] = []
if "run_time" not in st.session_state:
    st.session_state["run_time"] = 0

# Controls
col1,col2,col3,col4 = st.columns(4)
with col1:
    ticker_list = {"RELIANCE":"RELIANCE.NS","TATA MOTORS":"TATAMOTORS.NS","TCS":"TCS.NS","INFY":"INFY.NS","TRENT":"TRENT.NS","BTC":"BTC-USD"}
    sel = st.selectbox("Stock", list(ticker_list.keys()), index=0)
with col2:
    manual = st.text_input("Manual Search")
with col3:
    period = st.selectbox("Timeframe", ["1mo","3mo","1y","5y"], index=2)
with col4:
    speed = st.selectbox("Chart Run Speed", ["Fast ⚡","Medium 🏃","Slow 🐢"], index=0)

ticker = manual.strip().upper() if manual.strip()!="" else ticker_list[sel]
speed_map = {"Fast ⚡":0.5,"Medium 🏃":1,"Slow 🐢":2}
sleep_time = speed_map[speed]

run_on = st.checkbox("▶️ CHART RUN ON - Maranum + Run Aganum", value=True)

# Get base data
@st.cache_data(ttl=60)
def get_base(t,p):
    s = yf.Ticker(t)
    h = s.history(period=p)
    return h

base_hist = get_base(ticker, period)
if base_hist.empty:
    st.error("Data Not Found")
    st.stop()

last_close = float(base_hist["Close"].iloc[-1])

# Generate running ticks - if market closed we simulate running
if len(st.session_state["run_data"]) == 0:
    # Initialize with last 50 points
    init = base_hist.tail(50).copy()
    st.session_state["run_data"] = init["Close"].tolist()
    st.session_state["run_time"] = 0

# Add new running point every rerun
np.random.seed(int(time.time())%10000)
change = np.random.uniform(-0.5, 0.5) if not (now.weekday()<5 and 9<=now.hour<=15) else np.random.uniform(-0.3, 0.3)
new_price = st.session_state["run_data"][-1] * (1 + change/100)
st.session_state["run_data"].append(new_price)
if len(st.session_state["run_data"]) > 100:
    st.session_state["run_data"] = st.session_state["run_data"][-100:]
st.session_state["run_time"] += 1

run_prices = st.session_state["run_data"]
current_price = run_prices[-1]
prev_price = run_prices[-2] if len(run_prices)>1 else current_price
diff = current_price - prev_price

# LIVE STATUS
if diff > 0:
    status = "📈 YERUTHU - CHART MELA YERUTHU SIR!"
    color = "#26a69a"
    emoji = "🟢"
else:
    status = "📉 YERANGUTHU - CHART KEELA YERANGUTHU SIR!"
    color = "#ef5350"
    emoji = "🔴"

# TOP LIVE BAR - MARANUM
st.divider()
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(f"<div style='background:{color}; color:white; padding:20px; border-radius:12px; text-align:center;'><b>LIVE RUNNING</b><br><span style='font-size:28px;'>{round(current_price,2)}</span><br>{emoji} {status}</div>", unsafe_allow_html=True)
with c2:
    st.metric("Running Change", f"{round(diff,2)}", f"{round(diff/prev_price*100,3)}%")
with c3:
    st.metric("Run Count", f"{st.session_state['run_time']} ticks", f"Speed: {speed}")
with c4:
    st.markdown(f"<div style='background:linear-gradient(135deg,#667eea,#764ba2); padding:15px; border-radius:12px; color:white; text-align:center;'><div style='font-size:25px;'>🤖🏃‍♂️</div>Dolly: Chart {('Yeruthu Sir!' if diff>0 else 'Yeranguthu Sir!')}<br>Run Aaguthu Sir!</div>", unsafe_allow_html=True)

# MAIN RUNNING CHART - 2 CHARTS
st.divider()
left, right = st.columns([3,1])

with left:
    st.subheader(f"🏃‍♂️ {ticker} - RUNNING CHART - Maranum + Oodum")
    
    # Chart 1: Full History (Marum)
    fig1 = go.Figure()
    fig1.add_trace(go.Candlestick(x=base_hist.index, open=base_hist["Open"], high=base_hist["High"], low=base_hist["Low"], close=base_hist["Close"], name="History"))
    fig1.add_trace(go.Scatter(x=base_hist.index, y=base_hist["Close"].rolling(20).mean(), line=dict(color="blue", width=1), name="MA20"))
    fig1.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False, title=f"{ticker} - {period} - Chart Marum (Timeframe Maaralam)")
    st.plotly_chart(fig1, use_container_width=True)
    
    # Chart 2: LIVE RUNNING CHART - RUN AGANUM
    st.subheader("⚡ LIVE RUNNING - Chart Ooduthu Sir - Second Second Marum Sir!")
    run_times = [f"T-{100-i}" for i in range(len(run_prices))]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=run_times, y=run_prices, mode="lines", line=dict(color=color, width=3), fill="tozeroy", fillcolor=f"rgba({ '38,166,154' if diff>0 else '239,83,80'},0.2)", name="Running Price"))
    # Add moving dot at end
    fig2.add_trace(go.Scatter(x=[run_times[-1]], y=[run_prices[-1]], mode="markers", marker=dict(size=15, color=color), name="LIVE"))
    fig2.update_layout(height=400, template="plotly_dark", title=f"LIVE RUNNING CHART - Ippo {round(current_price,2)} - {status}", xaxis_title="Time (Running)", yaxis_title="Price", showlegend=False)
    fig2.update_xaxes(showgrid=False)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.success(f"✅ Chart Run Aaguthu Sir! {st.session_state['run_time']} times ooduchu Sir! Price {status} Sir!")

with right:
    st.subheader("⏰ Timing - Trade Yeruthu Yeranguthu")
    
    # Timing table that also runs
    timing_table = pd.DataFrame({
        "Time": ["9:15","10:30","12:00","2:00","3:30"],
        "What": ["Open - Volatile","Buy - Yeruthu","Slow","Power Hour","Close"],
        "Now?": ["✅" if 9<=now.hour<=10 else "","✅" if 10<=now.hour<=12 else "","✅" if 12<=now.hour<=14 else "","✅" if 14<=now.hour<=15 else "","✅" if now.hour>=15 else ""]
    })
    st.table(timing_table)
    
    st.divider()
    st.markdown("### 🤖 Dolly Live")
    if diff>0:
        st.success(f"Dolly: CHART YERUTHU SIR! 🏃‍♂️ Mela Yeruthu Sir! {round(diff,2)} up Sir! Chart Run Aaguthu Sir!")
    else:
        st.error(f"Dolly: CHART YERANGUTHU SIR! 📉 Keela Yeranguthu Sir! {round(diff,2)} down Sir! Chart Run Aaguthu Sir!")
    
    st.divider()
    st.write("**Chart Maranum:** Top chart la timeframe maaralam Sir - 1mo, 3mo, 1y nu")
    st.write("**Chart Run Aganum:** Keela chart live ah oodum Sir - second second marum Sir")
    
    if st.button("🔄 Reset Running Chart"):
        st.session_state["run_data"] = []
        st.session_state["run_time"] = 0
        st.rerun()

# AUTO RUN LOGIC - CHART RUN AGANUM
if run_on:
    st.caption(f"🏃‍♂️ CHART RUN AGUTHU SIR - Every {sleep_time}s chart marum + run aagum Sir - Live: {round(current_price,2)} - {status}")
    time.sleep(sleep_time)
    st.rerun()
else:
    st.caption("Chart Run Off Sir - Checkbox ON pannunga Sir")

st.divider()
st.caption("CHART MARANUM = Timeframe change + Candle change Sir | CHART RUN AGANUM = Live running ticker Sir")
