import React from "react";
import Home from "./pages/Home.jsx";
import Header from "./components/Header.jsx";
import "./App.css";

function App() {
  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <Home />
      </main>
      <footer className="footer">
        <p>LeafGuard &copy; 2026 &mdash; Vighnesh PM (2025H1120159)</p>
      </footer>
    </div>
  );
}

export default App;
