'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { Map, Navigation, Shield, Phone, AlertTriangle, ChevronRight, Star, Users, MapPin } from 'lucide-react';

const features = [
  {
    icon: Map,
    title: 'Safety Zones Map',
    description: 'Visualize cities across India color-coded by safety levels based on crime data.',
    color: 'from-emerald-500 to-cyan-500',
    href: '/explore',
  },
  {
    icon: Navigation,
    title: 'Safe Route Planning',
    description: 'Get routes optimized for safety, avoiding high-risk areas when possible.',
    color: 'from-cyan-500 to-blue-500',
    href: '/route',
  },
  {
    icon: Shield,
    title: 'Tourist Hotspots',
    description: 'Discover popular attractions with safety ratings for each location.',
    color: 'from-purple-500 to-pink-500',
    href: '/explore',
  },
  {
    icon: Phone,
    title: 'Emergency Support',
    description: 'Quick access to emergency contacts and step-by-step guidance for crisis situations.',
    color: 'from-red-500 to-orange-500',
    href: '/emergency',
  },
];

const stats = [
  { value: '50+', label: 'Cities Covered' },
  { value: '3', label: 'Safety Zones' },
  { value: '100+', label: 'Attractions' },
  { value: '24/7', label: 'Emergency Help' },
];

export default function HomePage() {
  return (
    <div className="min-h-screen bg-pattern">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
          <div className="text-center">
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm font-medium mb-8"
            >
              <Shield className="w-4 h-4" />
              <span>Your Safety is Our Priority</span>
            </motion.div>

            {/* Title */}
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="text-4xl sm:text-5xl lg:text-7xl font-bold mb-6"
            >
              Travel <span className="gradient-text">Safely</span> Across
              <br />
              <span className="gradient-text">India</span>
            </motion.h1>

            {/* Description */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto mb-10"
            >
              Discover tourist hotspots, plan safe routes, and access emergency support
              with real-time safety data for cities across India.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
            >
              <Link
                href="/explore"
                className="group flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-xl text-white font-semibold shadow-lg shadow-emerald-500/25 hover:shadow-emerald-500/40 transition-all"
              >
                <Map className="w-5 h-5" />
                Explore Safety Map
                <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                href="/route"
                className="flex items-center gap-2 px-8 py-4 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl text-white font-semibold transition-all"
              >
                <Navigation className="w-5 h-5" />
                Plan Safe Route
              </Link>
            </motion.div>
          </div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8"
          >
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-3xl sm:text-4xl font-bold gradient-text">
                  {stat.value}
                </div>
                <div className="text-slate-400 mt-1">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-slate-900/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">
              Everything You Need for
              <span className="gradient-text"> Safe Travel</span>
            </h2>
            <p className="text-slate-400 max-w-2xl mx-auto">
              Our comprehensive platform combines safety data, navigation, and emergency
              support to ensure you have a worry-free travel experience.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
              >
                <Link
                  href={feature.href}
                  className="block h-full p-6 rounded-2xl bg-slate-800/50 border border-slate-700/50 hover:border-slate-600 transition-all group"
                >
                  <div
                    className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}
                  >
                    <feature.icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-white mb-2 group-hover:text-emerald-400 transition-colors">
                    {feature.title}
                  </h3>
                  <p className="text-slate-400 text-sm">{feature.description}</p>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Safety Zones Explanation */}
      <section className="py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl sm:text-4xl font-bold mb-6">
                Understanding Our
                <span className="gradient-text"> Safety Zones</span>
              </h2>
              <p className="text-slate-400 mb-8">
                We analyze crime data from official sources to classify cities into
                three safety zones, helping you make informed travel decisions.
              </p>

              <div className="space-y-4">
                <div className="flex items-start gap-4 p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30">
                  <div className="w-10 h-10 rounded-lg bg-emerald-500 flex items-center justify-center flex-shrink-0">
                    <Shield className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-emerald-400">Green Zone - Safe</h4>
                    <p className="text-sm text-slate-400">Low crime rate, highly recommended for tourists</p>
                  </div>
                </div>

                <div className="flex items-start gap-4 p-4 rounded-xl bg-orange-500/10 border border-orange-500/30">
                  <div className="w-10 h-10 rounded-lg bg-orange-500 flex items-center justify-center flex-shrink-0">
                    <AlertTriangle className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-orange-400">Orange Zone - Moderate</h4>
                    <p className="text-sm text-slate-400">Exercise normal precautions, stay aware</p>
                  </div>
                </div>

                <div className="flex items-start gap-4 p-4 rounded-xl bg-red-500/10 border border-red-500/30">
                  <div className="w-10 h-10 rounded-lg bg-red-500 flex items-center justify-center flex-shrink-0">
                    <AlertTriangle className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-red-400">Red Zone - High Risk</h4>
                    <p className="text-sm text-slate-400">Increased caution advised, avoid isolated areas</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="aspect-square rounded-2xl bg-slate-800/50 border border-slate-700/50 overflow-hidden">
                {/* Placeholder for map preview */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <Map className="w-16 h-16 text-slate-600 mx-auto mb-4" />
                    <p className="text-slate-500">Interactive Safety Map</p>
                    <Link
                      href="/explore"
                      className="inline-flex items-center gap-2 mt-4 text-emerald-400 hover:text-emerald-300"
                    >
                      View Full Map
                      <ChevronRight className="w-4 h-4" />
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Emergency CTA */}
      <section className="py-24 bg-gradient-to-b from-slate-900/50 to-slate-950">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-red-500/20 border border-red-500/30 mb-8 pulse-glow">
            <Phone className="w-10 h-10 text-red-400" />
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            Need <span className="text-red-400">Emergency</span> Help?
          </h2>
          <p className="text-slate-400 mb-8 max-w-2xl mx-auto">
            Access emergency contacts, step-by-step guidance, and quick help resources
            for any crisis situation during your travels.
          </p>
          <Link
            href="/emergency"
            className="inline-flex items-center gap-2 px-8 py-4 bg-red-500 hover:bg-red-600 rounded-xl text-white font-semibold shadow-lg shadow-red-500/25 transition-all"
          >
            <AlertTriangle className="w-5 h-5" />
            Emergency Resources
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-cyan-500 flex items-center justify-center">
                <Map className="w-4 h-4 text-white" />
              </div>
              <span className="font-semibold gradient-text">SafeTravel India</span>
            </div>
            <p className="text-slate-500 text-sm">
              Data sourced from NCRB and official government records
            </p>
            <div className="flex items-center gap-4 text-slate-400">
              <span className="text-sm">Emergency: 112</span>
              <span className="text-sm">Tourist Helpline: 1363</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
