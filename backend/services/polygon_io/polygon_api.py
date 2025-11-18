import dotenv
import requests
import pandas as pd
from constants import COIN_NAME, CURRENCY, POLYGON_URL, MULTIPLIER, TIMESPAN, FROM, TO 
from typing import Any, Dict

def get_latest_market_data(entries : int = 50) -> pd.DataFrame:
    polygonApiKey = dotenv.get_key(".env", "POLYGON_API_KEY")

    url = f"{POLYGON_URL}/v2/aggs/ticker/X:{COIN_NAME}{CURRENCY}/range/{MULTIPLIER}/{TIMESPAN}/{FROM}/{TO}"
    response : requests.Response = requests.get(
        url=url,
        params={
            "apiKey": polygonApiKey,
            "sort": "asc"
            #"limit": entries
        }
    )
    response_json : Dict[str, Any] = response.json()
    if response.status_code != 200:
        raise Exception(response_json.get("error"))

    return process_polygon_responses(response_json)

def process_polygon_responses(response_json: Dict[str, Any]) -> pd.DataFrame: 
    status = response_json.get("status", None)
    if status != "OK":
        raise Exception("Status of response is not completed, got: " + status)
    
    data = response_json.get("results", None)
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
        .replace({r'\.': ''}, regex=True)
        .apply(pd.to_numeric, errors='coerce')
    )

    historical_prices_df["volume-weighted"] = (
        historical_prices_df["volume-weighted"]
        .replace({r'\.': ''}, regex=True)
        .apply(pd.to_numeric, errors='coerce')
    )

    # Convert relevant columns to numeric
    numeric_cols = ['open', 'highest', 'lowest', 'closed', 'volume', 'volume-weighted', 'n_transactions']
    historical_prices_df[numeric_cols] = historical_prices_df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    return historical_prices_df 