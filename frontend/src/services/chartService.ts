import type { ClientDetails, ChartResponse } from "../types";
import { API_BASE_URL } from "../constants";

export async function calculateChart(details: ClientDetails): Promise<ChartResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/d1`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(details),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to calculate chart");
    }

    return await response.json();
  } catch (error) {
    console.error("Error calculating chart:", error);
    throw error;
  }
} 