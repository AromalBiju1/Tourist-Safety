'use client';

import { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import dynamic from 'next/dynamic';
import { Search, Filter, Shield, AlertTriangle, Map as MapIcon, List, ChevronDown } from 'lucide-react';
import { safetyApi, type City } from '@/lib/api';
import { CityCard } from '@/components/Map/MapView';

// Dynamic import for map (no SSR for Leaflet)
const MapView = dynamic(
    () => import('@/components/Map/MapView').then((mod) => mod.MapView),
    { ssr: false, loading: () => <MapSkeleton /> }
);

function MapSkeleton() {
    return (
        <div className="h-[600px] bg-slate-800/50 rounded-2xl flex items-center justify-center">
            <div className="flex flex-col items-center gap-4">
                <div className="w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
                <p className="text-slate-400">Loading map...</p>
            </div>
        </div>
    );
}

export default function ExplorePage() {
    const [selectedCity, setSelectedCity] = useState<City | null>(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [zoneFilter, setZoneFilter] = useState<string>('all');
    const [viewMode, setViewMode] = useState<'map' | 'list'>('map');

    const { data: safetyData, isLoading, error } = useQuery({
        queryKey: ['safety-cities'],
        queryFn: () => safetyApi.getAllCities(),
    });

    const filteredCities = useMemo(() => {
        if (!safetyData?.cities) return [];

        return safetyData.cities.filter((city) => {
            const matchesSearch =
                city.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                city.state.toLowerCase().includes(searchQuery.toLowerCase());
            const matchesZone = zoneFilter === 'all' || city.safety_zone === zoneFilter;
            return matchesSearch && matchesZone;
        });
    }, [safetyData?.cities, searchQuery, zoneFilter]);

    if (error) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <AlertTriangle className="w-16 h-16 text-red-400 mx-auto mb-4" />
                    <h2 className="text-xl font-semibold mb-2">Failed to load data</h2>
                    <p className="text-slate-400">Please make sure the backend server is running.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-pattern">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold mb-2">
                        Explore <span className="gradient-text">Safety Zones</span>
                    </h1>
                    <p className="text-slate-400">
                        View cities across India classified by safety levels based on crime data
                    </p>
                </div>

                {/* Stats Summary */}
                {safetyData && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"
                    >
                        <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
                            <div className="text-2xl font-bold text-white">{safetyData.total_cities}</div>
                            <div className="text-sm text-slate-400">Total Cities</div>
                        </div>
                        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30">
                            <div className="flex items-center gap-2">
                                <Shield className="w-5 h-5 text-emerald-400" />
                                <span className="text-2xl font-bold text-emerald-400">{safetyData.green_count}</span>
                            </div>
                            <div className="text-sm text-emerald-400/70">Safe Cities</div>
                        </div>
                        <div className="p-4 rounded-xl bg-orange-500/10 border border-orange-500/30">
                            <div className="flex items-center gap-2">
                                <AlertTriangle className="w-5 h-5 text-orange-400" />
                                <span className="text-2xl font-bold text-orange-400">{safetyData.orange_count}</span>
                            </div>
                            <div className="text-sm text-orange-400/70">Moderate Risk</div>
                        </div>
                        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30">
                            <div className="flex items-center gap-2">
                                <AlertTriangle className="w-5 h-5 text-red-400" />
                                <span className="text-2xl font-bold text-red-400">{safetyData.red_count}</span>
                            </div>
                            <div className="text-sm text-red-400/70">High Risk</div>
                        </div>
                    </motion.div>
                )}

                {/* Controls */}
                <div className="flex flex-col md:flex-row gap-4 mb-6">
                    {/* Search */}
                    <div className="relative flex-1">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                        <input
                            type="text"
                            placeholder="Search cities or states..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full pl-12 pr-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:border-emerald-500/50 transition-colors"
                        />
                    </div>

                    {/* Zone Filter */}
                    <div className="relative">
                        <select
                            value={zoneFilter}
                            onChange={(e) => setZoneFilter(e.target.value)}
                            className="appearance-none px-4 py-3 pr-10 bg-slate-800/50 border border-slate-700/50 rounded-xl text-white focus:outline-none focus:border-emerald-500/50 transition-colors cursor-pointer"
                        >
                            <option value="all">All Zones</option>
                            <option value="green">🟢 Safe</option>
                            <option value="orange">🟠 Moderate</option>
                            <option value="red">🔴 High Risk</option>
                        </select>
                        <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                    </div>

                    {/* View Toggle */}
                    <div className="flex rounded-xl overflow-hidden border border-slate-700/50">
                        <button
                            onClick={() => setViewMode('map')}
                            className={`flex items-center gap-2 px-4 py-3 transition-colors ${viewMode === 'map'
                                    ? 'bg-emerald-500/20 text-emerald-400'
                                    : 'bg-slate-800/50 text-slate-400 hover:text-white'
                                }`}
                        >
                            <MapIcon className="w-5 h-5" />
                            <span className="hidden sm:inline">Map</span>
                        </button>
                        <button
                            onClick={() => setViewMode('list')}
                            className={`flex items-center gap-2 px-4 py-3 transition-colors ${viewMode === 'list'
                                    ? 'bg-emerald-500/20 text-emerald-400'
                                    : 'bg-slate-800/50 text-slate-400 hover:text-white'
                                }`}
                        >
                            <List className="w-5 h-5" />
                            <span className="hidden sm:inline">List</span>
                        </button>
                    </div>
                </div>

                {/* Main Content */}
                {isLoading ? (
                    <MapSkeleton />
                ) : viewMode === 'map' ? (
                    <div className="grid lg:grid-cols-3 gap-6">
                        {/* Map */}
                        <div className="lg:col-span-2">
                            <MapView
                                cities={filteredCities}
                                selectedCity={selectedCity}
                                onCitySelect={setSelectedCity}
                                height="600px"
                            />
                        </div>

                        {/* Sidebar */}
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <h3 className="font-semibold text-white">
                                    Cities ({filteredCities.length})
                                </h3>
                                {selectedCity && (
                                    <button
                                        onClick={() => setSelectedCity(null)}
                                        className="text-sm text-slate-400 hover:text-white"
                                    >
                                        Clear selection
                                    </button>
                                )}
                            </div>

                            <div className="h-[540px] overflow-y-auto space-y-3 pr-2">
                                {filteredCities.map((city) => (
                                    <CityCard
                                        key={city.id}
                                        city={city}
                                        isSelected={selectedCity?.id === city.id}
                                        onClick={() => setSelectedCity(city)}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>
                ) : (
                    /* List View */
                    <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                        {filteredCities.map((city) => (
                            <CityCard
                                key={city.id}
                                city={city}
                                isSelected={selectedCity?.id === city.id}
                                onClick={() => setSelectedCity(city)}
                            />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
