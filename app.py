import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="TAPINU TRADER", layout="wide")

try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1000, key="trader_tick")
except:
    pass

st.markdown("""
<style>
.pro-card {background:white; border:1px solid #e0e3eb; border-radius:12px; padding:14px; margin-bottom:10px;}
.buy-btn {background:#00c853; color:white;}
.sell-btn {background:#ff1744; color:white;}
</style>
""", unsafe_allow_html=True)

# INIT PORTFOLIO - Session
if "cash" not in st.session_state:
    st.session_state["cash"] = 100000.0  # 1 Lakh Demo Money Sir
    st.session_state["holdings"] = {}  # symbol -> qty, avg
    st.session_state["trades"] = []  # history
    st.session_state["price_store"] = {}
    st.session_state["history_store"] = {}

st.markdown("## 💰 TAPINU TRADER - BUY/SELL + LIVE TICK")

# Symbol
symbol = st.text_input("Symbol", value="TCS.NS").strip().upper() or "TCS.NS"

# LIVE PRICE TICK - SECOND SECOND
if symbol not in st.session_state["price_store"]:
    try:
        import yfinance as yf
        d = yf.Ticker(symbol).history(period="1d", interval="1m")
        base = float(d["Close"].iloc[-1]) if len(d)>0 else 2500.0
    except:
        base = 2500.0
    st.session_state["price_store"][symbol] = base
    st.session_state["history_store"][symbol] = [base + np.random.randn()*base*0.0002 for _ in range(60)]
    st.session_state["history_store"][symbol+"_time"] = [datetime.now()]*60

# Tick update
last_p = st.session_state["price_store"][symbol]
new_p = last_p + np.random.randn()*last_p*0.0008
new_p = max(new_p, last_p*0.995)
st.session_state["price_store"][symbol] = new_p
st.session_state["history_store"][symbol].append(new_p)
st.session_state["history_store"][symbol] = st.session_state["history_store"][symbol][-120:]
st.session_state["history_store"][symbol+"_time"].append(datetime.now())
st.session_state["history_store"][symbol+"_time"] = st.session_state["history_store"][symbol+"_time"][-120:]

prices = st.session_state["history_store"][symbol]
times = st.session_state["history_store"][symbol+"_time"]

color = "#00c853" if new_p>=prices[0] else "#ff1744"

# TOP BAR - CASH + P&L
hold_qty = st.session_state["holdings"].get(symbol, {}).get("qty",0)
hold_avg = st.session_state["holdings"].get(symbol, {}).get("avg",0)
hold_pl = (new_p - hold_avg)*hold_qty if hold_qty>0 else 0
total_hold_value = sum([st.session_state["price_store"].get(s,0)*d["qty"] for s,d in st.session_state["holdings"].items()])
total_pl = total_hold_value - sum([d["avg"]*d["qty"] for d in st.session_state["holdings"].values()]) if st.session_state["holdings"] else 0
total_value = st.session_state["cash"] + total_hold_value

c1,c2,c3,c4 = st.columns(4)
c1.metric("💵 Cash", f"₹{st.session_state['cash']:,.2f}")
c2.metric("📦 Holdings Value", f"₹{total_hold_value:,.2f}", f"₹{total_pl:+.2f}")
c3.metric("💎 Total Portfolio", f"₹{total_value:,.2f}", f"₹{total_value-100000:+.2f}")
c4.metric(f"{symbol} P&L", f"₹{hold_pl:+.2f}", f"{hold_qty} Qty")

# CHART + BUY/SELL PANEL
col_chart, col_trade = st.columns([2.2,1])

with col_chart:
    st.markdown(f"<div class='pro-card'><b>{symbol} LIVE TICK</b> {new_p:.2f} <span style='color:{color};'>Second Second</span> • {datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=prices, mode="lines", line=dict(color=color, width=2.5, shape="spline"), fill="tozeroy", fillcolor=f"rgba(0,200,83,0.15)" if color=="#00c853" else "rgba(255,23,68,0.15)"))
    fig.add_trace(go.Scatter(x=[times[-1]], y=[new_p], mode="markers", marker=dict(size=12, color=color, line=dict(width=2, color="white"))))
    # Avg line if holding
    if hold_qty>0:
        fig.add_hline(y=hold_avg, line_dash="dash", line_color="blue", annotation_text=f"Your AVG {hold_avg:.2f}")
    fig.update_layout(height=420, plot_bgcolor="white", paper_bgcolor="white", margin=dict(l=5,r=50,t=10,b=20), showlegend=False, xaxis=dict(tickformat="%H:%M:%S"), yaxis=dict(side="right"), uirevision="trade")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with col_trade:
    st.markdown("<div class='pro-card'>", unsafe_allow_html=True)
    st.markdown(f"#### Trade {symbol}")
    st.markdown(f"**LTP: ₹{new_p:,.2f}**")
    qty = st.number_input("Quantity", min_value=1, value=1, step=1)
    cost = qty*new_p
    st.markdown(f"**Cost: ₹{cost:,.2f}**")
    
    b1,b2 = st.columns(2)
    with b1:
        if st.button("🟢 BUY", use_container_width=True, type="primary"):
            if st.session_state["cash"] >= cost:
                st.session_state["cash"] -= cost
                if symbol in st.session_state["holdings"]:
                    old_qty = st.session_state["holdings"][symbol]["qty"]
                    old_avg = st.session_state["holdings"][symbol]["avg"]
                    new_qty = old_qty + qty
                    new_avg = (old_qty*old_avg + qty*new_p)/new_qty
                    st.session_state["holdings"][symbol] = {"qty": new_qty, "avg": new_avg}
                else:
                    st.session_state["holdings"][symbol] = {"qty": qty, "avg": new_p}
                st.session_state["trades"].append({"time":datetime.now().strftime("%H:%M:%S"), "symbol":symbol, "type":"BUY", "qty":qty, "price":new_p, "total":cost})
                st.success(f"BUY {qty} {symbol} @ {new_p:.2f}")
                st.rerun()
            else:
                st.error("Cash Illa Sir!")
    
    with b2:
        if st.button("🔴 SELL", use_container_width=True):
            if symbol in st.session_state["holdings"] and st.session_state["holdings"][symbol]["qty"] >= qty:
                st.session_state["cash"] += cost
                st.session_state["holdings"][symbol]["qty"] -= qty
                if st.session_state["holdings"][symbol]["qty"]==0:
                    del st.session_state["holdings"][symbol]
                st.session_state["trades"].append({"time":datetime.now().strftime("%H:%M:%S"), "symbol":symbol, "type":"SELL", "qty":qty, "price":new_p, "total":cost})
                st.success(f"SELL {qty} {symbol} @ {new_p:.2f}")
                st.rerun()
            else:
                st.error(f"Holdings Illa Sir! You have {hold_qty}")

    st.markdown("---")
    st.markdown("**AI Signal**")
    rsi_proxy = 50 + (new_p-prices[0])/prices[0]*1000
    signal = "🟢 STRONG BUY" if rsi_proxy<45 else "🔴 STRONG SELL" if rsi_proxy>55 else "🟡 HOLD"
    st.markdown(f"<div style='background:#f3e5f5; color:#7c4dff; padding:8px; border-radius:8px; text-align:center; font-weight:700;'>{signal}<br><small>RSI {rsi_proxy:.0f}</small></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# PORTFOLIO + HISTORY
t1,t2 = st.tabs(["📦 My Holdings - P&L", "📜 Trade History"])

with t1:
    if st.session_state["holdings"]:
        rows = []
        for sym,data in st.session_state["holdings"].items():
            cur = st.session_state["price_store"].get(sym, data["avg"])
            pl = (cur-data["avg"])*data["qty"]
            pl_pct = (cur-data["avg"])/data["avg"]*100
            rows.append({"Symbol":sym, "Qty":data["qty"], "Avg Price":f"{data['avg']:.2f}", "LTP":f"{cur:.2f}", "P&L ₹":f"{pl:+.2f}", "P&L %":f"{pl_pct:+.2f}%", "Value":f"{cur*data['qty']:.2f}"})
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.info("Holdings Illa Sir - BUY Pannunga Sir")

with t2:
    if st.session_state["trades"]:
        st.dataframe(pd.DataFrame(st.session_state["trades"][::-1]), use_container_width=True)
        if st.button("Clear History"):
            st.session_state["trades"] = []
            st.rerun()
    else:
        st.info("Trade History Illa Sir")

st.caption(f"Demo Trading • Starting Cash 1 Lakh • Second Second Price • {datetime.now().strftime('%H:%M:%S')} • BUY/SELL Real Maathiri Sir")
