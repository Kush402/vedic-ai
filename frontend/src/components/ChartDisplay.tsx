import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { generateReport } from '../services/chartService';

interface ChartData {
  name: string;
  dob: string;
  tob: string;
  location: string;
  ascendant: string;
  nakshatra: {
    nakshatra: string;
    pada: number;
  };
  houses: Array<{
    sign: string;
    planets: string;
  }>;
  dasha: {
    current_maha_dasha: string;
    years_remaining: number;
  };
}

const ChartDisplay: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [report, setReport] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const chartData = location.state?.chartData as ChartData;

  if (!chartData) {
    return (
      <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-lg">
        <p className="text-red-600">No chart data available. Please go back and generate a chart.</p>
        <button
          onClick={() => navigate('/')}
          className="mt-4 w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700"
        >
          Go Back
        </button>
      </div>
    );
  }

  const generateAstrologyReport = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await generateReport(chartData);
      setReport(response.overall_analysis);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error generating report');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto mt-8 p-6">
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">Chart Details</h2>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-gray-600">Name</p>
            <p className="font-semibold">{chartData.name}</p>
          </div>
          <div>
            <p className="text-gray-600">Ascendant</p>
            <p className="font-semibold">{chartData.ascendant}</p>
          </div>
          <div>
            <p className="text-gray-600">Nakshatra</p>
            <p className="font-semibold">{chartData.nakshatra.nakshatra} (Pada {chartData.nakshatra.pada})</p>
          </div>
          <div>
            <p className="text-gray-600">Current Dasha</p>
            <p className="font-semibold">{chartData.dasha.current_maha_dasha} ({chartData.dasha.years_remaining} years remaining)</p>
          </div>
        </div>

        <div className="mt-6">
          <h3 className="text-xl font-semibold mb-3 text-gray-800">House Placements</h3>
          <div className="grid grid-cols-3 gap-4">
            {chartData.houses.map((house, index) => (
              <div key={index} className="bg-gray-50 p-3 rounded">
                <p className="text-gray-600">House {index + 1}</p>
                <p className="font-semibold">{house.sign}</p>
                {house.planets && <p className="text-sm text-gray-500">{house.planets}</p>}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">Astrological Report</h2>
        <button
          onClick={generateAstrologyReport}
          disabled={loading}
          className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white 
            ${loading 
              ? 'bg-indigo-400 cursor-not-allowed' 
              : 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
            }`}
        >
          {loading ? 'Generating Report...' : 'Generate Report'}
        </button>

        {error && (
          <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}

        {report && (
          <div className="mt-6 prose prose-indigo max-w-none">
            {report.split('\n').map((paragraph, index) => (
              <p key={index} className="mb-4">{paragraph}</p>
            ))}
          </div>
        )}
      </div>

      <button
        onClick={() => navigate('/')}
        className="mt-6 w-full py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
      >
        Generate New Chart
      </button>
    </div>
  );
};

export default ChartDisplay; 