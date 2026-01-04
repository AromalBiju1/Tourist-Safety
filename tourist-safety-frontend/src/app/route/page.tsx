'use client';

import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import dynamic from 'next/dynamic';
import {
    Navigation,
    MapPin,
    Search,
    Loader2,
    Shield,
    AlertTriangle,
    Clock,
    Ruler,
    ChevronRight,
} from 'lucide-react';
import { routesApi, safetyApi, type RouteOption, type City } from '@/lib/api';
import { RouteOptionCard } from '@/components/Map/RouteMap';

// Dynamic import for map
const RouteMap = dynamic(
    () => import('@/components/Map/RouteMap').then((mod) => mod.RouteMap),
    {
        ssr: false,
        loading: () => (
            <div className="h-[500px] bg-slate-800/50 rounded-2xl flex items-center justify-center">
                <div className="flex flex-col items-center gap-4">
                    <div className="w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
                    <p className="text-slate-400">Loading map...</p>
                </div>
            </div>
        ),
    }
);

export default function RoutePage() {
    const [origin, setOrigin] = useState<City | null>(null);
    const [destination, setDestination] = useState<City | null>(null);
    const [selectedRouteId, setSelectedRouteId] = useState<string>('');
    const [originSearch, setOriginSearch] = useState('');
    const [destSearch, setDestSearch] = useState('');

    // Fetch cities for autocomplete
    const { data: citiesData } = useQuery({
        queryKey: ['cities-for-route'],
        queryFn: () => safetyApi.getAllCities(),
    });

    // Calculate route mutation
    const routeMutation = useMutation({
        mutationFn: () =>
            routesApi.calculateSafeRoute(
                { lat: origin!.latitude, lng: origin!.longitude },
                { lat: destination!.latitude, lng: destination!.longitude }
            ),
        onSuccess: (data) => {
            if (data.routes.length > 0) {
                setSelectedRouteId(data.safest_route_id);
            }
        },
    });

    const handleCalculateRoute = () => {
        if (origin && destination) {
            routeMutation.mutate();
        }
    };

    const filteredOriginCities = citiesData?.cities.filter(
        (city) =>
            city.name.toLowerCase().includes(originSearch.toLowerCase()) ||
            city.state.toLowerCase().includes(originSearch.toLowerCase())
    );

    const filteredDestCities = citiesData?.cities.filter(
        (city) =>
            city.name.toLowerCase().includes(destSearch.toLowerCase()) ||
            city.state.toLowerCase().includes(destSearch.toLowerCase())
    );

    const selectedRoute = routeMutation.data?.routes.find(
        (r) => r.route_id === selectedRouteId
    );

    return (
        <div className="min-h-screen bg-pattern">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold mb-2">
                        Plan Your <span className="gradient-text">Safe Route</span>
                    </h1>
                    <p className="text-slate-400">
                        Get routes optimized for safety, with detailed zone breakdowns and recommendations
                    </p>
                </div>

                <div className="grid lg:grid-cols-3 gap-8">
                    {/* Left Panel - Input */}
                    <div className="space-y-6">
                        {/* Origin Selection */}
                        <div className="p-6 rounded-2xl bg-slate-800/50 border border-slate-700/50">
                            <label className="flex items-center gap-2 text-sm font-medium text-slate-300 mb-3">
                                <div className="w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center">
                                    <MapPin className="w-3 h-3 text-white" />
                                </div>
                                Starting Point
                            </label>

                            {origin ? (
                                <div className="flex items-center justify-between p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30">
                                    <div>
                                        <div className="font-medium text-white">{origin.name}</div>
                                        <div className="text-sm text-slate-400">{origin.state}</div>
                                    </div>
                                    <button
                                        onClick={() => setOrigin(null)}
                                        className="text-slate-400 hover:text-white"
                                    >
                                        Change
                                    </button>
                                </div>
                            ) : (
                                <div className="relative">
                                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                                    <input
                                        type="text"
                                        placeholder="Search city..."
                                        value={originSearch}
                                        onChange={(e) => setOriginSearch(e.target.value)}
                                        className="w-full pl-10 pr-4 py-2 bg-slate-900/50 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/50"
                                    />
                                    {originSearch && filteredOriginCities && (
                                        <div className="absolute z-10 w-full mt-2 max-h-48 overflow-y-auto bg-slate-800 border border-slate-700 rounded-lg shadow-xl">
                                            {filteredOriginCities.slice(0, 5).map((city) => (
                                                <button
                                                    key={city.id}
                                                    onClick={() => {
                                                        setOrigin(city);
                                                        setOriginSearch('');
                                                    }}
                                                    className="w-full px-4 py-2 text-left hover:bg-slate-700 transition-colors"
                                                >
                                                    <div className="font-medium text-white">{city.name}</div>
                                                    <div className="text-sm text-slate-400">{city.state}</div>
                                                </button>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>

                        {/* Arrow */}
                        <div className="flex justify-center">
                            <div className="w-10 h-10 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center">
                                <ChevronRight className="w-5 h-5 text-slate-400 rotate-90" />
                            </div>
                        </div>

                        {/* Destination Selection */}
                        <div className="p-6 rounded-2xl bg-slate-800/50 border border-slate-700/50">
                            <label className="flex items-center gap-2 text-sm font-medium text-slate-300 mb-3">
                                <div className="w-6 h-6 rounded-full bg-red-500 flex items-center justify-center">
                                    <MapPin className="w-3 h-3 text-white" />
                                </div>
                                Destination
                            </label>

                            {destination ? (
                                <div className="flex items-center justify-between p-3 rounded-lg bg-red-500/10 border border-red-500/30">
                                    <div>
                                        <div className="font-medium text-white">{destination.name}</div>
                                        <div className="text-sm text-slate-400">{destination.state}</div>
                                    </div>
                                    <button
                                        onClick={() => setDestination(null)}
                                        className="text-slate-400 hover:text-white"
                                    >
                                        Change
                                    </button>
                                </div>
                            ) : (
                                <div className="relative">
                                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                                    <input
                                        type="text"
                                        placeholder="Search city..."
                                        value={destSearch}
                                        onChange={(e) => setDestSearch(e.target.value)}
                                        className="w-full pl-10 pr-4 py-2 bg-slate-900/50 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/50"
                                    />
                                    {destSearch && filteredDestCities && (
                                        <div className="absolute z-10 w-full mt-2 max-h-48 overflow-y-auto bg-slate-800 border border-slate-700 rounded-lg shadow-xl">
                                            {filteredDestCities.slice(0, 5).map((city) => (
                                                <button
                                                    key={city.id}
                                                    onClick={() => {
                                                        setDestination(city);
                                                        setDestSearch('');
                                                    }}
                                                    className="w-full px-4 py-2 text-left hover:bg-slate-700 transition-colors"
                                                >
                                                    <div className="font-medium text-white">{city.name}</div>
                                                    <div className="text-sm text-slate-400">{city.state}</div>
                                                </button>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>

                        {/* Calculate Button */}
                        <button
                            onClick={handleCalculateRoute}
                            disabled={!origin || !destination || routeMutation.isPending}
                            className="w-full flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-xl text-white font-semibold shadow-lg shadow-emerald-500/25 hover:shadow-emerald-500/40 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                        >
                            {routeMutation.isPending ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <Navigation className="w-5 h-5" />
                            )}
                            {routeMutation.isPending ? 'Calculating...' : 'Find Safe Route'}
                        </button>

                        {/* Route Options */}
                        {routeMutation.data && (
                            <div className="space-y-4">
                                <h3 className="font-semibold text-white">
                                    Route Options ({routeMutation.data.routes.length})
                                </h3>
                                {routeMutation.data.routes.map((route) => (
                                    <RouteOptionCard
                                        key={route.route_id}
                                        route={route}
                                        isSelected={route.route_id === selectedRouteId}
                                        isSafest={route.route_id === routeMutation.data.safest_route_id}
                                        isFastest={route.route_id === routeMutation.data.fastest_route_id}
                                        onClick={() => setSelectedRouteId(route.route_id)}
                                    />
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Right Panel - Map & Details */}
                    <div className="lg:col-span-2 space-y-6">
                        {routeMutation.data && origin && destination ? (
                            <>
                                <RouteMap
                                    routes={routeMutation.data.routes}
                                    origin={{ lat: origin.latitude, lng: origin.longitude }}
                                    destination={{ lat: destination.latitude, lng: destination.longitude }}
                                    selectedRouteId={selectedRouteId}
                                    onRouteSelect={setSelectedRouteId}
                                    height="500px"
                                />

                                {/* Selected Route Details */}
                                {selectedRoute && (
                                    <motion.div
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        className="p-6 rounded-2xl bg-slate-800/50 border border-slate-700/50"
                                    >
                                        <h3 className="font-semibold text-white mb-4">Route Details</h3>

                                        <div className="grid sm:grid-cols-3 gap-4 mb-6">
                                            <div className="p-4 rounded-xl bg-slate-900/50">
                                                <div className="flex items-center gap-2 text-slate-400 mb-1">
                                                    <Shield className="w-4 h-4" />
                                                    <span className="text-sm">Safety Score</span>
                                                </div>
                                                <div className="text-2xl font-bold text-emerald-400">
                                                    {selectedRoute.safety_score}%
                                                </div>
                                            </div>
                                            <div className="p-4 rounded-xl bg-slate-900/50">
                                                <div className="flex items-center gap-2 text-slate-400 mb-1">
                                                    <Ruler className="w-4 h-4" />
                                                    <span className="text-sm">Distance</span>
                                                </div>
                                                <div className="text-2xl font-bold text-white">
                                                    {selectedRoute.distance_km} km
                                                </div>
                                            </div>
                                            <div className="p-4 rounded-xl bg-slate-900/50">
                                                <div className="flex items-center gap-2 text-slate-400 mb-1">
                                                    <Clock className="w-4 h-4" />
                                                    <span className="text-sm">Duration</span>
                                                </div>
                                                <div className="text-2xl font-bold text-white">
                                                    {Math.round(selectedRoute.duration_min)} min
                                                </div>
                                            </div>
                                        </div>

                                        {/* Recommendations */}
                                        <div>
                                            <h4 className="font-medium text-white mb-3">Safety Recommendations</h4>
                                            <div className="space-y-2">
                                                {selectedRoute.recommendations.map((rec, idx) => (
                                                    <div
                                                        key={idx}
                                                        className="flex items-start gap-2 text-sm text-slate-300"
                                                    >
                                                        <span>{rec}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    </motion.div>
                                )}
                            </>
                        ) : (
                            <div className="h-[500px] bg-slate-800/50 rounded-2xl flex items-center justify-center border border-slate-700/50">
                                <div className="text-center">
                                    <Navigation className="w-16 h-16 text-slate-600 mx-auto mb-4" />
                                    <h3 className="text-lg font-medium text-slate-400 mb-2">
                                        Plan Your Journey
                                    </h3>
                                    <p className="text-slate-500 max-w-sm">
                                        Select a starting point and destination to see safe route options
                                    </p>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
