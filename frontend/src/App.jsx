import { useState, useEffect } from "react";
import CryptoChart from "./components/CryptoChart";
import PredictionPanel from "./components/PredictionPanel";
import CustomDropdown from "./components/CustomDropdown"
import "./App.css";

const API_URL = "http://127.0.0.1:8000";
export default function App() {
  const [selectedCoin, setSelectedCoin] = useState("ethereum");
  const [selectedCurrency, setSelectedCurrency] = useState("usd");
  const [availableTickers, setAvailableTickers] = useState([]);
  const [availableCurrencies, setAvailableCurrencies] = useState([]);
  useEffect(() => {
    const loadTickers = async () => {
      try {
        const res = await fetch(API_URL + '/api/ticker');
        const data = await res.json();
        setAvailableTickers(data.tickers || []);
        setAvailableCurrencies(data.currencies || []);
      } catch(err){
        console.error("Failed to load tickers:", err);
      }
    }

    loadTickers();
  }, [])
  return (
    <div className="app-container">
      <header className="app-header">
        <div>
          <h1>Crypto Currency Prediction App</h1>
          <p>{selectedCoin.charAt(0).toUpperCase() + selectedCoin.slice(1)} price insights & prediction</p>
        </div>

        <div className='dropdown-options'>
          <CustomDropdown
            label="Currency"
            value={selectedCurrency}
            options={availableCurrencies}
            onChange={setSelectedCurrency}
          />

          <CustomDropdown
            label="Coin"
            value={selectedCoin}
            options={availableTickers}
            onChange={setSelectedCoin}
          />
        </div>

      </header>

      <main className="content">
        <PredictionPanel />
        <CryptoChart coin={selectedCoin} currency={selectedCurrency}/>
      </main>

      <footer className="app-footer">
        Information Retrieval – Crypto Currency Prediction Project
      </footer>
    </div>
  );
}
