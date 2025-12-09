from motor.motor_asyncio import AsyncIOMotorClient
import dotenv 

client = None
db = None
predictions_col = None

def start_db():
    global client, db, predictions_col
    MONGO_URI = dotenv.get_key(".env", "MONGO_URI")
    DB_NAME = dotenv.get_key(".env", "MONGO_DB")
    if MONGO_URI is None or DB_NAME is None:
        raise ValueError("MONGO_URI and MONGO_DB must be set in environment variables")
    
    
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    predictions_col = db["predictions"]

def close_db():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")

def get_predictions_col():
    global client, db
    if client is None or db is None:
        raise RuntimeError("Database not initialized")
    return db["predictions"]
