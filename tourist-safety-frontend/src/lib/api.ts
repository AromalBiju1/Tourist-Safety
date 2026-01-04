import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface City {
  id: number;
  name: string;
  state: string;
  latitude: number;
  longitude: number;
  population: number;
  crime_index: number;
  safety_zone: 'green' | 'orange' | 'red';
  safety_color?: string;
  safety_description?: string;
}

export interface SafetyOverview {
  total_cities: number;
  green_count: number;
  orange_count: number;
  red_count: number;
  cities: City[];
}

export interface Attraction {
  id: number;
  name: string;
  city_id: number;
  latitude: number;
  longitude: number;
  category: string;
  description: string;
  rating: number;
  review_count: number;
  image_url: string | null;
  city_name?: string;
  city_state?: string;
  city_safety_zone?: string;
  city_safety_color?: string;
}

export interface RouteOption {
  route_id: string;
  safety_score: number;
  classification: 'safe' | 'moderate' | 'risky';
  distance_km: number;
  duration_min: number;
  geometry: {
    type: string;
    coordinates: [number, number][];
  };
  zone_breakdown: {
    green_percentage: number;
    orange_percentage: number;
    red_percentage: number;
    green_distance_km: number;
    orange_distance_km: number;
    red_distance_km: number;
  };
  recommendations: string[];
}

export interface RouteResponse {
  origin: { lat: number; lng: number };
  destination: { lat: number; lng: number };
  routes: RouteOption[];
  safest_route_id: string;
  fastest_route_id: string;
}

export interface EmergencyContact {
  id: number;
  state: string;
  service_type: string;
  service_name: string;
  phone_number: string;
  alternate_number: string | null;
  description: string;
  available_24x7: string;
}

// API Functions
export const safetyApi = {
  getAllCities: async (zone?: string, state?: string): Promise<SafetyOverview> => {
    const params = new URLSearchParams();
    if (zone) params.append('zone', zone);
    if (state) params.append('state', state);
    const response = await api.get(`/safety/cities?${params}`);
    return response.data;
  },

  getCitySafety: async (cityName: string): Promise<City> => {
    const response = await api.get(`/safety/city/${cityName}`);
    return response.data;
  },

  getGeoJSON: async () => {
    const response = await api.get('/safety/zones/geojson');
    return response.data;
  },

  getRanking: async (limit = 20, order = 'safest') => {
    const response = await api.get(`/safety/ranking?limit=${limit}&order=${order}`);
    return response.data;
  },

  getStatesSummary: async () => {
    const response = await api.get('/safety/states');
    return response.data;
  },
};

export const attractionsApi = {
  search: async (query: string, category?: string, safetyZone?: string) => {
    const params = new URLSearchParams({ q: query });
    if (category) params.append('category', category);
    if (safetyZone) params.append('safety_zone', safetyZone);
    const response = await api.get(`/attractions/search?${params}`);
    return response.data;
  },

  getById: async (id: number): Promise<Attraction> => {
    const response = await api.get(`/attractions/${id}`);
    return response.data;
  },

  getByCity: async (cityName: string) => {
    const response = await api.get(`/attractions/city/${cityName}`);
    return response.data;
  },

  getNearby: async (lat: number, lng: number, radiusKm = 10) => {
    const response = await api.get(`/attractions/nearby?lat=${lat}&lng=${lng}&radius_km=${radiusKm}`);
    return response.data;
  },

  getCategories: async () => {
    const response = await api.get('/attractions/categories/list');
    return response.data;
  },
};

export const routesApi = {
  calculateSafeRoute: async (
    origin: { lat: number; lng: number },
    destination: { lat: number; lng: number }
  ): Promise<RouteResponse> => {
    const response = await api.post('/routes/safe', { origin, destination });
    return response.data;
  },

  checkPointSafety: async (lat: number, lng: number) => {
    const response = await api.get(`/routes/check-point?lat=${lat}&lng=${lng}`);
    return response.data;
  },
};

export const emergencyApi = {
  getNational: async () => {
    const response = await api.get('/emergency/national');
    return response.data;
  },

  getByState: async (stateName: string) => {
    const response = await api.get(`/emergency/state/${stateName}`);
    return response.data;
  },

  getQuickHelp: async () => {
    const response = await api.get('/emergency/quick-help');
    return response.data;
  },

  getSOS: async () => {
    const response = await api.get('/emergency/sos');
    return response.data;
  },
};

export default api;
