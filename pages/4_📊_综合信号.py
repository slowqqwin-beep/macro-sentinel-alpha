import streamlit as st
from modules.data_fetcher import fetch_shibor, fetch_cb_open_market
from modules.indicators import compute_liquidity_score, compute_cb_net_injection
from modules.charts import plot_liquidity_gauge

st.set_page_config(page_title="综合信号", page_icon="📊")
st.title("📊 AI综合流动性评分")
shibor = fetch_shibor()
cb = fetch_cb_open_market()
if not shibor.empty:
    dr007 = shibor["SHIBOR_1W"].iloc[-1]
    dev = (dr007 - 1.5) * 100
    r_dr_spread = 25  # 占位，实际需计算R007
    net_inj = compute_cb_net_injection(cb)
    score = compute_liquidity_score(dev, r_dr_spread, net_inj)
    st.plotly_chart(plot_liquidity_gauge(score), use_container_width=True)
    st.metric("综合评分", f"{score}/100")
else:
    st.warning("数据获取失败")
