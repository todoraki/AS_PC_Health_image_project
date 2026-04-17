import React from "react";

function ResultDisplay({ result }) {
  if (!result) return null;

  const { species, health, summary } = result;
  const isHealthy = health.status === "Healthy";
  const speciesPct = Math.max(0, Math.min(100, (species.confidence || 0) * 100));
  const healthPct = Math.max(0, Math.min(100, (health.confidence || 0) * 100));

  const interpretation =
    summary ||
    "The leaf exhibits no visible stress markers and aligns with healthy Prosopis Cineraria patterns.";

  return (
    <div className="card result-card result-dashboard reveal-in">
      <h2>AI Prediction Dashboard</h2>

      <div className="result-grid">
        <article className="result-box prediction-card">
          <div className="prediction-head">
            <div>
              <p className="label">Species Prediction</p>
              <h3 className="value">🌿 {species.name}</h3>
            </div>
            <div
              className="ring-progress"
              style={{
                background: `conic-gradient(#2c8f69 ${speciesPct}%, rgba(15, 61, 46, 0.12) ${speciesPct}% 100%)`,
              }}
            >
              <span>{speciesPct.toFixed(0)}%</span>
            </div>
          </div>

          <div className="confidence">Confidence score: {speciesPct.toFixed(1)}%</div>
          <div className="confidence-bar-wrap">
            <div
              className="confidence-bar"
              style={{ width: `${speciesPct}%` }}
            />
          </div>
        </article>

        <article
          className={`result-box prediction-card ${
            isHealthy ? "health-healthy" : "health-unhealthy"
          }`}
        >
          <div className="prediction-head">
            <div>
              <p className="label">Health Status</p>
              <h3 className="value">❤️ {health.status}</h3>
            </div>
            <div
              className="ring-progress"
              style={{
                background: `conic-gradient(${isHealthy ? "#2c8f69" : "#c44562"} ${healthPct}%, rgba(15, 61, 46, 0.12) ${healthPct}% 100%)`,
              }}
            >
              <span>{healthPct.toFixed(0)}%</span>
            </div>
          </div>

          <div className="confidence">Confidence score: {healthPct.toFixed(1)}%</div>
          <div className="confidence-bar-wrap">
            <div
              className="confidence-bar"
              style={{
                width: `${healthPct}%`,
                background: isHealthy ? "#40916c" : "#e63946",
              }}
            />
          </div>
        </article>
      </div>

      <div className="model-interpretation">
        <h3>Model Interpretation</h3>
        <p>{interpretation}</p>
      </div>
    </div>
  );
}

export default ResultDisplay;
