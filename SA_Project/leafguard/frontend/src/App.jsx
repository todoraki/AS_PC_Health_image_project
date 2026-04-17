import React from "react";
import Home from "./pages/Home.jsx";
import Header from "./components/Header.jsx";
import "./App.css";

function App() {
  return (
    <div className="app">
      <div className="bg-layer dna-pattern" aria-hidden="true" />
      <div className="bg-layer molecule-pattern" aria-hidden="true" />
      <div className="bg-layer neural-network" aria-hidden="true" />
      <Header />
      <main className="main-content">
        <Home />
      </main>
      <footer className="footer">
        <p>LeafGuard &copy; 2026 | Research Interface for Plant Health Analytics</p>
      </footer>
    </div>
  );
}

export default App;
