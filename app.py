import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="TAPINU - 3D CANDLE BAR", layout="wide", page_icon="💎")

st.title("💎 3D CANDLE BAR - Building Maathiri Nikkum Sir!")
st.caption("Candle ellam 3D Bar ah - Green Red Building Sir!")

choice = st.selectbox("Stock", ["SENSEX - ^BSESN", "NIFTY - ^NSEI", "RELIANCE - RELIANCE.NS"], index=0)
ticker = choice.split(" - ")[1]
period = st.selectbox("Period", ["1mo", "3mo", "6mo"], index=1)

@st.cache_data(ttl=60)
def load_data(t, p):
    s = yf.Ticker(t)
    return s.history(period=p, interval="1d")

data = load_data(ticker, period)
if data.empty:
    st.stop()

# Take last 30 candles for clear 3D view
data = data.tail(30)

last = float(data["Close"].iloc[-1])

# Function to create 3D Box (Candle Body)
def cuboid(x0, x1, y0, y1, z0, z1, color):
    # 8 vertices
    X = [x0, x1, x1, x0, x0, x1, x1, x0]
    Y = [y0, y0, y1, y1, y0, y0, y1, y1]
    Z = [z0, z0, z0, z0, z1, z1, z1, z1]
    # faces
    i = [0,0,0,0,1,1,2,2,3,3,4,6]
    j = [1,2,3,4,2,6,3,7,4,7,5,7]
    k = [2,3,4,5,6,7,7,4,7,5,6,5]
    return go.Mesh3d(x=X, y=Y, z=Z, i=i, j=j, k=k, color=color, opacity=0.85, flatshading=True)

fig = go.Figure()

for idx in range(len(data)):
    o = float(data["Open"].iloc[idx])
    c = float(data["Close"].iloc[idx])
    h = float(data["High"].iloc[idx])
    l = float(data["Low"].iloc[idx])
    
    is_green = c >= o
    col = "#00ff88" if is_green else "#ff4444"
    
    x0 = idx - 0.3
    x1 = idx + 0.3
    y0 = -0.3
    y1 = 0.3
    z0 = min(o, c)
    z1 = max(o, c)
    
    # Body - 3D Bar
    fig.add_trace(cuboid(x0, x1, y0, y1, z0, z1, col))
    
    # Wick - High to Low line
    fig.add_trace(go.Scatter3d(
        x=[idx, idx],
        y=[0, 0],
        z=[l, h],
        mode='lines',
        line=dict(color=col, width=8),
        showlegend=False,
        hoverinfo='skip'
    ))

# Volume bars at bottom
vol = data["Volume"].values / data["Volume"].max() * 500  # scale
for idx in range(len(data)):
    v = vol[idx]
    fig.add_trace(cuboid(idx-0.3, idx+0.3, 1, 1.6, 0, v, "#4a90e2"))

fig.update_layout(
    height=800,
    scene=dict(
        xaxis=dict(title="Time - Jan to Oct", showgrid=True, gridcolor="#333"),
        yaxis=dict(title="Width", showgrid=False, visible=False),
        zaxis=dict(title=f"Price - {int(data['Low'].min())} to {int(data['High'].max())}", showgrid=True, gridcolor="#333"),
        bgcolor="#0a0e1a",
        camera=dict(eye=dict(x=1.7, y=-1.5, z=0.8)),
        aspectmode="manual",
        aspectratio=dict(x=2.5, y=0.5, z=1)
    ),
    paper_bgcolor="#0a0e1a",
    plot_bgcolor="#0a0e1a",
    title=f"{ticker} - 3D CANDLE BARS - {len(data)} Candles - Building Maathiri - Green Yeruthu Red Yeranguthu",
    showlegend=False,
    font=dict(color="white")
)

# Add ground grid
fig.update_layout(scene_xaxis_gridcolor="#1a2332", scene_yaxis_gridcolor="#1a2332", scene_zaxis_gridcolor="#1a2332")

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.success(f"**3D CANDLE BAR READY SIR!**\n\n- Green Bar = Yeruthu Sir (Close > Open)\n- Red Bar = Yeranguthu Sir (Close < Open)\n- Height = Open to Close Sir\n- Wick = High to Low Sir\n- Blue Bar = Volume Sir\n\nMouse vechu suthi paarkalam Sir!")
with col2:
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#00ff88,#00cc6a); padding:20px; border-radius:15px; color:black; text-align:center; font-weight:bold;'>
        <div style='font-size:30px;'>🤖💎</div>
        Dolly: 3D Candle Bar Mass Sir!<br>
        SENSEX {round(last,2)} Sir!<br>
        Building maathiri nikkuthu Sir!<br>
        Rotate Pannunga Sir!
    </div>
    """, unsafe_allow_html=True)

st.info("💎 Tip: Mouse left click drag panni rotate pannalam Sir, Scroll panni zoom pannalam Sir, Right click drag panni move pannalam Sir - Full 3D Sir!")
st.caption("3D CANDLE BAR - TradingView kooda illa Sir - TAPINU First Sir - Building Maathiri Candle Sir!")
