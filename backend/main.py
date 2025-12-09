from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import services.polygon_io as polygon
import services.trading.technical_indicators as technical_indicators
from constants import FEATURES
import database
from datetime import datetime
import xgboost
from sklearn.preprocessing import StandardScaler
import joblib

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.start_db()
    yield
    database.close_db()

app = FastAPI(lifespan=lifespan)
origins = [
    "http://localhost:3000",
    "http://localhost:80"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = joblib.load("./model/eth_xgb_model.pkl")
scaler = joblib.load("./model/scaler.pkl")

@app.get("/predict")
async def predict_price():
    # 1. Get OHLCV Data from Polygon.io API
    df = polygon.get_latest_market_data() 
    
    # 2. Compute tehnical trading indicators
    df = compute_indicators(df)
    
    # 3. Convert timestamp to cyclic features
    technical_indicators.convert_time(df)
    df.pop('timestamp')

    # 4. Get news from API and calculate sentiment score
    if 'sentiment' not in df.columns:
        df['sentiment'] = 0  # default to 0
    
    # 3. Prepare features
    X = df[df.columns].iloc[-1:].values
    print(X)
    X_scaled = scaler.transform(X)
    # 4. Predict
    predicted_close = float(model.predict(X_scaled)[0])
    
    # 5. Save to DB
    row = {
        "timestamp": datetime.now(),
        "model_name": 'eth_xgb_model',
        "ticker": 'X:ETHUSD',
        "predicted_close": predicted_close,
        "actual_close": None
    }
    await database.get_predictions_col().insert_one(row)
    
    return {
        "predicted_next_close": predicted_close
    }

@app.get('/api/ticker')
async def get_available_tickers():
    return {
        "tickers": [
            "ETH"
        ],
        "currencies": {
            "USD"
        }
    }

def compute_indicators(df: pd.DataFrame):
    technical_indicators.calculate_atr(df)
    technical_indicators.calculate_obv(df)
    technical_indicators.calculate_rsi(df)
    technical_indicators.calculate_sma(df)
    return df