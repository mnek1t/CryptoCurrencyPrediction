from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# CORS (not strictly needed once same-origin, but it doesn't hurt)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Backend API ===
@app.get("/predict")
async def predict_price():
    # Very simple dummy prediction for now
    return {"predicted_next_close": 1239.56}


# === Frontend (static files) ===
# Serve everything in the "public" folder at the root ("/")
# Visiting http://127.0.0.1:8000/ will serve public/index.html
app.mount("/", StaticFiles(directory="public", html=True), name="public")
