import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BirthDetailsForm from './components/BirthDetailsForm';
import ChartDisplay from './components/ChartDisplay';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Vedic Astrology Report Generator</h1>
        </header>

        <main className="App-main">
          <Routes>
            <Route path="/" element={<BirthDetailsForm />} />
            <Route path="/chart" element={<ChartDisplay />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 