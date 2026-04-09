import streamlit as st
from modules.data_fetcher import fetch_shibor
from modules.charts import plot_rate_chart

st.set_page_config(page_title="资金利率", page_icon="💰")
st.title("💰 资金利率监控")
df = fetch_shibor()
if not df.empty:
    st.plotly_chart(plot_rate_chart(df), use_container_width=True)
    st.dataframe(df.tail(10))
else:
    st.warning("数据获取失败")
