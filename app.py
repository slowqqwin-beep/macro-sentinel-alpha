import streamlit as st
st.set_page_config(page_title="Macro Sentinel Alpha", page_icon="📊", layout="wide")
st.title("🏦 Macro Sentinel Alpha · 流动性监控仪表盘")
st.markdown("基于《熊猫笔记》AI决策框架 · 实时监控核心流动性指标")

from modules.data_fetcher import fetch_shibor, fetch_cb_open_market, fetch_cnh_spot, fetch_cnh_hibor
from modules.indicators import compute_cb_net_injection, compute_liquidity_score, classify_liquidity_tier
from modules.charts import plot_rate_chart, plot_cb_gauge, plot_cnh_pressure, plot_liquidity_gauge

# 数据加载
df_shibor = fetch_shibor()
df_cb = fetch_cb_open_market()
df_cnh_spot = fetch_cnh_spot()
df_cnh_hibor = fetch_cnh_hibor()

# 指标卡
col1, col2, col3 = st.columns(3)
with col1:
    on_val = df_shibor["SHIBOR_O/N"].iloc[-1] if not df_shibor.empty else None
    st.metric("SHIBOR隔夜", f"{on_val:.4f}%" if on_val else "N/A")
with col2:
    net = compute_cb_net_injection(df_cb)
    st.metric("近30日净投放", f"{net:.0f} 亿元")
with col3:
    r_dr_spread = 25.0
    tier, color, _ = classify_liquidity_tier(r_dr_spread)
    st.metric("R007-DR007利差(估)", f"{r_dr_spread:.0f} bp")
    st.markdown(f"**分层**: :{color}[{tier}]")

# 图表
col_left, col_right = st.columns(2)
with col_left:
    st.subheader("SHIBOR利率")
    if not df_shibor.empty:
        st.plotly_chart(plot_rate_chart(df_shibor), use_container_width=True)
with col_right:
    st.subheader("央行操作仪表盘")
    total = df_cb[df_cb["操作日期"] >= pd.Timestamp.now() - pd.Timedelta(days=30)]["交易量"].sum() if not df_cb.empty else 0
    st.plotly_chart(plot_cb_gauge(net, total), use_container_width=True)

st.subheader("CNH跨境压力")
st.plotly_chart(plot_cnh_pressure(df_cnh_spot, df_cnh_hibor), use_container_width=True)

st.subheader("AI综合评分")
score = compute_liquidity_score((df_shibor["SHIBOR_1W"].iloc[-1]-1.5)*100 if not df_shibor.empty else 0, 25, net)
st.plotly_chart(plot_liquidity_gauge(score), use_container_width=True)
