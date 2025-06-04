import type { ChartResponse } from "../types";
import { ZODIAC_SIGNS } from "../constants";

interface ChartDisplayProps {
  chart: ChartResponse;
}

export default function ChartDisplay({ chart }: ChartDisplayProps) {
  const formatDegree = (degree: number) => {
    return `${Math.floor(degree)}°${Math.floor((degree % 1) * 60)}'`;
  };

  const getSignName = (sign: number) => {
    return ZODIAC_SIGNS[sign - 1];
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-6">Birth Chart</h2>
      
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-2">Ascendant</h3>
        <p className="text-gray-700">
          {getSignName(chart.ascendant.sign)} {formatDegree(chart.ascendant.degree)}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {chart.houses.map((house) => (
          <div key={house.houseNumber} className="border rounded-lg p-4">
            <h4 className="font-semibold mb-2">House {house.houseNumber}</h4>
            <p className="text-gray-700 mb-2">
              {getSignName(house.sign)} {formatDegree(house.degree)}
            </p>
            
            {house.planets.length > 0 && (
              <div className="mt-2">
                <h5 className="text-sm font-medium text-gray-600 mb-1">Planets:</h5>
                <ul className="space-y-1">
                  {house.planets.map((planet) => (
                    <li key={planet.name} className="text-sm text-gray-700">
                      {planet.name} in {getSignName(planet.sign)} {formatDegree(planet.degree)}
                      {planet.isRetrograde && " (R)"}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
} 