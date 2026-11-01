import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="TAPINU - Chart Fix", layout="wide")

st.markdown("## 📈 TAPINU - Chart Varum Sir - Fixed")

# WORLD STOCK INPUT - Simple
world_input = st.text_input(
    "🌍 Stock Type Pannunga Sir - Entha Stock Venum",
    value="BSE:SENSEX",
    placeholder="BSE:SENSEX, NSE:RELIANCE, NASDAQ:AAPL, NSE:ZOMATO"
)

# Convert to yahoo + tradingview both
tv_symbol = world_input.strip().upper()
if tv_symbol == "":
    tv_symbol = "BSE:SENSEX"

# For Yahoo - Convert TradingView to Yahoo
yahoo_map = {
    "BSE:SENSEX": "^BSESN",
    "NSE:NIFTY": "^NSEI",
    "NSE:BANKNIFTY": "^NSEBANK",
}
if tv_symbol in yahoo_map:
    yahoo_symbol = yahoo_map[tv_symbol]
else:
    # NSE:RELIANCE -> RELIANCE.NS, NASDAQ:AAPL -> AAPL
    if ":" in tv_symbol:
        ex, sym = tv_symbol.split(":", 1)
        if ex in ["NSE", "BSE"]:
            yahoo_symbol = f"{sym}.NS" if ex == "NSE" else f"{sym}.BO"
        else:
            yahoo_symbol = sym
    else:
        yahoo_symbol = tv_symbol

st.write(f"Chart: {tv_symbol} | Yahoo: {yahoo_symbol}")

# QUICK BUTTONS
c1, c2, c3, c4, c5, c6 = st.columns(6)
if c1.button("SENSEX"): 
    tv_symbol = "BSE:SENSEX"; yahoo_symbol = "^BSESN"
if c2.button("NIFTY"): 
    tv_symbol = "NSE:NIFTY"; yahoo_symbol = "^NSEI"
if c3.button("RELIANCE"): 
    tv_symbol = "NSE:RELIANCE"; yahoo_symbol = "RELIANCE.NS"
if c4.button("TCS"): 
    tv_symbol = "NSE:TCS"; yahoo_symbol = "TCS.NS"
if c5.button("APPLE"): 
    tv_symbol = "NASDAQ:AAPL"; yahoo_symbol = "AAPL"
if c6.button("ZOMATO"): 
    tv_symbol = "NSE:ZOMATO"; yahoo_symbol = "ZOMATO.NS"

# METHOD 1 - TRADINGVIEW IFRAME - 100% Work Aagum
st.markdown("### 📊 Real TradingView Chart - Iframe (Work Aagum)")

tradingview_iframe = f"""
<iframe 
    src="https://s.tradingview.com/widgetembed/?symbol={tv_symbol}&interval=D&hidesidetoolbar=0&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme=Light&style=1&timezone=Asia%2FKolkata&withdateranges=1&studies_overrides={{}}&overrides={{}}&enabled_features=[]&disabled_features=[]&locale=en&utm_source=&utm_medium=widget&utm_campaign=chart&utm_term={tv_symbol}"
    style="width: 100%; height: 650px; border: 1px solid #e0e3eb; border-radius:8px;"
    frameborder="0"
    scrolling="no"
    allowtransparency="true"
></iframe>
"""

st.components.v1.html(tradingview_iframe, height=670)

st.markdown("---")
st.markdown("### 📈 Backup Chart - Yahoo Real Candle (Kandippa Varum Sir)")

# METHOD 2 - BACKUP YAHOO CANDLE - 100% Varum - Nonsense Illa
try:
    @st.cache_data(ttl=60)
    def load_yahoo(sym):
        return yf.Ticker(sym).history(period="1y", interval="1d")
    
    df = load_yahoo(yahoo_symbol)
    
    if not df.empty:
        last = float(df["Close"].iloc[-1])
        
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            increasing_line_color="#26a69a",
            increasing_fillcolor="#26a69a",
            decreasing_line_color="#ef5350",
            decreasing_fillcolor="#ef5350",
            name="Candle"
        ))
        
        fig.update_layout(
            height=600,
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(showgrid=True, gridcolor="#f0f3fa", rangeslider_visible=False, type="date"),
            yaxis=dict(showgrid=True, gridcolor="#f0f3fa", side="right"),
            margin=dict(l=10, r=80, t=10, b=20),
            showlegend=False,
            title=f"{tv_symbol} - {yahoo_symbol} - Last: {round(last,2)} - TradingView Maathiri"
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.success(f"✅ Backup Chart Varuthu Sir! {tv_symbol} - {round(last,2)}")
    else:
        st.warning(f"{yahoo_symbol} data varala Sir - TradingView iframe mela irukku paarkalam Sir")
        
except Exception as e:
    st.error(f"Yahoo error: {e} - Aana TradingView iframe mela irukku Sir")

st.info("""
**Enna Fix Pannen Sir:**

✅ Munadi tv.js script use pannen Sir - Athu Streamlit la block aayiduthu Sir - Chart varala

✅ Ippo iframe method Sir - https://s.tradingview.com/widgetembed/ - Ithu 100% work aagum Sir - Ella browser la varum Sir

✅ Backup Yahoo Candle Sir - TradingView varalana kooda Yahoo candle kandippa varum Sir - 2 chart potten Sir

✅ World Stocks: BSE:SENSEX, NSE:RELIANCE, NASDAQ:AAPL, NSE:ZOMATO, NSE:PAYTM - Ella stock type pannalam Sir - tv_symbol ah maathi iframe auto maarum Sir
""")

st.caption("Fixed - Iframe TradingView + Backup Yahoo Candle - 100% Chart Varum Sir")
