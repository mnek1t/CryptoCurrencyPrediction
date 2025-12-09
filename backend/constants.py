from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = '%H:%M'

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

# POLYGON API CONSTANTS
MULTIPLIER = 1
TIMESPAN = "hour"
PLAN_DATE = datetime.today() - timedelta(days=2)
TO = PLAN_DATE.strftime(DATE_FORMAT)
FROM = (PLAN_DATE - timedelta(hours=50)).strftime(DATE_FORMAT)
POLYGON_URL = "https://api.polygon.io"
COIN_NAME = "ETH"
CURRENCY = "USD"