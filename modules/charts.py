"""
可视化模块 — 基于Plotly
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def plot_rate_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["SHIBOR_O/N"], mode="lines", name="SHIBOR隔夜"))
    fig.add_trace(go.Scatter(x=df["date"], y=df["SHIBOR_1W"], mode="lines", name="SHIBOR 1W"))
    fig.add_hline(y=1.5, line_dash="dash", annotation_text="7天逆回购(1.5%)")
    fig.update_layout(title="SHIBOR走势", xaxis_title="日期", yaxis_title="利率(%)", height=400)
    return fig

def plot_cb_gauge(net_injection: float, total_volume: float) -> go.Figure:
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "indicator"}, {"type": "indicator"}]])
    fig.add_trace(go.Indicator(mode="number", value=net_injection, title={"text": "净投放(亿)"}), row=1, col=1)
    fig.add_trace(go.Indicator(mode="number", value=total_volume, title={"text": "总操作量(亿)"}), row=1, col=2)
    fig.update_layout(height=250)
    return fig

def plot_liquidity_gauge(score: int) -> go.Figure:
    color = "green" if score >= 70 else ("orange" if score >= 40 else "red")
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score, domain={"x": [0,1], "y": [0,1]},
        gauge={"axis": {"range": [0,100]}, "bar": {"color": color},
               "steps": [{"range": [0,40], "color": "rgba(255,0,0,0.3)"},
                         {"range": [40,70], "color": "rgba(255,165,0,0.3)"},
                         {"range": [70,100], "color": "rgba(0,255,0,0.3)"}]}
    ))
    fig.update_layout(height=300)
    return fig

def plot_cnh_pressure(spot_df: pd.DataFrame, hibor_df: pd.DataFrame) -> go.Figure:
    fig = make_subplots(rows=2, cols=1, subplot_titles=("USD/CNH", "CNH HIBOR隔夜"))
    if not spot_df.empty:
        fig.add_trace(go.Scatter(x=spot_df["date"], y=spot_df["close"], name="CNH"), row=1, col=1)
    if not hibor_df.empty:
        fig.add_trace(go.Scatter(x=hibor_df["日期"], y=hibor_df["隔夜"], name="HIBOR"), row=2, col=1)
        fig.add_hline(y=10, line_dash="dash", line_color="orange", row=2, col=1)
    fig.update_layout(height=500)
    return fig
