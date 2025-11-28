const API_URL = "http://127.0.0.1:8000/predict";
console.log("API_URL is:", API_URL);


document.addEventListener("DOMContentLoaded", () => {
  const predictBtn = document.getElementById("predictBtn");
  const resultText = document.getElementById("resultText");
  const errorText = document.getElementById("errorText");
  const amountInput = document.getElementById("amountInput"); // optional

  // Safety check: make sure elements exist
  console.log("predictBtn:", predictBtn);
  console.log("resultText:", resultText);
  console.log("errorText:", errorText);

  predictBtn.addEventListener("click", async () => {
    // clear previous error
    errorText.hidden = true;
    errorText.textContent = "";

    const originalText = predictBtn.textContent;
    predictBtn.disabled = true;
    predictBtn.textContent = "Predicting...";

    try {
      // You can send amount later if backend needs it.
      const amount = amountInput.value ? Number(amountInput.value) : null;
      console.log("Amount entered:", amount);

      // SIMPLE GET request
      const response = await fetch(API_URL);

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
      }

      const data = await response.json();

      const prediction =
        data.predicted_next_close ??
        data.prediction ??
        data.result ??
        data.message ??
        JSON.stringify(data);

      resultText.textContent = prediction;
    } catch (err) {
      console.error(err);
      errorText.hidden = false;
      errorText.textContent =
        "Failed to get prediction from backend: " + err.message;
    } finally {
      predictBtn.disabled = false;
      predictBtn.textContent = originalText;
    }
  });

  // ====== Ethereum demo chart (same as before) ======
  initEthChart();
});

function initEthChart() {
  const canvas = document.getElementById("ethChart");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  const labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const sampleData = [3250, 3320, 3180, 3400, 3550, 3480, 3620];

  // eslint-disable-next-line no-undef
  new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "ETH Price (USD)",
          data: sampleData,
          tension: 0.35,
          fill: true,
          backgroundColor: "rgba(129, 140, 248, 0.18)",
          borderColor: "rgba(129, 140, 248, 0.95)",
          borderWidth: 2,
          pointRadius: 3,
          pointBackgroundColor: "rgba(248, 250, 252, 0.9)",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
      },
      scales: {
        x: {
          grid: { color: "rgba(148, 163, 184, 0.15)" },
          ticks: {
            color: "rgba(226, 232, 240, 0.8)",
            font: { size: 10 },
          },
        },
        y: {
          grid: { color: "rgba(148, 163, 184, 0.18)" },
          ticks: {
            color: "rgba(226, 232, 240, 0.8)",
            font: { size: 10 },
          },
        },
      },
    },
  });
}
