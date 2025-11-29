from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import services.polygon_io as polygon
import services.trading.technical_indicators as technical_indicators
from constants import FEATURES

app = FastAPI()
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#model = joblib.load("eth_xgb_model.pkl")

@app.get("/predict")
async def predict_price():
    df = polygon.get_latest_market_data() 
    
    # 2. Compute indicators
    df = compute_indicators(df)
    print(df.head())
    print(df.tail())
    
    # 3. Prepare features
    X = df[FEATURES.values()].iloc[-1:].values
    print(X)
    
    # 4. Predict
    #pred = model.predict(X)[0]
    
    return {
        "predicted_next_close": 3001.42
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