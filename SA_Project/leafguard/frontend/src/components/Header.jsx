import React from "react";

function Header() {
  return (
    <header className="header hero">
      <div className="hero-network" aria-hidden="true">
        <span className="hero-node node-1" />
        <span className="hero-node node-2" />
        <span className="hero-node node-3" />
        <span className="hero-node node-4" />
        <span className="hero-link link-1" />
        <span className="hero-link link-2" />
        <span className="hero-link link-3" />
      </div>

      <div className="hero-content">
        <span className="hero-badge">Research Prototype</span>
        <div className="header-kicker">AI + Biology + Research Lab</div>
        <h1>LeafGuard</h1>
        <p>
          AI-powered Plant Disease Detection for Acacia senegal &amp; Prosopis
          cineraria
        </p>
      </div>
    </header>
  );
}

export default Header;
