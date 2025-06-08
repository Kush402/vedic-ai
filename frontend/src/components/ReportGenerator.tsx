import React, { useState } from 'react';
import axios from 'axios';

interface ReportGeneratorProps {
  chartData: {
    name: string;
    dob: string;
    tob: string;
    latitude: number;
    longitude: number;
  };
}

const ReportGenerator: React.FC<ReportGeneratorProps> = ({ chartData }) => {
  const [report, setReport] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const generateReport = async () => {
    try {
      setLoading(true);
      setError('');
      
      const response = await axios.post('http://localhost:8001/api/v1/generate-report', chartData);
      setReport(response.data.report);
    } catch (err) {
      setError('Error generating report. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="report-generator">
      <button 
        onClick={generateReport}
        disabled={loading}
        className="generate-button"
      >
        {loading ? 'Generating Report...' : 'Generate Report'}
      </button>

      {error && <div className="error-message">{error}</div>}

      {report && (
        <div 
          className="report-content"
          dangerouslySetInnerHTML={{ __html: report }}
        />
      )}

      <style jsx>{`
        .report-generator {
          padding: 20px;
          max-width: 800px;
          margin: 0 auto;
        }

        .generate-button {
          background-color: #4CAF50;
          color: white;
          padding: 12px 24px;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 16px;
          transition: background-color 0.3s;
        }

        .generate-button:hover {
          background-color: #45a049;
        }

        .generate-button:disabled {
          background-color: #cccccc;
          cursor: not-allowed;
        }

        .error-message {
          color: #ff0000;
          margin: 10px 0;
          padding: 10px;
          background-color: #ffe6e6;
          border-radius: 4px;
        }

        .report-content {
          margin-top: 20px;
          padding: 20px;
          background-color: #f9f9f9;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .report-content h2 {
          color: #333;
          margin-bottom: 15px;
        }

        .report-content p {
          margin-bottom: 15px;
          line-height: 1.6;
        }

        .report-content ul {
          margin-left: 20px;
          margin-bottom: 15px;
        }

        .report-content li {
          margin-bottom: 8px;
        }

        .report-content strong {
          color: #2c3e50;
        }

        .report-content em {
          color: #34495e;
          font-style: italic;
        }
      `}</style>
    </div>
  );
};

export default ReportGenerator; 