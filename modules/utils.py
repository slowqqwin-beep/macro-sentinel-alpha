"""工具函数"""
import pandas as pd

def safe_float_convert(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")
