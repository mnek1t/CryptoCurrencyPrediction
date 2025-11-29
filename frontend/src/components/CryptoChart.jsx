import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import { IoReload } from "react-icons/io5";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Filler, Tooltip, Legend);


export default function CryptoChart({ coin, currency}) {
  const [labels, setLabels] = useState([]);
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(false);
  const loadData = async () => {
    try {
      setLoading(true);

      const url = `https://api.coingecko.com/api/v3/coins/${coin}/market_chart?vs_currency=${currency}&days=7`;
      const res = await fetch(url);
      const data = await res.json();

      const times = [];
      const vals = [];

      data.prices.forEach(([timestamp, price]) => {
        const date = new Date(timestamp);
        times.push(
          date.toLocaleString("en-US", {
            day: "numeric",
            month: "short",
            hour: "2-digit",
          })
        );
        vals.push(price.toFixed(2));
      });

      setLabels(times);
      setPrices(vals);
    } catch (err) {
      console.error("Chart load error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [coin, currency]);

  const chartData = {
    labels,
    datasets: [
      {
        label: `${coin.toUpperCase()} Price (${currency.toUpperCase()})`,
        data: prices,
        tension: 0.35,
        fill: true,
        backgroundColor: "rgba(129, 140, 248, 0.18)",
        borderColor: "rgba(129, 140, 248, 0.95)",
        borderWidth: 2,
        pointRadius: 0,
        pointHitRadius: 15,
        pointHoverRadius: 6,
        pointHoverBackgroundColor: "rgba(129, 140, 248, 1)",
      },
    ]

  };

  const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,

  onHover: (event) => {
    event.native.target.style.cursor = "pointer";
  },

  plugins: {
    legend: { display: false },

    tooltip: {
      enabled: true,
      backgroundColor: "rgba(15, 23, 42, 0.9)",
      titleColor: "#fff",
      bodyColor: "#cbd5e1",
      borderColor: "rgba(255,255,255,0.15)",
      borderWidth: 1,
      padding: 10,
      displayColors: false,
      callbacks: {
        label: (context) => `Price: ${context.raw} ${currency.toUpperCase()}`,
      },
    },
  },

  scales: {
    x: {
      ticks: { color: "rgba(226,232,240,0.8)", maxTicksLimit: 10 },
    },
    y: {
      ticks: { color: "rgba(226,232,240,0.8)" },
    },
  },
};


  return (
    <section className="panel chart-panel">
      <div className="chart-header">
        <button className="refresh-btn" onClick={loadData} disabled={loading}>
          {loading ? <span className="loader"></span> : (<IoReload size={18} color="white" />)}
        </button>
        <h2>{coin.charAt(0).toUpperCase() + coin.slice(1)} Price by CoinGecko</h2>
      </div>
      <p className="panel-subtitle">Hourly price data for the last 7 days.</p>

      <div style={{ height: "300px" }}>
        <Line data={chartData} options={chartOptions} />
      </div>
    </section>
  );
}