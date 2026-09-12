# app/utils.py
import pandas as pd

ACCEL_FEATURES = [
    "LAT", "LON", "WIND_KTS", "PRES_MB",
    "WIND_DELTA_1", "PRES_DELTA_1",
    "WIND_TREND_3", "PRES_TREND_3",
    "WIND_TREND_6", "PRES_TREND_6",
    "STORM_AGE_H", "STORM_SPEED", "DIST2LAND",
    "WIND_ACCEL", "PRES_ACCEL"
]

DEPLOYED_THRESHOLD = {"+6h": 0.25, "+12h": 0.20, "+24h": 0.15}
INTENSIFY_THRESHOLD_KT = {"+6h": 5, "+12h": 7, "+24h": 10}

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["SID", "ISO_TIME"]).copy()
    df["ISO_TIME"] = pd.to_datetime(df["ISO_TIME"])
    g = df.groupby("SID")

    df["WIND_DELTA_1"] = g["WIND_KTS"].diff()
    df["PRES_DELTA_1"] = g["PRES_MB"].diff()
    df["STORM_AGE_H"] = (df["ISO_TIME"] - g["ISO_TIME"].transform("min")).dt.total_seconds() / 3600
    df["WIND_TREND_3"] = g["WIND_KTS"].transform(lambda s: s.diff().rolling(3, min_periods=1).mean())
    df["PRES_TREND_3"] = g["PRES_MB"].transform(lambda s: s.diff().rolling(3, min_periods=1).mean())
    df["WIND_TREND_6"] = g["WIND_KTS"].transform(lambda s: s.diff().rolling(6, min_periods=2).mean())
    df["PRES_TREND_6"] = g["PRES_MB"].transform(lambda s: s.diff().rolling(6, min_periods=2).mean())

    df["STORM_SPEED"] = pd.to_numeric(df["STORM_SPEED"], errors="coerce")
    df["DIST2LAND"] = pd.to_numeric(df["DIST2LAND"], errors="coerce")
    return df

def add_acceleration(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["WIND_ACCEL"] = df["WIND_TREND_3"] - df["WIND_TREND_6"]
    df["PRES_ACCEL"] = df["PRES_TREND_3"] - df["PRES_TREND_6"]
    return df