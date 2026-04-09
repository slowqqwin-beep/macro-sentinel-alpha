import streamlit as st
from modules.data_fetcher import fetch_cnh_spot, fetch_cnh_hibor
from modules.charts import plot_cnh_pressure

st.set_page_config(page_title="CNH压力", page_icon="🌊")
st.title("🌊 CNH跨境流动性监测")
spot = fetch_cnh_spot()
hibor = fetch_cnh_hibor()
st.plotly_chart(plot_cnh_pressure(spot, hibor), use_container_width=True)
latest = hibor["隔夜"].iloc[-1] if not hibor.empty else None
if latest:
    if latest > 10:
        st.error(f"⚠️ HIBOR隔夜 {latest:.2f}% 危机预警")
    elif latest > 5:
        st.warning(f"⚠️ HIBOR隔夜 {latest:.2f}% 偏紧")
    else:
        st.success(f"✅ HIBOR隔夜 {latest:.2f}% 正常")
