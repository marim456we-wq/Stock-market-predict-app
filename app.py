import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="TAPINU - Groww Style", layout="wide")

try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1500, key="groww")
except:
    pass

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* {font-family: 'Inter', sans-serif;}
.groww-header {background:white; padding:14px 0; border-bottom:1px solid #e9ecef; position:sticky; top:0; z-index:10;}
.groww-card {background:white; border:1px solid #e9ecef; border-radius:12px; padding:16px; margin-bottom:12px;}
.groww-stock-row {display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid #f5f5f5;}
.groww-search {background:#f5f7f9; border-radius:12px; padding:12px 16px; border:none; width:100%; font-size:14px;}
.groww-green {color:#00a25b;}
.groww-red {color:#eb5b3c;}
.groww-btn-buy {background:#00a25b; color:white; border:none; border-radius:8px; padding:10px 24px; font-weight:600; width:100%;}
.groww-btn-sell {background:white; color:#eb5b3c; border:1px solid #eb5b3c; border-radius:8px; padding:10px 24px; font-weight:600; width:100%;}
.groww-chip {background:#f5f7f9; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:500; display:inline-block; margin:4px;}
.stButton>button {border-radius:8px; font-weight:600;}
</style>
""", unsafe_allow_html=True)

# INIT
if "cash" not in st.session_state:
    st.session_state["cash"] = 100000.0
    st.session_state["holdings"] = {}
    st.session_state["price"] = {}
    st.session_state["watch"] = ["TCS.NS","RELIANCE.NS","INFY.NS","TRENT.NS","ZOMATO.NS"]

if "selected_stock" not in st.session_state:
    st.session_state["selected_stock"] = "TCS.NS"

# PRICE TICK
def get_tick(sym):
    if sym not in st.session_state["price"]:
        try:
            import yfinance as yf
            d = yf.Ticker(sym).history(period="1d", interval="1m")
            base = float(d["Close"].iloc[-1]) if len(d)>0 else np.random.randint(500,3000)
        except:
            base = np.random.randint(500,3000)
        st.session_state["price"][sym] = base
    last = st.session_state["price"][sym]
    new = last + np.random.randn()*last*0.0006
    st.session_state["price"][sym] = max(new, last*0.996)
    return st.session_state["price"][sym]

for s in st.session_state["watch"]:
    get_tick(s)

selected = st.session_state["selected_stock"]
current_price = st.session_state["price"][selected]

# GROWW HEADER
st.markdown(f"""
<div class='groww-header'>
    <div style='display:flex; justify-content:space-between; align-items:center; padding:0 4px;'>
        <div style='display:flex; align-items:center; gap:12px;'>
            <div style='background:#00a25b; color:white; width:36px; height:36px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:18px;'>T</div>
            <div><div style='font-weight:700; font-size:16px;'>TAPINU</div><div style='font-size:11px; color:#6e6e6e;'>Groww Style • Demo</div></div>
        </div>
        <div style='text-align:right;'>
            <div style='font-size:11px; color:#6e6e6e;'>Total Balance</div>
            <div style='font-weight:700; font-size:14px;'>₹{st.session_state["cash"] + sum([st.session_state["price"].get(k,0)*v["qty"] for k,v in st.session_state["holdings"].items()]):,.0f}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# SEARCH
search = st.text_input("", placeholder="🔍 Search Stocks, Mutual Funds - Ex: TCS, RELIANCE, ZOMATO", label_visibility="collapsed")
if search:
    st.session_state["selected_stock"] = search.strip().upper()
    if ".NS" not in st.session_state["selected_stock"]:
        st.session_state["selected_stock"] += ".NS"
    selected = st.session_state["selected_stock"]
    current_price = get_tick(selected)

# GROWW TABS - Bottom Nav Style
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Explore", "📊 Stocks", "💼 Portfolio", "⭐ Watchlist"])

with tab1:
    st.markdown("#### 👋 Good Morning, Trader")
    st.markdown(f"<div class='groww-card'><div style='font-size:12px; color:#6e6e6e;'>MARKET TODAY • {datetime.now().strftime('%d %b %H:%M')}</div><div style='display:flex; gap:16px; margin-top:10px;'><div><div style='font-size:12px; color:#6e6e6e;'>NIFTY 50</div><div style='font-weight:700;'>23,252.60</div><div class='groww-green' style='font-size:12px;'>▲ 0.87%</div></div><div><div style='font-size:12px; color:#6e6e6e;'>SENSEX</div><div style='font-weight:700;'>74,659</div><div class='groww-green' style='font-size:12px;'>▲ 0.52%</div></div><div><div style='font-size:12px; color:#6e6e6e;'>Your P&L</div><div style='font-weight:700;' class='groww-green'>+₹{sum([(st.session_state['price'].get(k,0)-v['avg'])*v['qty'] for k,v in st.session_state['holdings'].items()]):,.0f}</div><div style='font-size:12px;'>Today</div></div></div></div>", unsafe_allow_html=True)
    
    st.markdown("#### 🔥 Popular Stocks - Groww Style")
    cols = st.columns(2)
    for i, sym in enumerate(["TCS.NS","RELIANCE.NS","INFY.NS","TRENT.NS","ZOMATO.NS","LAURUSLABS.NS"]):
        price = get_tick(sym)
        change = np.random.randn()*1.5
        col = cols[i%2]
        with col:
            if st.button(f"{sym.replace('.NS','')} \n₹{price:.0f}  {'▲' if change>0 else '▼'} {abs(change):.2f}%", key=f"pop_{sym}", use_container_width=True):
                st.session_state["selected_stock"] = sym
                st.rerun()

    st.markdown("#### 💰 Mutual Funds - Top Picks")
    st.markdown("""
    <div class='groww-card'><div style='display:flex; justify-content:space-between;'><div><div style='font-weight:600; font-size:13px;'>Nippon Small Cap</div><div style='font-size:11px; color:#6e6e6e;'>5Y • 28.5%</div></div><div style='color:#00a25b; font-weight:700;'>+28.5%</div></div></div>
    <div class='groww-card'><div style='display:flex; justify-content:space-between;'><div><div style='font-weight:600; font-size:13px;'>Quant Small Cap</div><div style='font-size:11px; color:#6e6e6e;'>5Y • 32.1%</div></div><div style='color:#00a25b; font-weight:700;'>+32.1%</div></div></div>
    """, unsafe_allow_html=True)

with tab2:
    # Groww Stock Detail Page
    st.markdown(f"""
    <div class='groww-card'>
        <div style='display:flex; justify-content:space-between; align-items:start;'>
            <div>
                <div style='background:#f5f7f9; width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:16px;'>{selected[:2]}</div>
                <div style='font-weight:700; font-size:18px; margin-top:8px;'>{selected.replace('.NS','')}</div>
                <div style='font-size:12px; color:#6e6e6e;'>NSE • {selected}</div>
            </div>
            <div style='text-align:right;'>
                <div style='font-weight:700; font-size:22px;'>₹{current_price:,.2f}</div>
                <div class='{"groww-green" if np.random.randn()>-0.2 else "groww-red"}' style='font-size:13px; font-weight:600;'>▲ ₹{(current_price*0.008):.2f} (0.82%) • 1D</div>
                <div style='font-size:11px; color:#6e6e6e; margin-top:4px;'>{datetime.now().strftime('%H:%M:%S')} • LIVE • Tick</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Groww Chart
    hist = st.session_state["price"].get(selected, current_price)
    prices = [hist + np.random.randn()*hist*0.005 for _ in range(60)]
    prices[-1] = current_price
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=prices, mode="lines", line=dict(color="#00a25b", width=2.5, shape="spline"), fill="tozeroy", fillcolor="rgba(0,162,91,0.1)"))
    fig.update_layout(height=220, plot_bgcolor="white", paper_bgcolor="white", margin=dict(l=0,r=0,t=0,b=0), showlegend=False, xaxis=dict(visible=False), yaxis=dict(visible=False))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Groww Info Chips
    st.markdown("""
    <div style='margin:10px 0;'>
        <span class='groww-chip'>📊 Day Low ₹2,480</span><span class='groww-chip'>📈 Day High ₹2,560</span><span class='groww-chip'>52W Low ₹2,100</span><span class='groww-chip'>52W High ₹3,100</span>
        <span class='groww-chip'>PE 28.5</span><span class='groww-chip'>Market Cap ₹12L Cr</span>
    </div>
    """, unsafe_allow_html=True)

    # Groww BUY SELL Buttons - Bottom Fixed Style
    st.markdown("#### Trade")
    qty = st.number_input("Quantity", min_value=1, value=1, step=1)
    st.markdown(f"**Order Value: ₹{qty*current_price:,.2f}**")
    st.caption("Brokerage: ₹20 or 0.05% • Groww Style Charges")
    
    b1,b2 = st.columns(2)
    with b1:
        if st.button("BUY", use_container_width=True, type="primary"):
            cost = qty*current_price
            if st.session_state["cash"] >= cost:
                st.session_state["cash"] -= cost
                if selected in st.session_state["holdings"]:
                    old = st.session_state["holdings"][selected]
                    new_qty = old["qty"]+qty
                    new_avg = (old["qty"]*old["avg"] + qty*current_price)/new_qty
                    st.session_state["holdings"][selected] = {"qty":new_qty, "avg":new_avg}
                else:
                    st.session_state["holdings"][selected] = {"qty":qty, "avg":current_price}
                st.success(f"✅ BUY Order Placed - {qty} {selected} @ ₹{current_price:.2f} - Groww Style!")
                st.balloons()
                st.rerun()
            else:
                st.error("Insufficient Balance Sir!")
    with b2:
        if st.button("SELL", use_container_width=True):
            if selected in st.session_state["holdings"] and st.session_state["holdings"][selected]["qty"] >= qty:
                st.session_state["cash"] += qty*current_price
                st.session_state["holdings"][selected]["qty"] -= qty
                if st.session_state["holdings"][selected]["qty"]==0:
                    del st.session_state["holdings"][selected]
                st.success(f"✅ SELL Order Placed - {qty} {selected} @ ₹{current_price:.2f}")
                st.rerun()
            else:
                st.error("No Holdings Sir!")

with tab3:
    st.markdown("#### 💼 Your Portfolio - Groww Style")
    total_val = st.session_state["cash"] + sum([st.session_state["price"].get(k,0)*v["qty"] for k,v in st.session_state["holdings"].items()])
    pnl = total_val - 100000
    st.markdown(f"""
    <div class='groww-card' style='background:linear-gradient(135deg,#00a25b 0%, #00c853 100%); color:white; border:none;'>
        <div style='font-size:12px; opacity:0.9;'>Total Portfolio • Groww</div>
        <div style='font-size:28px; font-weight:700; margin-top:4px;'>₹{total_val:,.0f}</div>
        <div style='font-size:13px; background:rgba(255,255,255,0.2); display:inline-block; padding:4px 10px; border-radius:20px; margin-top:6px;'>{"▲" if pnl>=0 else "▼"} ₹{pnl:+,.0f} ({pnl/100000*100:+.2f}%) • All Time</div>
    </div>
    """, unsafe_allow_html=True)
    
    c1,c2 = st.columns(2)
    c1.markdown(f"<div class='groww-card'><div style='font-size:11px; color:#6e6e6e;'>Cash Available</div><div style='font-weight:700;'>₹{st.session_state['cash']:,.0f}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='groww-card'><div style='font-size:11px; color:#6e6e6e;'>Invested</div><div style='font-weight:700;'>₹{sum([v['qty']*v['avg'] for v in st.session_state['holdings'].values()]):,.0f}</div></div>", unsafe_allow_html=True)

    if st.session_state["holdings"]:
        for sym, data in st.session_state["holdings"].items():
            cur = st.session_state["price"].get(sym, data["avg"])
            pl = (cur-data["avg"])*data["qty"]
            st.markdown(f"""
            <div class='groww-card'>
                <div style='display:flex; justify-content:space-between;'>
                    <div><div style='font-weight:600;'>{sym.replace('.NS','')}</div><div style='font-size:11px; color:#6e6e6e;'>{data["qty"]} Qty • Avg ₹{data["avg"]:.0f}</div></div>
                    <div style='text-align:right;'><div style='font-weight:700;'>₹{cur*data["qty"]:,.0f}</div><div style='font-size:12px;' class='{"groww-green" if pl>=0 else "groww-red"}'>{"▲" if pl>=0 else "▼"} ₹{pl:+.0f} ({pl/(data["avg"]*data["qty"])*100:+.2f}%)</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No Holdings Yet Sir - Go to Stocks Tab and BUY Sir - Groww Maathiri")

with tab4:
    st.markdown("#### ⭐ Watchlist")
    for sym in st.session_state["watch"]:
        price = st.session_state["price"].get(sym, 0)
        change = np.random.randn()*2
        st.markdown(f"""
        <div class='groww-card' style='padding:12px 16px;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div><div style='font-weight:600; font-size:14px;'>{sym.replace('.NS','')}</div><div style='font-size:11px; color:#6e6e6e;'>{sym}</div></div>
                <div style='text-align:right;'><div style='font-weight:700; font-size:14px;'>₹{price:.0f}</div><div style='font-size:12px;' class='{"groww-green" if change>0 else "groww-red"}'>{"▲" if change>0 else "▼"} {abs(change):.2f}%</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Trade {sym.replace('.NS','')}", key=f"watch_{sym}"):
            st.session_state["selected_stock"] = sym
            st.rerun()

st.caption("TAPINU - Groww Clone • Green #00a25b • White Cards • Rounded 12px • Inter Font • Second Second Tick • Demo Trading • Built for Chennai")
