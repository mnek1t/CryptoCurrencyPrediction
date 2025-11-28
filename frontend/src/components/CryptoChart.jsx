import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Filler);

export default function CryptoChart({ coin }) {
  const [labels, setLabels] = useState([]);
  const [prices, setPrices] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const url = `https://api.coingecko.com/api/v3/coins/${coin}/market_chart?vs_currency=usd&days=7`;
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
          vals.push(price);
        });

        setLabels(times);
        setPrices(vals);
      } catch (err) {
        console.error("Chart load error:", err);
      }
    };

    loadData();
  }, [coin]);

  const chartData = {
    labels,
    datasets: [
      {
        label: `${coin.toUpperCase()} Price (USD)`,
        data: prices,
        tension: 0.35,
        fill: true,
        backgroundColor: "rgba(129, 140, 248, 0.18)",
        borderColor: "rgba(129, 140, 248, 0.95)",
        borderWidth: 2,
        pointRadius: 0,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
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
      <h2>{coin.toUpperCase()} Price by CoinGecko</h2>
      <p className="panel-subtitle">Hourly price data for the last 7 days.</p>

      <div style={{ height: "300px" }}>
        <Line data={chartData} options={chartOptions} />
      </div>
    </section>
  );
}