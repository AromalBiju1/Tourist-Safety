'use client';

import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import { motion } from 'framer-motion';
import { Shield, AlertTriangle, Users, MapPin } from 'lucide-react';
import 'leaflet/dist/leaflet.css';
import type { City } from '@/lib/api';
import { SAFETY_COLORS, INDIA_CENTER, DEFAULT_ZOOM } from '@/lib/constants';

interface MapViewProps {
    cities: City[];
    onCitySelect?: (city: City) => void;
    selectedCity?: City | null;
    height?: string;
}

// Component to handle map view updates
function MapController({ center, zoom }: { center: [number, number]; zoom: number }) {
    const map = useMap();

    useEffect(() => {
        map.setView(center, zoom, { animate: true });
    }, [map, center, zoom]);

    return null;
}

export function MapView({ cities, onCitySelect, selectedCity, height = '600px' }: MapViewProps) {
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    if (!mounted) {
        return (
            <div
                className="bg-slate-800/50 rounded-2xl flex items-center justify-center"
                style={{ height }}
            >
                <div className="flex flex-col items-center gap-4">
                    <div className="w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
                    <p className="text-slate-400">Loading map...</p>
                </div>
            </div>
        );
    }

    const center: [number, number] = selectedCity
        ? [selectedCity.latitude, selectedCity.longitude]
        : [INDIA_CENTER.lat, INDIA_CENTER.lng];

    const zoom = selectedCity ? 10 : DEFAULT_ZOOM;

    return (
        <div className="relative rounded-2xl overflow-hidden border border-slate-700/50 shadow-2xl" style={{ height }}>
            {/* Map Legend */}
            <div className="absolute top-4 right-4 z-[1000] bg-slate-900/90 backdrop-blur-md rounded-xl p-4 border border-slate-700/50">
                <h4 className="text-sm font-semibold text-white mb-3">Safety Zones</h4>
                <div className="space-y-2">
                    <div className="flex items-center gap-2">
                        <div className="w-4 h-4 rounded-full bg-emerald-500" />
                        <span className="text-xs text-slate-300">Safe</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-4 h-4 rounded-full bg-orange-500" />
                        <span className="text-xs text-slate-300">Moderate</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-4 h-4 rounded-full bg-red-500" />
                        <span className="text-xs text-slate-300">High Risk</span>
                    </div>
                </div>
            </div>

            <MapContainer
                center={center}
                zoom={zoom}
                className="w-full h-full"
                style={{ background: '#0f172a' }}
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                    url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                />
                <MapController center={center} zoom={zoom} />

                {cities.map((city) => (
                    <CircleMarker
                        key={city.id}
                        center={[city.latitude, city.longitude]}
                        radius={selectedCity?.id === city.id ? 15 : 10}
                        fillColor={SAFETY_COLORS[city.safety_zone]}
                        color={selectedCity?.id === city.id ? '#fff' : SAFETY_COLORS[city.safety_zone]}
                        weight={selectedCity?.id === city.id ? 3 : 2}
                        opacity={1}
                        fillOpacity={0.7}
                        eventHandlers={{
                            click: () => onCitySelect?.(city),
                        }}
                    >
                        <Popup>
                            <CityPopup city={city} />
                        </Popup>
                    </CircleMarker>
                ))}
            </MapContainer>
        </div>
    );
}

function CityPopup({ city }: { city: City }) {
    const zoneConfig = {
        green: { icon: Shield, text: 'Safe Zone', bg: 'bg-emerald-500/20', border: 'border-emerald-500/50', textColor: 'text-emerald-400' },
        orange: { icon: AlertTriangle, text: 'Moderate Risk', bg: 'bg-orange-500/20', border: 'border-orange-500/50', textColor: 'text-orange-400' },
        red: { icon: AlertTriangle, text: 'High Risk', bg: 'bg-red-500/20', border: 'border-red-500/50', textColor: 'text-red-400' },
    };

    const config = zoneConfig[city.safety_zone];
    const Icon = config.icon;

    return (
        <div className="min-w-[200px] p-1">
            <div className="flex items-center gap-2 mb-2">
                <MapPin className="w-4 h-4 text-slate-600" />
                <h3 className="font-bold text-slate-900">{city.name}</h3>
            </div>
            <p className="text-sm text-slate-600 mb-2">{city.state}</p>

            <div className={`flex items-center gap-2 px-2 py-1 rounded-lg ${config.bg} border ${config.border}`}>
                <Icon className={`w-4 h-4 ${config.textColor}`} />
                <span className={`text-sm font-medium ${config.textColor}`}>{config.text}</span>
            </div>

            <div className="mt-2 flex items-center gap-4 text-xs text-slate-500">
                <div className="flex items-center gap-1">
                    <Users className="w-3 h-3" />
                    <span>{(city.population / 1000000).toFixed(1)}M</span>
                </div>
                <div>
                    Crime Index: <span className="font-medium">{city.crime_index}</span>
                </div>
            </div>
        </div>
    );
}

// City card for sidebar
export function CityCard({ city, isSelected, onClick }: { city: City; isSelected?: boolean; onClick?: () => void }) {
    const zoneConfig = {
        green: { bg: 'bg-emerald-500/10', border: 'border-emerald-500/30', text: 'text-emerald-400', label: 'Safe' },
        orange: { bg: 'bg-orange-500/10', border: 'border-orange-500/30', text: 'text-orange-400', label: 'Moderate' },
        red: { bg: 'bg-red-500/10', border: 'border-red-500/30', text: 'text-red-400', label: 'High Risk' },
    };

    const config = zoneConfig[city.safety_zone];

    return (
        <motion.button
            onClick={onClick}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`w-full p-4 rounded-xl text-left transition-all ${isSelected
                    ? 'bg-slate-700/50 border-2 border-emerald-500/50'
                    : 'bg-slate-800/50 border border-slate-700/50 hover:border-slate-600/50'
                }`}
        >
            <div className="flex items-start justify-between">
                <div>
                    <h4 className="font-semibold text-white">{city.name}</h4>
                    <p className="text-sm text-slate-400">{city.state}</p>
                </div>
                <div className={`px-2 py-1 rounded-lg ${config.bg} border ${config.border}`}>
                    <span className={`text-xs font-medium ${config.text}`}>{config.label}</span>
                </div>
            </div>
            <div className="mt-2 flex items-center gap-4 text-xs text-slate-500">
                <span>Crime Index: {city.crime_index}</span>
                <span>{(city.population / 1000000).toFixed(1)}M people</span>
            </div>
        </motion.button>
    );
}
