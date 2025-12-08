import pandas as pd
import numpy as np
def calculate_obv(df: pd.DataFrame):
    obv = [0]
    for i in range(1, len(df)):
        if df.loc[i, 'closed'] > df.loc[i - 1, 'closed']:
            obv.append(obv[-1] + df.loc[i, 'volume'])
        elif df.loc[i, 'closed'] < df.loc[i - 1, 'closed']:
            obv.append(obv[-1] - df.loc[i, 'volume'])
        else:
            obv.append(obv[-1])
    df['OBV'] = obv

def calculate_atr(df: pd.DataFrame, period: int = 14):
    high_low = df['highest'] - df['lowest']
    high_close_prev = (df['highest'] - df['closed'].shift()).abs()
    low_close_prev = (df['lowest'] - df['closed'].shift()).abs()
    true_range = pd.concat([high_low, high_close_prev, low_close_prev], axis=1).max(axis=1)
    df[f'ATR_{period}'] = true_range.rolling(window=period).mean()

def calculate_rsi(df: pd.DataFrame, period: int = 14):
    series = df["closed"] 

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    df[f"RSI_{period}"] = 100 - (100 / (1 + rs))

def calculate_sma(df: pd.DataFrame, period: int = 50):
    df[f'SMA_{period}'] = df['closed'].rolling(window=period).mean()

def convert_time(df: pd.DataFrame):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['dayofweek'] = df['timestamp'].dt.dayofweek

    df['hour_sin'] = np.sin(2 * np.pi * df['hour']/24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour']/24)
    df['dow_sin']  = np.sin(2 * np.pi * df['dayofweek']/7)
    df['dow_cos']  = np.cos(2 * np.pi * df['dayofweek']/7)