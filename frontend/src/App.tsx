import React, { useState } from 'react';
import ReportGenerator from './components/ReportGenerator';
import './App.css';

function App() {
  const [chartData, setChartData] = useState({
    name: '',
    dob: '',
    tob: '',
    latitude: 0,
    longitude: 0
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setChartData(prev => ({
      ...prev,
      [name]: name === 'latitude' || name === 'longitude' ? parseFloat(value) : value
    }));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Vedic Astrology Report Generator</h1>
      </header>

      <main className="App-main">
        <div className="input-form">
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              name="name"
              value={chartData.name}
              onChange={handleInputChange}
              placeholder="Enter your name"
            />
          </div>

          <div className="form-group">
            <label htmlFor="dob">Date of Birth:</label>
            <input
              type="date"
              id="dob"
              name="dob"
              value={chartData.dob}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="tob">Time of Birth:</label>
            <input
              type="time"
              id="tob"
              name="tob"
              value={chartData.tob}
              onChange={handleInputChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="latitude">Latitude:</label>
            <input
              type="number"
              id="latitude"
              name="latitude"
              value={chartData.latitude}
              onChange={handleInputChange}
              step="0.000001"
              placeholder="Enter latitude"
            />
          </div>

          <div className="form-group">
            <label htmlFor="longitude">Longitude:</label>
            <input
              type="number"
              id="longitude"
              name="longitude"
              value={chartData.longitude}
              onChange={handleInputChange}
              step="0.000001"
              placeholder="Enter longitude"
            />
          </div>
        </div>

        <ReportGenerator chartData={chartData} />
      </main>

      <style jsx>{`
        .App {
          text-align: center;
          min-height: 100vh;
          background-color: #f5f5f5;
        }

        .App-header {
          background-color: #282c34;
          padding: 20px;
          color: white;
        }

        .App-main {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
        }

        .input-form {
          background-color: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          margin-bottom: 20px;
        }

        .form-group {
          margin-bottom: 15px;
          text-align: left;
        }

        .form-group label {
          display: block;
          margin-bottom: 5px;
          color: #333;
        }

        .form-group input {
          width: 100%;
          padding: 8px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 16px;
        }

        .form-group input:focus {
          outline: none;
          border-color: #4CAF50;
          box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
        }
      `}</style>
    </div>
  );
}

export default App; 