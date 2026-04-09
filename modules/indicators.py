"""
指标计算模块 — 实现熊猫笔记中的AI决策规则
"""
import pandas as pd

def compute_dr007_deviation(dr007: float, policy_rate: float = 1.5) -> float:
    """计算DR007偏离幅度(bp)"""
    return (dr007 - policy_rate) * 100

def classify_liquidity_tier(r_dr_spread: float) -> tuple:
    """流动性分层分类"""
    if r_dr_spread < 10:
        return "充裕", "green", "非银杠杆策略友好"
    elif r_dr_spread < 30:
        return "正常", "blue", "正常范围"
    elif r_dr_spread < 50:
        return "偏紧", "orange", "警惕理财赎回和信用债抛售"
    elif r_dr_spread < 100:
        return "紧张", "red", "非银流动性严重承压"
    else:
        return "危机", "darkred", "流动性危机模式"

def compute_cb_net_injection(df: pd.DataFrame, lookback_days: int = 30) -> float:
    """计算央行净投放"""
    if df is None or df.empty:
        return 0.0
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=lookback_days)
    recent = df[df["操作日期"] >= cutoff]
    net = 0.0
    for _, row in recent.iterrows():
        vol = row["交易量"]
        direction = row["正/逆回购"]
        if direction == "逆回购":
            net += vol
        elif direction == "正回购":
            net -= vol
    return net

def compute_liquidity_score(dr007_dev: float, r_dr_spread: float, net_inj: float) -> int:
    """综合流动性评分 0-100"""
    score = 50
    if abs(dr007_dev) < 10:
        score += 15
    elif abs(dr007_dev) > 50:
        score -= 20
    if r_dr_spread < 10:
        score += 15
    elif r_dr_spread > 50:
        score -= 20
    if net_inj > 1000:
        score += 10
    elif net_inj < -500:
        score -= 15
    return max(0, min(100, score))
