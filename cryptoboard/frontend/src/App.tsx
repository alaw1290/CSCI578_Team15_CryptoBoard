import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Currencies from "./pages/Currencies";
import Predictions from "./pages/Predictions";
import Sentiments from "./pages/Sentiments";
import Navbar from "./components/Navbar";
import "./App.css";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Currencies />} />
        <Route path="/predictions" element={<Predictions />} />
        <Route path="/sentiments" element={<Sentiments />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
