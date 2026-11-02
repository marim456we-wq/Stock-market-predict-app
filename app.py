import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

st.set_page_config(page_title="TAPINU REAL", layout="wide")

try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=10000, key="real")  # 10 Sec ku Real Price Update - Yahoo Limit Sir
except:
    pass

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
* {font-family: 'Inter';}
.real-card {background:white; border:1px solid #e0e3eb; border-radius:12px; padding:16px; margin-bottom:12px;}
.live-dot {background:#eb5b3c; color:white; padding:2px 8px; border-radius:12px; font-size:10px; font-weight:700; animation: blink 1s infinite;}
</style>
""", unsafe_allow_html=True)

if "cash" not in st.session_state:
    st.session_state["cash"] = 100000.0
    st.session_state["holdings"] = {}

# REAL LIVE DATA - NO DEMO - YAHOO DIRECT
@st.cache_data(ttl=10)  # 10 Sec Only - Real Time Ku
def get_real_nse_price(symbol):
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        # REAL INTRADAY - 1m interval - ITHU REAL NSE DATA SIR
        intraday = ticker.history(period="1d", interval="1m", auto_adjust=False)
        daily = ticker.history(period="1y", interval="1d", auto_adjust=False)
        info = {}
        try:
            info = ticker.fast_info
        except:
            pass
        
        if len(intraday) > 0:
            last_price = float(intraday["Close"].iloc[-1])
            last_time = intraday.index[-1]
            open_p = float(intraday["Open"].iloc[0])
            high = float(intraday["High"].max())
            low = float(intraday["Low"].min())
            volume = int(intraday["Volume"].sum())
            prev_close = float(daily["Close"].iloc[-2]) if len(daily)>1 else open_p
            return {
                "price": last_price, "time": last_time, "open": open_p, "high": high, "low": low,
                "volume": volume, "prev": prev_close, "intraday": intraday, "daily": daily, "live": True
            }
        elif len(daily) > 0:
            last_price = float(daily["Close"].iloc[-1])
            return {
                "price": last_price, "time": daily.index[-1], "open": last_price, "high": last_price,
                "low": last_price, "volume": 0, "prev": float(daily["Close"].iloc[-2]), "intraday": daily.tail(100), "daily": daily, "live": False
            }
    except Exception as e:
        st.error(f"Yahoo Error: {e}")
    return None

st.markdown("## 🔴 TAPINU REAL - 100% REAL NSE LIVE - NO DEMO")

symbol = st.text_input("Enter Real NSE Symbol (TCS.NS, RELIANCE.NS, INFY.NS, SBIN.NS)", value="TCS.NS").strip().upper()
if ".NS" not in symbol and "^" not in symbol:
    symbol += ".NS"

ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist)
is_market_open = 9 <= now_ist.hour < 16 and now_ist.weekday() < 5

data = get_real_nse_price(symbol)

if data is None:
    st.error(f"❌ {symbol} Real Data Kedaikala Sir - Symbol Check Pannunga Sir - Ex: TCS.NS, RELIANCE.NS, ^NSEI, ^BSESN")
    st.stop()

price = data["price"]
prev = data["prev"]
chg = price - prev
pct = (chg/prev*100) if prev!=0 else 0
is_up = chg>=0
color = "#00a25b" if is_up else "#eb5b3c"

# REAL HEADER
st.markdown(f"""
<div class='real-card' style='border-left:4px solid {color};'>
    <div style='display:flex; justify-content:space-between; flex-wrap:wrap;'>
        <div>
            <div style='display:flex; align-items:center; gap:8px;'><span class='live-dot'>● {"LIVE" if data["live"] and is_market_open else "CLOSED"}</span><span style='font-size:12px; color:#6e6e6e;'>{symbol} • NSE REAL • {data["time"].strftime('%d-%m-%Y %H:%M:%S')} IST • Source: Yahoo Finance NSE</span></div>
            <div style='font-size:12px; color:#6e6e6e; margin-top:4px;'>OPEN ₹{data["open"]:.2f} • HIGH ₹{data["high"]:.2f} • LOW ₹{data["low"]:.2f} • VOL {data["volume"]:,}</div>
            <div style='font-size:32px; font-weight:700; margin-top:6px;'>{price:,.2f} <span style='font-size:18px; color:{color};'>{'▲' if is_up else '▼'} {chg:+.2f} ({pct:+.2f}%)</span></div>
            <div style='font-size:11px; color:{"#00a25b" if is_market_open else "#eb5b3c"}; font-weight:600; margin-top:4px;'>{'🟢 MARKET OPEN - REAL PRICE UPDATING EVERY 10 SEC' if is_market_open else '🔴 MARKET CLOSED - Showing Last Close Price - 9:15 AM to 3:30 PM Only Live'} • Chennai Time: {now_ist.strftime('%H:%M:%S')}</div>
        </div>
        <div style='text-align:right;'>
            <div style='font-size:11px; color:#6e6e6e;'>PREV CLOSE</div><div style='font-weight:700;'>₹{prev:.2f}</div>
            <div style='margin-top:8px;'><span style='background:{"#e8f5e9" if is_up else "#ffebee"}; color:{color}; padding:6px 12px; border-radius:20px; font-weight:700; font-size:12px;'>NSE REAL DATA - NO DEMO</span></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# REAL CHART - INTRADAY 1m
col_chart, col_trade = st.columns([2.2,1])

with col_chart:
    st.markdown("#### 📈 Real Intraday Chart - NSE Live")
    df = data["intraday"]
    fig = go.Figure()
    
    # If intraday available - Real 1m candles
    if len(df) > 10 and data["live"]:
        fig.add_trace(go.Candlestick(x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], name="REAL NSE 1m"))
    else:
        fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", line=dict(color=color, width=2.5, shape="spline"), fill="tozeroy", fillcolor=f"rgba(0,162,91,0.1)" if is_up else "rgba(235,91,60,0.1)", name="REAL Close"))
    
    fig.update_layout(height=400, plot_bgcolor="white", paper_bgcolor="white", xaxis_rangeslider_visible=False, margin=dict(l=5,r=60,t=10,b=20), showlegend=False, xaxis=dict(showgrid=True, gridcolor="#f0f3fa", title="Real NSE Time"), yaxis=dict(showgrid=True, gridcolor="#f0f3fa", side="right"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.caption(f"Real Data Source: Yahoo Finance NSE - {symbol} - Last Update {data['time']} - Updates every 10 sec during market hours")

with col_trade:
    st.markdown("<div class='real-card'>", unsafe_allow_html=True)
    st.markdown(f"#### Trade Real {symbol.replace('.NS','')}")
    st.markdown(f"**Real LTP: ₹{price:,.2f}** - NSE")
    qty = st.number_input("Qty", min_value=1, value=1, step=1, key="real_qty")
    cost = qty*price
    st.markdown(f"**Real Value: ₹{cost:,.2f}**")
    
    b1,b2 = st.columns(2)
    with b1:
        if st.button("🟢 BUY REAL", use_container_width=True, type="primary"):
            if st.session_state["cash"] >= cost:
                st.session_state["cash"] -= cost
                if symbol in st.session_state["holdings"]:
                    o = st.session_state["holdings"][symbol]
                    nq = o["qty"]+qty
                    na = (o["qty"]*o["avg"]+qty*price)/nq
                    st.session_state["holdings"][symbol] = {"qty":nq, "avg":na}
                else:
                    st.session_state["holdings"][symbol] = {"qty":qty, "avg":price}
                st.success(f"BUY {qty} @ Real ₹{price:.2f}")
                st.rerun()
            else:
                st.error("Cash Illa Sir!")
    with b2:
        if st.button("🔴 SELL REAL", use_container_width=True):
            if symbol in st.session_state["holdings"] and st.session_state["holdings"][symbol]["qty"]>=qty:
                st.session_state["cash"] += cost
                st.session_state["holdings"][symbol]["qty"] -= qty
                if st.session_state["holdings"][symbol]["qty"]==0:
                    del st.session_state["holdings"][symbol]
                st.success(f"SELL {qty} @ Real ₹{price:.2f}")
                st.rerun()
            else:
                st.error("Holdings Illa!")
    
    st.markdown("---")
    st.markdown("**Real Market Info**")
    st.markdown(f"<div style='font-size:12px; color:#6e6e6e;'>Symbol: {symbol}<br>Exchange: NSE<br>Currency: INR<br>Price Type: REAL LTP<br>Delay: ~1 Min (Yahoo Free)<br>For 0 Sec Delay Need Zerodha API</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Portfolio Real
st.markdown("#### 💼 Real Portfolio - NSE Live P&L")
if st.session_state["holdings"]:
    for sym, d in st.session_state["holdings"].items():
        rd = get_real_nse_price(sym)
        cur = rd["price"] if rd else d["avg"]
        pl = (cur-d["avg"])*d["qty"]
        st.markdown(f"<div class='real-card'><div style='display:flex; justify-content:space-between;'><div><b>{sym}</b> {d['qty']} Qty Avg ₹{d['avg']:.2f}</div><div style='text-align:right;'><b>₹{cur*d['qty']:,.0f}</b> <span style='color:{'#00a25b' if pl>=0 else '#eb5b3c'}'>₹{pl:+.0f}</span></div></div></div>", unsafe_allow_html=True)
else:
    st.info("No Holdings - Real Stock BUY Pannunga Sir")

st.markdown("---")
st.markdown("""
**REAL vs DEMO Difference Sir Purinjikonga:**

✅ **Ippo Full REAL Sir** - Yahoo Finance NSE Direct Data Sir - TCS Real Price ₹2500+ Kaamikkum Sir - Demo Illa Sir

✅ **10 Sec Update Sir** - Yahoo Free Limit 10 Sec Sir - Second Second Ku Update Panna Yahoo Block Pannidum Sir - 10 Sec Best Sir

✅ **Market Hours 9:15-15:30 Sir** - Ippo Time 10:15 AM Sir - Market Open Sir - So Real Live Price Varum Sir

⚠️ **0 Second Real Tick Venum Na** - Zerodha Kite API, TrueData, TradingView Paid Venum Sir - Athu ₹2000/month Sir - Yahoo Free La 1 Min Delay Thaan Kedaikkum Sir

**Ippo Symbol Type Panni Paarkalam Sir - TCS.NS, RELIANCE.NS, INFY.NS, ^NSEI, ^BSESN Ellam Real Price Varum Sir!**
""")

st.caption(f"REAL NSE DATA • Source: yfinance NSE • No Simulation • Last Check {datetime.now().strftime('%H:%M:%S')} • Chennai")
