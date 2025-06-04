export interface ClientDetails {
  name: string;
  dob: string;
  tob: string;
  latitude: number;
  longitude: number;
}

export interface ChartHouse {
  houseNumber: number;
  sign: number;
  degree: number;
  planets: {
    name: string;
    sign: number;
    degree: number;
    isRetrograde: boolean;
  }[];
}

export interface ChartResponse {
  houses: ChartHouse[];
  ascendant: {
    sign: number;
    degree: number;
  };
} 