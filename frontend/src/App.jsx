import { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    name: '',
    date: '',
    time: '',
    city: '',
    country: ''
  });
  const [chart, setChart] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      // Format the date and time
      const [year, month, day] = formData.date.split('-');
      const [hours, minutes] = formData.time.split(':');
      
      const requestData = {
        name: formData.name,
        dob: `${year}-${month}-${day}`,
        tob: `${hours}:${minutes}`,
        location: `${formData.city}, ${formData.country}`
      };

      console.log('Sending data:', requestData); // Debug log
      
      const response = await fetch('http://localhost:8001/api/v1/charts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate chart');
      }
      
      const data = await response.json();
      setChart(data);
    } catch (err) {
      console.error('Error:', err); // Debug log
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateReport = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Format the date and time from the original form data
      const [year, month, day] = formData.date.split('-');
      const [hours, minutes] = formData.time.split(':');
      
      const requestData = {
        name: formData.name,
        dob: `${year}-${month}-${day}`,
        tob: `${hours}:${minutes}`,
        location: `${formData.city}, ${formData.country}`
      };

      console.log('Sending report request:', requestData); // Debug log
      
      const response = await fetch('http://localhost:8001/api/v1/generate-report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate report');
      }
      
      const data = await response.json();
      setReport(data);
    } catch (err) {
      console.error('Error:', err); // Debug log
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      date: '',
      time: '',
      city: '',
      country: ''
    });
    setChart(null);
    setReport(null);
    setError(null);
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <h2>Generating your chart...</h2>
          <p>Please wait while we calculate your astrological chart.</p>
        </div>
      </div>
    );
  }

  if (chart) {
    return (
      <div className="container">
        <div className="chart-container">
          <div className="chart-header">
            <h2>{chart.name}'s Astrological Chart</h2>
            <button onClick={resetForm}>Generate New Chart</button>
          </div>
          
          <div className="chart-details">
            <h3>Chart Details</h3>
            <div className="detail-grid">
              <div className="detail-item">
                <h4>Ascendant</h4>
                <p>{chart.ascendant}</p>
              </div>
              <div className="detail-item">
                <h4>Moon Nakshatra</h4>
                <p>{chart.nakshatra.nakshatra} (Pada {chart.nakshatra.pada})</p>
              </div>
              <div className="detail-item">
                <h4>Current Dasha</h4>
                <p>{chart.dasha.current_maha_dasha} ({chart.dasha.years_remaining} years remaining)</p>
              </div>
            </div>
          </div>

          {!report && (
            <button onClick={generateReport} className="generate-report">
              Generate AI Report
            </button>
          )}

          {report && (
            <div className="report-container">
              <div className="report-section">
                <div className="report-content">
                  {report.overall_analysis.split('\n').map((paragraph, index) => {
                    // Clean up the text by removing all ** and * markers
                    const cleanText = paragraph
                      .replace(/\*\*/g, '')  // Remove ** markers
                      .replace(/^\*\s*/, '')  // Remove * at start of line
                      .replace(/\s*\*\s*/g, ' ')  // Remove * in middle of text
                      .trim();
                    
                    // Handle section headers (lines that were previously marked with **)
                    if (paragraph.trim().startsWith('**')) {
                      return <h3 key={index} className="section-header">{cleanText}</h3>;
                    }
                    // Handle bullet points (lines starting with *)
                    else if (paragraph.trim().startsWith('*')) {
                      return (
                        <ul key={index} className="bullet-list">
                          <li>{cleanText}</li>
                        </ul>
                      );
                    }
                    // Handle regular paragraphs
                    else if (cleanText) {
                      return <p key={index} className="report-paragraph">{cleanText}</p>;
                    }
                    return null;
                  })}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="header">
        <h1>Vedic Astrology Chart Generator</h1>
        <p>Enter your birth details to generate your astrological chart</p>
      </div>

      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Full Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
              placeholder="Enter your full name"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="date">Date of Birth</label>
              <input
                type="date"
                id="date"
                name="date"
                value={formData.date}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="time">Time of Birth</label>
              <input
                type="time"
                id="time"
                name="time"
                value={formData.time}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="city">City</label>
              <input
                type="text"
                id="city"
                name="city"
                value={formData.city}
                onChange={handleInputChange}
                required
                placeholder="Enter city of birth"
              />
            </div>

            <div className="form-group">
              <label htmlFor="country">Country</label>
              <input
                type="text"
                id="country"
                name="country"
                value={formData.country}
                onChange={handleInputChange}
                required
                placeholder="Enter country of birth"
              />
            </div>
          </div>

          {error && <div className="error">{error}</div>}

          <button type="submit">Generate Chart</button>
        </form>
      </div>
    </div>
  );
}

export default App; 