import { useState } from "react";

const API_URL = "http://127.0.0.1:8000/predict";

export default function PredictionPanel() {
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState("No prediction yet.");
  const [error, setError] = useState("");

  const handlePredict = async () => {
    setError("");
    setLoading(true);

    try {
      const res = await fetch(API_URL);
      if (!res.ok) throw new Error("Backend error");

      const data = await res.json();
      setPrediction(data.predicted_next_close || JSON.stringify(data));
    } catch (err) {
      setError("Failed to fetch prediction.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="panel prediction-panel">
      <h2>Prediction</h2>
      <p className="panel-subtitle">Hit the button to get a closed price prediction.</p>

      <button className="primary-btn" onClick={handlePredict} disabled={loading}>
        {loading ? "Predicting..." : "Predict"}
      </button>

      <div className="result-box">
        <div className="result-title">Prediction result</div>
        <div className="result-text">{prediction}</div>
      </div>

      {error && <div className="error-text">{error}</div>}
    </section>
  );
}
