export const SAFETY_COLORS = {
    green: '#22c55e',
    orange: '#f97316',
    red: '#ef4444',
} as const;

export const SAFETY_DESCRIPTIONS = {
    green: 'Safe - Low crime rate, recommended for tourists',
    orange: 'Moderate Risk - Exercise normal precautions',
    red: 'High Risk - Exercise increased caution',
} as const;

export const INDIA_CENTER = {
    lat: 20.5937,
    lng: 78.9629,
} as const;

export const DEFAULT_ZOOM = 5;

export const EMERGENCY_NUMBERS = {
    police: '100',
    ambulance: '102',
    fire: '101',
    women_helpline: '1091',
    tourist_helpline: '1363',
    universal: '112',
} as const;

export const CATEGORIES = [
    'monument',
    'temple',
    'nature',
    'museum',
    'entertainment',
    'beach',
    'fort',
    'palace',
] as const;
