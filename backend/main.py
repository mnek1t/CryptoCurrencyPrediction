from contextlib import asynccontextmanager
from fastapi import FastAPI
import pandas as pd
import joblib
import services.polygon_io as polygon
import services.trading.technical_indicators as technical_indicators
from constants import FEATURES
import database
from datetime import datetime

#model = joblib.load("eth_xgb_model.pkl")

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.start_db()
    yield
    database.close_db()

app = FastAPI(lifespan=lifespan)

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
    #predicted_close = model.predict(X)[0]
    
    # 5. Save to DB
    row = {
        "timestamp": datetime.now(),
        "model_name": 'eth_xgb_model',
        "ticker": 'X:ETHUSD',
        "predicted_close": 1239.56,
        "actual_close": None
    }
    await database.get_predictions_col().insert_one(row)

    # return {
    #     "predicted_next_close": float(pred)
    # }

def compute_indicators(df: pd.DataFrame):
    technical_indicators.calculate_atr(df)
    technical_indicators.calculate_obv(df)
    technical_indicators.calculate_rsi(df)
    technical_indicators.calculate_sma(df)
    return df