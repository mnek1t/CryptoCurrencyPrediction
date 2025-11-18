from fastapi import FastAPI
import dotenv
from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np
import joblib

app = FastAPI()

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = '%H:%M'
MULTIPLIER = 1
TIMESPAN = "hour"
PLAN_DATE = datetime.today() - timedelta(days=1)
TO = PLAN_DATE.strftime(DATE_FORMAT)
FROM = (PLAN_DATE - timedelta(hours=50)).strftime(DATE_FORMAT)
POLYGON_URL = "https://api.polygon.io"
COIN_NAME = "ETH"
CURRENCY = "USD"
#model = joblib.load("eth_xgb_model.pkl")

FEATURES = {
    "v": "volume",
    "vw": "volume-weighted",
    "o": "open",
    "c": "closed",
    "h": "highest",
    "l": "lowest",
    "t": "timestamp",
    "n": "n_transactions"
}
@app.get("/predict")
async def predict_price():
    df = get_latest_market_data() 
    print('======================DATA IS RECEIVED======================')
    # 2. Compute indicators
    df = compute_indicators(df)
    print(df.head())
    print(df.tail())
    
    # 3. Prepare features
    X = df[FEATURES.values()].iloc[-1:].values
    print(X)
    # 4. Predict
    #pred = model.predict(X)[0]
    
    # return {
    #     "predicted_next_close": float(pred)
    # }

def get_latest_market_data(entries : int = 50) -> pd.DataFrame:
    polygonApiKey = dotenv.get_key(".env", "POLYGON_API_KEY")

    url = f"{POLYGON_URL}/v2/aggs/ticker/X:{COIN_NAME}{CURRENCY}/range/{MULTIPLIER}/{TIMESPAN}/{FROM}/{TO}"
    response = requests.get(
        url=url,
        params={
            "apiKey": polygonApiKey,
            "sort": "asc"
            #"limit": entries
        }
    )
    if response.status_code != 200:
        raise Exception(response.json().get("error"))

    return process_polygon_responses(response)

def process_polygon_responses(response) -> pd.DataFrame: 
    status = response.json().get("status", None)
    if status != "OK":
        raise Exception("Status of response is not completed, got: " + status)
    
    data = response.json().get("results", None)
    if not data:
        raise Exception("No results found in the response")
    
    historical_prices_df = pd.DataFrame(data)

    # adjust data
    historical_prices_df["t"] = pd.to_datetime(historical_prices_df["t"], unit="ms")
    
    historical_prices_df = historical_prices_df.rename(columns={
        "v": "volume",
        "vw": "volume-weighted",
        "o": "open",
        "c": "closed",
        "h": "highest",
        "l": "lowest",
        "t": "timestamp",
        "n": "n_transactions"
    })
    historical_prices_df["volume"] = (
        historical_prices_df["volume"]
        .replace({r'\.': ''}, regex=True)   # remove dots
        .apply(pd.to_numeric, errors='coerce')
    )

    historical_prices_df["volume-weighted"] = (
        historical_prices_df["volume-weighted"]
        .replace({r'\.': ''}, regex=True)   # remove dots
        .apply(pd.to_numeric, errors='coerce')
    )

    # Convert relevant columns to numeric
    numeric_cols = ['open', 'highest', 'lowest', 'closed', 'volume', 'volume-weighted', 'n_transactions']
    historical_prices_df[numeric_cols] = historical_prices_df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    return historical_prices_df 

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

def compute_indicators(df: pd.DataFrame):
    calculate_atr(df)
    calculate_obv(df)
    calculate_rsi(df)
    calculate_sma(df)
    return df
