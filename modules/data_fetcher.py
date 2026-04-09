"""
数据拉取模块 — 基于AkShare获取中国流动性核心指标
"""
import akshare as ak
import pandas as pd
from datetime import datetime
import streamlit as st


@st.cache_data(ttl=3600)
def fetch_shibor() -> pd.DataFrame:
    """获取SHIBOR利率"""
    df = ak.macro_china_shibor_all()
    if df is not None and not df.empty:
        df = df[["日期", "O/N-定价", "1W-定价"]]
        df.columns = ["date", "SHIBOR_O/N", "SHIBOR_1W"]
        df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data(ttl=3600)
def fetch_cb_open_market() -> pd.DataFrame:
    """获取央行公开市场操作"""
    # 正确的函数名是 macro_china_gksccz
    df = ak.macro_china_gksccz()
    if df is not None and not df.empty:
        df["操作日期"] = pd.to_datetime(df["操作日期"])
        df["交易量"] = pd.to_numeric(df["交易量"], errors="coerce")
        df["中标利率"] = pd.to_numeric(df["中标利率"], errors="coerce")
    return df


@st.cache_data(ttl=3600)
def fetch_money_supply() -> pd.DataFrame:
    """获取货币供应量"""
    df = ak.macro_china_money_supply()
    if df is not None and not df.empty:
        df = df[["月份", "M2同比", "M1同比", "M0同比"]]
    return df


@st.cache_data(ttl=3600)
def fetch_forex_reserve() -> pd.DataFrame:
    """获取外汇储备"""
    return ak.macro_china_forex_reserve()


@st.cache_data(ttl=3600)
def fetch_cnh_spot() -> pd.DataFrame:
    """获取USD/CNH汇率"""
    # 正确的函数名是 forex_hist_em
    df = ak.forex_hist_em(symbol="USDCNH")
    if df is not None and not df.empty:
        df = df.rename(columns={
            "日期": "date",
            "最新价": "close",
            "今开": "open",
            "最高": "high",
            "最低": "low"
        })
        df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data(ttl=3600)
def fetch_cnh_hibor() -> pd.DataFrame:
    """获取CNH HIBOR"""
    return ak.macro_china_hk_rate_of_interest()


@st.cache_data(ttl=3600)
def fetch_social_financing() -> pd.DataFrame:
    """获取社会融资规模"""
    return ak.macro_china_shrzgm()
