import axios from 'axios';

// Use VITE_API_URL for backend connection (set in Vercel and .env)
const API_BASE_URL = import.meta.env.VITE_API_URL;

interface ChartRequest {
  name: string;
  dob: string;
  tob: string;
  location: string;
}

interface ChartResponse {
  name: string;
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

interface ReportResponse {
  overall_analysis: string;
  chart_data: ChartResponse;
}

export const generateChart = async (data: ChartRequest): Promise<ChartResponse> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/v1/charts`, data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Error generating chart');
    }
    throw error;
  }
};

export const generateReport = async (data: ChartRequest): Promise<ReportResponse> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/v1/generate-report`, data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Error generating report');
    }
    throw error;
  }
}; 