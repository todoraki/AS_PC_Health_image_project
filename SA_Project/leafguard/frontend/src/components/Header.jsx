import React from "react";
import bitsLogo from "../assets/bits_logo.png";

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
        <span className="hero-badge" aria-label="Software Innovations Lab BITS AI and Biology">
          <img className="lab-logo" src={bitsLogo} alt="BITS logo" />
          <span className="lab-copy">
            <span className="lab-title">Software Innovations Lab BITS</span>
            <span className="lab-subtitle">AI + Biology</span>
          </span>
        </span>
        <h1>
          LeafGuard: AI-powered Plant Disease Detection for Acacia Senegal and
          Prosopis Cineraria
        </h1>
      </div>
    </header>
  );
}

export default Header;
