import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="TAPINU - Real TradingView", layout="wide")

st.markdown("### 📈 TAPINU - Real TradingView Chart - Original")

# Ticker Selector
col1, col2 = st.columns(2)
with col1:
    ticker_map = {
        "S&P BSE SENSEX": "BSE:SENSEX",
        "NIFTY 50": "NSE:NIFTY",
        "RELIANCE": "NSE:RELIANCE",
        "TATA MOTORS": "NSE:TATAMOTORS",
        "TCS": "NSE:TCS",
        "INFY": "NSE:INFY"
    }
    sel_name = st.selectbox("Stock Select Pannunga Sir", list(ticker_map.keys()), index=0)
with col2:
    st.write(f"Selected: {sel_name}")

symbol = ticker_map[sel_name]

# REAL TRADINGVIEW WIDGET - 100% Original - No Nonsense
tradingview_code = f"""
<div class="tradingview-widget-container" style="height:700px;width:100%">
  <div id="tradingview_chart" style="height:700px;width:100%"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget(
  {{
    "autosize": true,
    "symbol": "{symbol}",
    "interval": "D",
    "timezone": "Asia/Kolkata",
    "theme": "light",
    "style": "1",
    "locale": "en",
    "enable_publishing": false,
    "allow_symbol_change": true,
    "calendar": false,
    "studies": [
      "Volume@tv-basicstudies"
    ],
    "support_host": "https://www.tradingview.com"
  }}
  );
  </script>
</div>
"""

components.html(tradingview_code, height=700)

st.markdown("---")
st.success(f"**{sel_name} - Real TradingView Chart Sir! - Ithu Original TradingView Sir - Nonsense Illa Sir!**")

# Info like screenshot
st.markdown(f"""
<div style='background:white; padding:10px; border:1px solid #e0e3eb; border-radius:8px;'>
    <span style='background:#2962ff; color:white; padding:3px 10px; border-radius:15px; font-weight:bold; font-size:12px;'>BSE</span>
    <span style='font-weight:700; font-size:16px; margin-left:8px;'>S&P BSE Sensex Index - D - Real TradingView</span>
    <br><br>
    <b>Features:</b><br>
    ✅ Original TradingView Candle - No Nonsense Sir<br>
    ✅ Tools Left Side - Trendline, Fib, Text ellam irukkum Sir<br>
    ✅ BUY/SELL, Volume, Indicator ellam irukkum Sir<br>
    ✅ Mouse vechu candle theliva paarkalam Sir - Jul 28, 2026 open: 76831.75 maathiri<br>
    ✅ Top la 74459.53 +308.49 (+0.42%) maathiri live varum Sir
</div>
""", unsafe_allow_html=True)

st.info("💎 Tip: Ithu Real TradingView Sir - Unga Screenshot la irukura gray white box ellam poidum Sir - Full Original TradingView Sir! Zoom, Pan, Tools ellam work aagum Sir!")

st.caption("Real TradingView Widget - 100% Original - No Plotly Nonsense - TradingView Exact")
