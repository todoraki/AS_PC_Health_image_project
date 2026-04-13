import React from "react";

function ResultDisplay({ result }) {
  if (!result) return null;

  const { species, health, summary } = result;
  const isHealthy = health.status === "Healthy";

  return (
    <div className="card result-card">
      <h2>Analysis Result</h2>

      <div className="result-grid">
        {/* Species box */}
        <div className="result-box">
          <div className="label">Species</div>
          <div className="value">{species.name}</div>
          <div className="confidence">
            Confidence: {(species.confidence * 100).toFixed(1)}%
          </div>
          <div className="confidence-bar-wrap">
            <div
              className="confidence-bar"
              style={{ width: `${species.confidence * 100}%` }}
            />
          </div>
        </div>

        {/* Health box */}
        <div
          className={`result-box ${
            isHealthy ? "health-healthy" : "health-unhealthy"
          }`}
        >
          <div className="label">Health Status</div>
          <div className="value">{health.status}</div>
          <div className="confidence">
            Confidence: {(health.confidence * 100).toFixed(1)}%
          </div>
          <div className="confidence-bar-wrap">
            <div
              className="confidence-bar"
              style={{
                width: `${health.confidence * 100}%`,
                background: isHealthy ? "#40916c" : "#e63946",
              }}
            />
          </div>
        </div>
      </div>

      <div className="result-summary">{summary}</div>
    </div>
  );
}

export default ResultDisplay;
