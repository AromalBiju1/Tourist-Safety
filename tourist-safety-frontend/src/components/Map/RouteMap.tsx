'use client';

import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polyline, CircleMarker, Popup, useMap } from 'react-leaflet';
import { motion } from 'framer-motion';
import { Navigation, Clock, Ruler, Shield, AlertTriangle } from 'lucide-react';
import 'leaflet/dist/leaflet.css';
import type { RouteOption } from '@/lib/api';
import { SAFETY_COLORS } from '@/lib/constants';

interface RouteMapProps {
    routes: RouteOption[];
    origin: { lat: number; lng: number };
    destination: { lat: number; lng: number };
    selectedRouteId: string;
    onRouteSelect: (routeId: string) => void;
    height?: string;
}

function MapBounds({ routes, origin, destination }: { routes: RouteOption[]; origin: { lat: number; lng: number }; destination: { lat: number; lng: number } }) {
    const map = useMap();

    useEffect(() => {
        const allCoords: [number, number][] = [
            [origin.lat, origin.lng],
            [destination.lat, destination.lng],
        ];

        routes.forEach((route) => {
            route.geometry.coordinates.forEach(([lng, lat]) => {
                allCoords.push([lat, lng]);
            });
        });

        if (allCoords.length > 0) {
            map.fitBounds(allCoords, { padding: [50, 50] });
        }
    }, [map, routes, origin, destination]);

    return null;
}

export function RouteMap({
    routes,
    origin,
    destination,
    selectedRouteId,
    onRouteSelect,
    height = '500px',
}: RouteMapProps) {
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
                    <p className="text-slate-400">Loading route map...</p>
                </div>
            </div>
        );
    }

    const getRouteColor = (route: RouteOption, isSelected: boolean) => {
        if (!isSelected) return '#64748b'; // slate-500 for non-selected

        if (route.safety_score >= 70) return SAFETY_COLORS.green;
        if (route.safety_score >= 40) return SAFETY_COLORS.orange;
        return SAFETY_COLORS.red;
    };

    return (
        <div className="relative rounded-2xl overflow-hidden border border-slate-700/50 shadow-2xl" style={{ height }}>
            <MapContainer
                center={[origin.lat, origin.lng]}
                zoom={10}
                className="w-full h-full"
                style={{ background: '#0f172a' }}
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                    url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                />
                <MapBounds routes={routes} origin={origin} destination={destination} />

                {/* Draw routes */}
                {routes.map((route) => {
                    const isSelected = route.route_id === selectedRouteId;
                    const positions: [number, number][] = route.geometry.coordinates.map(
                        ([lng, lat]) => [lat, lng]
                    );

                    return (
                        <Polyline
                            key={route.route_id}
                            positions={positions}
                            color={getRouteColor(route, isSelected)}
                            weight={isSelected ? 6 : 4}
                            opacity={isSelected ? 1 : 0.5}
                            eventHandlers={{
                                click: () => onRouteSelect(route.route_id),
                            }}
                        />
                    );
                })}

                {/* Origin marker */}
                <CircleMarker
                    center={[origin.lat, origin.lng]}
                    radius={12}
                    fillColor="#22c55e"
                    color="#fff"
                    weight={3}
                    opacity={1}
                    fillOpacity={1}
                >
                    <Popup>
                        <div className="font-medium">Start Point</div>
                    </Popup>
                </CircleMarker>

                {/* Destination marker */}
                <CircleMarker
                    center={[destination.lat, destination.lng]}
                    radius={12}
                    fillColor="#ef4444"
                    color="#fff"
                    weight={3}
                    opacity={1}
                    fillOpacity={1}
                >
                    <Popup>
                        <div className="font-medium">Destination</div>
                    </Popup>
                </CircleMarker>
            </MapContainer>
        </div>
    );
}

// Route option card
export function RouteOptionCard({
    route,
    isSelected,
    isSafest,
    isFastest,
    onClick,
}: {
    route: RouteOption;
    isSelected: boolean;
    isSafest: boolean;
    isFastest: boolean;
    onClick: () => void;
}) {
    const getClassificationConfig = (classification: string) => {
        switch (classification) {
            case 'safe':
                return { bg: 'bg-emerald-500/20', border: 'border-emerald-500/50', text: 'text-emerald-400', icon: Shield };
            case 'moderate':
                return { bg: 'bg-orange-500/20', border: 'border-orange-500/50', text: 'text-orange-400', icon: AlertTriangle };
            default:
                return { bg: 'bg-red-500/20', border: 'border-red-500/50', text: 'text-red-400', icon: AlertTriangle };
        }
    };

    const config = getClassificationConfig(route.classification);
    const Icon = config.icon;

    return (
        <motion.button
            onClick={onClick}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`w-full p-4 rounded-xl text-left transition-all ${isSelected
                    ? 'bg-slate-700/50 border-2 border-emerald-500/50 shadow-lg shadow-emerald-500/10'
                    : 'bg-slate-800/50 border border-slate-700/50 hover:border-slate-600/50'
                }`}
        >
            {/* Badges */}
            <div className="flex items-center gap-2 mb-3">
                {isSafest && (
                    <span className="px-2 py-0.5 bg-emerald-500/20 border border-emerald-500/50 rounded-full text-xs font-medium text-emerald-400">
                        🛡️ Safest
                    </span>
                )}
                {isFastest && (
                    <span className="px-2 py-0.5 bg-cyan-500/20 border border-cyan-500/50 rounded-full text-xs font-medium text-cyan-400">
                        ⚡ Fastest
                    </span>
                )}
            </div>

            {/* Safety Score */}
            <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                    <Icon className={`w-5 h-5 ${config.text}`} />
                    <span className={`font-semibold ${config.text}`}>
                        Safety Score: {route.safety_score}%
                    </span>
                </div>
                <div className={`px-2 py-1 rounded-lg ${config.bg} border ${config.border}`}>
                    <span className={`text-xs font-medium ${config.text} capitalize`}>
                        {route.classification}
                    </span>
                </div>
            </div>

            {/* Stats */}
            <div className="flex items-center gap-4 text-sm text-slate-400 mb-3">
                <div className="flex items-center gap-1">
                    <Ruler className="w-4 h-4" />
                    <span>{route.distance_km} km</span>
                </div>
                <div className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    <span>{Math.round(route.duration_min)} min</span>
                </div>
            </div>

            {/* Zone Breakdown Bar */}
            <div className="mb-3">
                <div className="flex h-2 rounded-full overflow-hidden bg-slate-700">
                    <div
                        className="bg-emerald-500"
                        style={{ width: `${route.zone_breakdown.green_percentage}%` }}
                    />
                    <div
                        className="bg-orange-500"
                        style={{ width: `${route.zone_breakdown.orange_percentage}%` }}
                    />
                    <div
                        className="bg-red-500"
                        style={{ width: `${route.zone_breakdown.red_percentage}%` }}
                    />
                </div>
                <div className="flex justify-between text-xs text-slate-500 mt-1">
                    <span>🟢 {route.zone_breakdown.green_percentage}%</span>
                    <span>🟠 {route.zone_breakdown.orange_percentage}%</span>
                    <span>🔴 {route.zone_breakdown.red_percentage}%</span>
                </div>
            </div>

            {/* Recommendations (show first one) */}
            {route.recommendations.length > 0 && (
                <p className="text-xs text-slate-400 line-clamp-1">
                    {route.recommendations[0]}
                </p>
            )}
        </motion.button>
    );
}
