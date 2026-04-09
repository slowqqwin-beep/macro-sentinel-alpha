import streamlit as st
import pandas as pd
from modules.data_fetcher import fetch_cb_open_market
from modules.indicators import compute_cb_net_injection

st.set_page_config(page_title="央行操作", page_icon="🏦")
st.title("🏦 央行公开市场操作")
df = fetch_cb_open_market()
if not df.empty:
    days = st.slider("天数", 7, 90, 30)
    net = compute_cb_net_injection(df, days)
    st.metric("净投放", f"{net:.0f} 亿元")
    recent = df[df["操作日期"] >= pd.Timestamp.now() - pd.Timedelta(days=days)]
    st.dataframe(recent.sort_values("操作日期", ascending=False))
else:
    st.warning("数据获取失败")
