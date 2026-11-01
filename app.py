import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="TAPINU - WORLD ALL STOCKS", layout="wide")

st.markdown("## 🌍 TAPINU - WORLD FULL STOCKS - Ella Stock Varum Sir!")

st.info("🌍 World la 50,000+ Stocks Sir - Entha Stock Venumna Type Pannunga Sir - Real TradingView la Varum Sir!")

# WORLD STOCK SEARCH - ANY STOCK
col1, col2, col3 = st.columns([2,1,1])

with col1:
    world_stock = st.text_input(
        "🌍 WORLD STOCK SEARCH - Entha Stock Venumna Type Pannunga Sir",
        value="BSE:SENSEX",
        placeholder="Ex: BSE:SENSEX, NSE:RELIANCE, NASDAQ:AAPL, NYSE:TSLA, BINANCE:BTCUSDT",
        help="World la entha stock venumna TradingView symbol type pannunga Sir"
    )

with col2:
    exchange = st.selectbox(
        "Exchange Quick Select",
        ["BSE: (India)", "NSE: (India)", "NASDAQ: (USA)", "NYSE: (USA)", "BINANCE: (Crypto)", "LSE: (London)", "TSE: (Tokyo)"]
    )
    
with col3:
    quick_symbol = st.text_input("Symbol Only (Ex: RELIANCE, AAPL, BTCUSDT)", placeholder="RELIANCE")

# Build final symbol
symbol = world_stock.strip().upper()

if quick_symbol.strip() != "" and world_stock.strip() == "BSE:SENSEX":
    # Auto build from exchange
    ex_code = exchange.split(":")[0]
    symbol = f"{ex_code}:{quick_symbol.strip().upper()}"
elif quick_symbol.strip() != "" and world_stock.strip() != "":
    # If both given, prefer world_stock
    pass

if not symbol:
    symbol = "BSE:SENSEX"

# QUICK BUTTONS - World Famous
st.markdown("**⚡ Quick World Famous Stocks - Click Pannunga Sir:**")
q1, q2, q3, q4, q5, q6, q7, q8 = st.columns(8)

if q1.button("SENSEX 🇮🇳"): symbol = "BSE:SENSEX"
if q2.button("NIFTY 🇮🇳"): symbol = "NSE:NIFTY"
if q3.button("RELIANCE 🇮🇳"): symbol = "NSE:RELIANCE"
if q4.button("TCS 🇮🇳"): symbol = "NSE:TCS"
if q5.button("APPLE 🇺🇸"): symbol = "NASDAQ:AAPL"
if q6.button("TESLA 🇺🇸"): symbol = "NASDAQ:TSLA"
if q7.button("BITCOIN ₿"): symbol = "BINANCE:BTCUSDT"
if q8.button("GOOGLE 🇺🇸"): symbol = "NASDAQ:GOOGL"

# More quick
q1, q2, q3, q4, q5, q6, q7, q8 = st.columns(8)
if q1.button("NVIDIA 🇺🇸"): symbol = "NASDAQ:NVDA"
if q2.button("ZOMATO 🇮🇳"): symbol = "NSE:ZOMATO"
if q3.button("PAYTM 🇮🇳"): symbol = "NSE:PAYTM"
if q4.button("BANKNIFTY 🇮🇳"): symbol = "NSE:BANKNIFTY"
if q5.button("SBI 🇮🇳"): symbol = "NSE:SBIN"
if q6.button("HDFC 🇮🇳"): symbol = "NSE:HDFCBANK"
if q7.button("MICROSOFT 🇺🇸"): symbol = "NASDAQ:MSFT"
if q8.button("ETH ₿"): symbol = "BINANCE:ETHUSDT"

st.markdown(f"### 📈 Live Chart: `{symbol}` - World Real TradingView")

# REAL TRADINGVIEW - WORLD - Allow Symbol Change = TRUE = World Search Inside Chart
tv_world_code = f"""
<div class="tradingview-widget-container" style="height:750px;width:100%">
  <div id="tradingview_world" style="height:750px;width:100%"></div>
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
    "withdateranges": true,
    "hide_side_toolbar": false,
    "allow_symbol_change": true,
    "details": true,
    "hotlist": true,
    "calendar": true,
    "studies": [
      "Volume@tv-basicstudies",
      "MAExp@tv-basicstudies"
    ],
    "support_host": "https://www.tradingview.com"
  }}
  );
  </script>
</div>
"""

components.html(tv_world_code, height=750)

st.success(f"✅ {symbol} - World Stock Live Sir! - Chart la top la symbol click panni vera stock search pannalam Sir!")

# HOW TO SEARCH WORLD STOCKS
st.markdown("""
<div style='background:linear-gradient(135deg,#667eea,#764ba2); padding:20px; border-radius:12px; color:white;'>
<h4>🌍 WORLD ELLA STOCK EPPADI THEADARATHU SIR:</h4>

<b>Method 1 - Direct Type (Ella Stock):</b><br>
• India: BSE:SENSEX, NSE:RELIANCE, NSE:TCS, NSE:ZOMATO, NSE:PAYTM, NSE:SBIN<br>
• USA: NASDAQ:AAPL, NASDAQ:TSLA, NYSE:BABA, NASDAQ:NVDA, NASDAQ:GOOGL, NASDAQ:MSFT<br>
• Crypto: BINANCE:BTCUSDT, BINANCE:ETHUSDT, BINANCE:DOGEUSDT<br>
• Forex: FX:EURUSD, FX:USDJPY, FX:GBPUSD<br>
• London: LSE:HSBA, LSE:BP<br>
• Japan: TSE:7203 (Toyota)<br><br>

<b>Method 2 - Chart Inside Search (Easy):</b><br>
• Chart la mela irukura Symbol (BSE:SENSEX) mela click pannunga Sir<br>
• TradingView Search Box varum Sir - Anga "APPLE" "RELIANCE" nu type pannuna world stocks ellam varum Sir<br>
• 50,000+ Stocks Search Pannalam Sir!<br><br>

<b>Method 3 - Quick Buttons:</b><br>
• Mela irukura Button click pannunga Sir - Direct ah stock maarum Sir<br><br>

<b>⚡ allow_symbol_change = true Sir - Chart ullaye world full search irukku Sir!</b>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption(f"🌍 WORLD FULL STOCKS - {symbol} - Real TradingView - 50,000+ Stocks Search - allow_symbol_change true - World Search Inside Chart")

# World Market List for Reference
with st.expander("🌍 World Market Full List Paarkalam Sir - Click Pannunga"):
    st.markdown("""
    **INDIA 🇮🇳** - BSE: , NSE: (RELIANCE, TCS, INFY, ZOMATO, PAYTM, IRCTC, HAL, RVNL, SUZLON, YESBANK)
    
    **USA NASDAQ 🇺🇸** - NASDAQ: (AAPL, TSLA, GOOGL, MSFT, NVDA, META, AMZN, NFLX, AMD, INTC)
    
    **USA NYSE 🇺🇸** - NYSE: (BABA, BRK.A, JPM, BAC, WMT, KO, DIS)
    
    **CRYPTO ₿** - BINANCE: (BTCUSDT, ETHUSDT, BNBUSDT, DOGEUSDT, SHIBUSDT)
    
    **FOREX 💱** - FX: (EURUSD, USDJPY, GBPUSD, USDINR)
    
    **LONDON 🇬🇧** - LSE: (HSBA, BP, VOD, BARC)
    
    **JAPAN 🇯🇵** - TSE: (7203 Toyota, 6758 Sony)
    
    **Type pannunga Sir - Ella Stock Varum Sir! Ex: NASDAQ:AAPL, NSE:RELIANCE, BINANCE:BTCUSDT**
    """)
