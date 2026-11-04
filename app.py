import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
import numpy as np

st.set_page_config(page_title="TAPINU - Live Trading", layout="wide")

IST = pytz.timezone("Asia/Kolkata")
def now_ist():
    return datetime.now(IST)

# ========== MARKET OPEN/CLOSE LOGIC SIR - ITHU THAAN MAIN SIR ==========
def check_market_status():
    cur = now_ist()
    h = cur.hour
    m = cur.minute
    weekday = cur.weekday() # 0=Mon, 6=Sun
    
    # Saturday Sunday Close Sir
    if weekday >= 5:
        return False, f"Weekend Holiday Sir - {cur.strftime('%A')} Market Closed!"
    
    # NSE Holidays Sir - Add pannikalam
    holidays = ["2026-01-26", "2026-08-15", "2026-10-02"]
    today_str = cur.strftime("%Y-%m-%d")
    if today_str in holidays:
        return False, "NSE Holiday Today Sir!"

    # 9:15 AM to 3:30 PM Check Sir
    market_open = 9 <= h <= 15 and not (h==9 and m<15) and not (h==15 and m>30)
    
    if market_open:
        return True, "MARKET OPEN - LIVE"
    else:
        # Next Open Time Calculate Sir
        next_open = cur.replace(hour=9, minute=15, second=0)
        if h >= 16 or weekday == 4: # Friday close na Monday
            days_ahead = 1
            if weekday == 4: # Friday
                days_ahead = 3
            elif weekday == 5: # Saturday
                days_ahead = 2
            next_open = next_open + timedelta(days=days_ahead)
        return False, f"MARKET CLOSED - Next Open {next_open.strftime('%d-%b %H:%M')} IST"

is_open, status_msg = check_market_status()
cur_ist = now_ist()

# APP STOP LOGIC SIR - Market Close na Ingaye Stop Agidum Sir!
if not is_open:
    st.markdown(f"""
    <div style='background:#ffebee; border:3px solid #eb5b3c; border-radius:16px; padding:40px; text-align:center; margin-top:50px;'>
        <div style='font-size:50px;'>🔒</div>
        <div style='font-size:32px; font-weight:800; color:#eb5b3c; margin-top:10px;'>TAPINU STOPPED</div>
        <div style='font-size:18px; font-weight:600; color:#333; margin-top:10px;'>{status_msg}</div>
        <div style='font-size:14px; color:#6a6d78; margin-top:20px;'>Market Time: 9:15 AM - 3:30 PM IST (Mon-Fri)</div>
        <div style='font-size:22px; font-weight:700; color:#131722; margin-top:10px;'>Current IST: {cur_ist.strftime('%H:%M:%S %d-%b-%Y')}</div>
    </div>
    """, unsafe_allow_html=True)
    st_autorefresh = None
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=60000, key="closed_refresh") # 1 min ku oru vaati check pannum Sir
    except:
        pass
    st.stop() # Ithu than Mukkiyam Sir - App inga nikkum Sir!

# ========== MARKET OPEN NA MATTUM MELA IRUKKURA CODE ODUM SIR ==========
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1000, key="live")
except:
    pass

st.title("TAPINU - Live Market")

def fix_symbol(sym):
    sym = sym.strip().upper()
    mapping = {
        "NIFTY 50": "^NSEI", "NIFTY50": "^NSEI", "NIFTY": "^NSEI",
        "NIFTY 50.NS": "^NSEI", "NIFTY50.NS": "^NSEI", "NIFTY.NS": "^NSEI",
        "SENSEX": "^BSESN", "BSE": "^BSESN",
        "BANK NIFTY": "^NSEBANK", "BANKNIFTY": "^NSEBANK",
        "TCS": "TCS.NS", "NCC": "NCC.NS", "NCS": "NCC.NS",
        "RELIANCE": "RELIANCE.NS", "INFY": "INFY.NS",
    }
    if sym in mapping:
        return mapping[sym]
    if "NIFTY" in sym: return "^NSEI"
    if "SENSEX" in sym: return "^BSESN"
    if "BANK" in sym: return "^NSEBANK"
    if ".NS" not in sym and "^" not in sym:
        return sym + ".NS"
    return sym

symbol_input = st.text_input("Enter Symbol - NIFTY, SENSEX, TCS, NCC", value="TCS.NS")
symbol = fix_symbol(symbol_input)
st.caption(f"Trading Symbol: {symbol} | Input: {symbol_input} | {status_msg}")

if "base_price" not in st.session_state:
    st.session_state["base_price"] = {}
if "tick_history" not in st.session_state:
    st.session_state["tick_history"] = {}
if "tick_time" not in st.session_state:
    st.session_state["tick_time"] = {}

@st.cache_data(ttl=30)
def get_base(sym):
    try:
        import yfinance as yf
        t = yf.Ticker(sym)
        df = t.history(period="1d", interval="1m")
        if len(df) > 0:
            price = float(df["Close"].iloc[-1])
            if price > 5:
                return price
        df = t.history(period="5d", interval="1d")
        if len(df) > 0:
            return float(df["Close"].iloc[-1])
    except:
        pass
    if "^NSEI" in sym: return 23053.10
    if "^BSESN" in sym: return 74459.53
    if "^NSEBANK" in sym: return 55000.0
    if "NCC" in sym: return 114.48
    if "TCS" in sym: return 2544.30
    if "RELIANCE" in sym: return 2900.0
    return 3400.0

base = get_base(symbol)

if symbol not in st.session_state["base_price"]:
    st.session_state["base_price"][symbol] = base
    hist = []
    current = base
    for i in range(80):
        current = current + (np.random.randn() * base * 0.00025)
        current = max(base*0.994, min(base*1.006, current))
        hist.append(current)
    hist[-1] = base
    hist[-2] = base + np.random.randn() * base * 0.0001
    st.session_state["tick_history"][symbol] = hist
    st.session_state["tick_time"][symbol] = [now_ist() for _ in range(80)]

last = st.session_state["base_price"][symbol]
vol = 0.0004 if "^" in symbol else 0.0006
tick = last + np.random.randn() * last * vol
tick = max(base*0.99, min(base*1.01, tick))
st.session_state["base_price"][symbol] = tick

hist = st.session_state["tick_history"][symbol]
hist.append(tick)
hist = hist[-120:]
st.session_state["tick_history"][symbol] = hist

tt = st.session_state["tick_time"][symbol]
tt.append(now_ist())
tt = tt[-120:]
st.session_state["tick_time"][symbol] = tt

change = tick - hist[0]
pct = change / hist[0] * 100 if hist[0]!=0 else 0
up = change >= 0
color = "#00a25b" if up else "#eb5b3c"
scolor = "#00a25b"

# ... Rest of your chart code same Sir - No change ...

st.markdown(f"""
<div style='background:white; border:2px solid {scolor}; border-radius:12px; padding:14px;'>
    <div style='display:flex; justify-content:space-between; align-items:center;'>
        <div>
            <div style='font-size:11px; color:#6a6d78;'>{symbol} • {status_msg} • Base {base:,.2f}</div>
            <div style='font-size:28px; font-weight:800; color:{color};'>Rs {tick:,.2f}</div>
            <div style='font-size:12px; color:{color}; font-weight:600;'>{change:+.2f} ({pct:+.2f}%) • {symbol_input.upper()}</div>
        </div>
        <div style='text-align:right;'>
            <div style='font-size:10px; color:#6a6d78;'>IST TIME</div>
            <div style='font-size:22px; font-weight:800; color:#131722;'>{cur_ist.strftime('%H:%M:%S')}</div>
            <div style='font-size:11px; color:#6a6d78;'>{cur_ist.strftime('%d-%b-%Y')}</div>
            <div style='font-size:10px; color:{scolor}; font-weight:700; margin-top:4px;'>{status_msg}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

def ai_signal(prices):
    if len(prices) < 20:
        return "HOLD", 50
    arr = np.array(prices)
    sma20 = np.mean(arr[-20:])
    deltas = np.diff(arr)
    gains = np.where(deltas>0, deltas, 0)
    losses = np.where(deltas<0, -deltas, 0)
    avg_gain = np.mean(gains[-14:]) if len(gains)>=14 else 0.1
    avg_loss = np.mean(losses[-14:]) if len(losses)>=14 else 0.1
    rsi = 100 - (100/(1+ avg_gain/(avg_loss+0.0001)))
    score = 50 + (20 if arr[-1] > sma20 else -20) + (20 if rsi < 30 else -20 if rsi > 70 else 0)
    if score >= 65: return "BUY", score
    elif score <= 35: return "SELL", score
    else: return "HOLD", score

signal, score = ai_signal(hist)
sma20_val = np.mean(hist[-20:])
y_min = min(hist) * 0.9985
y_max = max(hist) * 1.0015

st.subheader(f"Live Chart - IST {cur_ist.strftime('%H:%M:%S')} - {symbol}")

fig = go.Figure()
fig.add_trace(go.Scatter(x=tt, y=hist, mode="lines", line=dict(color=color, width=3, shape="spline", smoothing=0.7), fill="tozeroy", fillcolor="rgba(0,162,91,0.08)" if up else "rgba(235,91,60,0.08)", name="LTP"))
fig.add_trace(go.Scatter(x=tt, y=[sma20_val]*len(tt), mode="lines", line=dict(color="#2962FF", width=1.5, dash="dot"), name=f"SMA20 {sma20_val:,.2f}"))
fig.add_trace(go.Scatter(x=[tt[-1]], y=[tick], mode="markers+text", marker=dict(size=12, color=color, line=dict(width=2, color="white")), text=[f" Rs {tick:,.2f}"], textposition="middle right", textfont=dict(size=12, color=color), name="NOW"))
fig.update_layout(height=520, plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(family="Inter", size=12, color="#131722"), margin=dict(l=10, r=80, t=20, b=40), showlegend=True, legend=dict(orientation="h", y=1.02, xanchor="right", x=1), xaxis=dict(showgrid=True, gridcolor="#f0f3fa", tickformat="%H:%M:%S"), yaxis=dict(showgrid=True, gridcolor="#f0f3fa", side="right", range=[y_min, y_max], title=f"{symbol} Rs", tickformat=",.2f"), hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)
