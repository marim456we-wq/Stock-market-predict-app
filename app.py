import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date, timedelta
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="BATCH-5 Stock Prediction", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1f77b4;'>859 - TJS POLYTECHNIC COLLEGE</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>DEPT OF AI & ML - BATCH 5 - Stock Price Trend Prediction</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Guide: Mrs. S.Tamil Selvi B.Tech., | Students: Veeraraghavan.S (25508695) & Perumal.M (25508689)</b></p>", unsafe_allow_html=True)
st.divider()

# Sidebar
st.sidebar.header("Configuration")
ticker = st.sidebar.selectbox("Select Stock
