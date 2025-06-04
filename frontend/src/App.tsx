import { useState } from "react";
import type { ClientDetails, ChartResponse } from "./types";
import { calculateChart } from "./services/chartService";
import ClientForm from "./components/ClientForm";
import ChartDisplay from "./components/ChartDisplay";

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [chart, setChart] = useState<ChartResponse | null>(null);

  const handleSubmit = async (details: ClientDetails) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await calculateChart(details);
      setChart(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-center text-gray-900 mb-8">
          Vedic Astrology Chart Calculator
        </h1>

        <ClientForm onSubmit={handleSubmit} isLoading={isLoading} />

        {error && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {chart && <ChartDisplay chart={chart} />}
      </div>
    </div>
  );
}

export default App;
