import { useState, useEffect } from "react";
import CryptoChart from "./components/CryptoChart";
import PredictionPanel from "./components/PredictionPanel";
import "./App.css";

export default function App() {
  const [selectedCoin, setSelectedCoin] = useState("ethereum");
  return (
    <div className="app-container">
      <header className="app-header">
        <div>
          <h1>Crypto Currency Prediction App</h1>
          <p>Ethereum price insights & prediction</p>
        </div>

        {/* Dropdown */}
        <select
          className="crypto-dropdown"
          value={selectedCoin}
          onChange={(e) => setSelectedCoin(e.target.value)}
        >
          <option value="ethereum">ETH</option>
        </select>
      </header>

      <main className="content">
        <PredictionPanel />
        <CryptoChart coin={selectedCoin} />
      </main>

      <footer className="app-footer">
        Information Retrieval project – CryptoCurrencyPrediction
      </footer>
    </div>
  );
}
