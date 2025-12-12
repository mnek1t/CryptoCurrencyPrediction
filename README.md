# CryptoCurrencyPrediction — Backend
Information Retrieval(English)(1),25/26-R
A clean, modern, and well‑structured backend powering the **CryptoCurrencyPrediction** project.  
Handles **data ingestion**, **model training**, and **cryptocurrency price prediction APIs**.

---

## Overview
The backend provides:
- Fast and clean REST API endpoints  
- Machine‑learning model training & evaluation  
- Data‑fetching and preprocessing pipelines  
- Docker-ready deployment  
- Easy project structure for extension

---

## Project Structure
backend/
├── app/            
├── models/          
├── scripts/          
├── data/            
├── configs/        
└── requirements.txt

frontend/
├── app/            
├── public/          

docker-compose.yml
---

##  Installation
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

---

## Environment Variables
APP_HOST=0.0.0.0
APP_PORT=8000
DATA_PATH=./data
MODEL_PATH=./models

---

## Running the API
uvicorn app.main:app --reload --host ${APP_HOST:-127.0.0.1} --port ${APP_PORT:-8000}

---

## API Endpoints
GET /health  
POST /predict  
GET /models  
POST /train  

---

## Training Models
python scripts/train.py --config configs/train.yaml

---

## Docker Support
docker build -t cryptocurrency-backend .
docker run -p 8000:8000 --env-file .env cryptocurrency-backend

---

## Running Tests
pytest -q

---

## Contributing
Fork → Branch → PR

---

## License
Specify license here.
