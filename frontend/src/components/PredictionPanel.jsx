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
      setPrediction(Math.round(data.predicted_next_close  * 100)/100|| JSON.stringify(data));
    } catch (err) {
      setError("Failed to fetch prediction.");
    } finally {
      setLoading(false);
    }
  };
  const now = new Date();
  const nextHour = new Date(now);
  nextHour.setHours(now.getHours() + 1, 0, 0, 0); // next hour, minutes = 0
  const targetTimeStr = nextHour.toLocaleString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
    day: "numeric",
    month: "short",
  });

  return (
    <section className="panel prediction-panel">
      <h2>Prediction</h2>
      <p className="panel-subtitle">Hit the button to get a closed price prediction for <strong>{targetTimeStr}</strong>.</p>

      <button className="primary-btn" onClick={handlePredict} disabled={loading}>
        {loading ? <span className="loader"></span> : "Predict"}
      </button>

      <div className="result-box">
        <div className="result-title">Prediction result</div>
        <div className="result-text">{prediction}</div>
      </div>

      {error && <div className="error-text">{error}</div>}
    </section>
  );
}
