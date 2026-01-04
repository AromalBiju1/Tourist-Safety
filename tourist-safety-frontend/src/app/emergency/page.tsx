'use client';

import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import {
    Phone,
    AlertTriangle,
    Shield,
    Ambulance,
    Flame,
    Users,
    Plane,
    MapPin,
    ExternalLink,
    Copy,
    Check,
} from 'lucide-react';
import { useState } from 'react';
import { emergencyApi } from '@/lib/api';

const emergencyCards = [
    {
        icon: Phone,
        number: '112',
        title: 'Universal Emergency',
        description: 'Works across all services',
        color: 'from-red-500 to-orange-500',
        bgColor: 'bg-red-500/20',
        borderColor: 'border-red-500/50',
    },
    {
        icon: Shield,
        number: '100',
        title: 'Police',
        description: 'Law enforcement emergency',
        color: 'from-blue-500 to-cyan-500',
        bgColor: 'bg-blue-500/20',
        borderColor: 'border-blue-500/50',
    },
    {
        icon: Ambulance,
        number: '102',
        title: 'Ambulance',
        description: 'Medical emergencies',
        color: 'from-emerald-500 to-teal-500',
        bgColor: 'bg-emerald-500/20',
        borderColor: 'border-emerald-500/50',
    },
    {
        icon: Flame,
        number: '101',
        title: 'Fire Brigade',
        description: 'Fire emergencies',
        color: 'from-orange-500 to-yellow-500',
        bgColor: 'bg-orange-500/20',
        borderColor: 'border-orange-500/50',
    },
    {
        icon: Users,
        number: '1091',
        title: 'Women Helpline',
        description: 'Women in distress',
        color: 'from-pink-500 to-purple-500',
        bgColor: 'bg-pink-500/20',
        borderColor: 'border-pink-500/50',
    },
    {
        icon: Plane,
        number: '1363',
        title: 'Tourist Helpline',
        description: 'Tourist assistance',
        color: 'from-cyan-500 to-blue-500',
        bgColor: 'bg-cyan-500/20',
        borderColor: 'border-cyan-500/50',
    },
];

function CopyButton({ text }: { text: string }) {
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        await navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <button
            onClick={handleCopy}
            className="p-2 hover:bg-slate-700/50 rounded-lg transition-colors"
        >
            {copied ? (
                <Check className="w-4 h-4 text-emerald-400" />
            ) : (
                <Copy className="w-4 h-4 text-slate-400" />
            )}
        </button>
    );
}

export default function EmergencyPage() {
    const { data: quickHelp } = useQuery({
        queryKey: ['quick-help'],
        queryFn: emergencyApi.getQuickHelp,
    });

    const { data: sosInfo } = useQuery({
        queryKey: ['sos-info'],
        queryFn: emergencyApi.getSOS,
    });

    return (
        <div className="min-h-screen bg-pattern">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header with SOS */}
                <div className="text-center mb-12">
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: 'spring', bounce: 0.5 }}
                        className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-red-500/20 border-2 border-red-500/50 mb-6 pulse-glow"
                    >
                        <AlertTriangle className="w-12 h-12 text-red-400" />
                    </motion.div>
                    <h1 className="text-4xl font-bold mb-4">
                        <span className="text-red-400">Emergency</span> Support
                    </h1>
                    <p className="text-slate-400 max-w-2xl mx-auto">
                        Quick access to emergency services and important contacts. Stay calm and call for help when needed.
                    </p>
                </div>

                {/* Emergency Numbers Grid */}
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-12">
                    {emergencyCards.map((card, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className={`relative p-6 rounded-2xl ${card.bgColor} border ${card.borderColor} overflow-hidden group`}
                        >
                            {/* Background gradient */}
                            <div
                                className={`absolute inset-0 bg-gradient-to-br ${card.color} opacity-0 group-hover:opacity-10 transition-opacity`}
                            />

                            <div className="relative">
                                <div className="flex items-center justify-between mb-4">
                                    <card.icon className="w-8 h-8 text-white" />
                                    <CopyButton text={card.number} />
                                </div>

                                <a
                                    href={`tel:${card.number}`}
                                    className="text-4xl font-bold text-white hover:underline"
                                >
                                    {card.number}
                                </a>

                                <h3 className="text-lg font-semibold text-white mt-2">{card.title}</h3>
                                <p className="text-sm text-slate-300">{card.description}</p>

                                <a
                                    href={`tel:${card.number}`}
                                    className="inline-flex items-center gap-2 mt-4 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white text-sm font-medium transition-colors"
                                >
                                    <Phone className="w-4 h-4" />
                                    Call Now
                                </a>
                            </div>
                        </motion.div>
                    ))}
                </div>

                {/* SOS Steps */}
                {sosInfo && (
                    <div className="mb-12">
                        <h2 className="text-2xl font-bold mb-6">
                            <span className="gradient-text">What to Do</span> in an Emergency
                        </h2>
                        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                            {sosInfo.immediate_actions.map((action: any, index: number) => (
                                <motion.div
                                    key={index}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: index * 0.15 }}
                                    className="p-6 rounded-2xl bg-slate-800/50 border border-slate-700/50"
                                >
                                    <div className="flex items-center gap-3 mb-4">
                                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-cyan-500 flex items-center justify-center text-white font-bold">
                                            {action.step}
                                        </div>
                                        <span className="text-2xl">{action.icon}</span>
                                    </div>
                                    <h3 className="font-semibold text-white mb-2">{action.title}</h3>
                                    <p className="text-sm text-slate-400">{action.description}</p>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Embassy Contacts */}
                {sosInfo?.important_embassies && (
                    <div className="mb-12">
                        <h2 className="text-2xl font-bold mb-6">
                            <span className="gradient-text">Embassy</span> Contacts
                        </h2>
                        <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-4">
                            {Object.entries(sosInfo.important_embassies).map(
                                ([country, phone]: [string, any], index) => (
                                    <motion.div
                                        key={country}
                                        initial={{ opacity: 0, scale: 0.9 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        transition={{ delay: index * 0.1 }}
                                        className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/50 hover:border-slate-600 transition-colors"
                                    >
                                        <div className="flex items-center justify-between mb-2">
                                            <span className="font-medium text-white">{country}</span>
                                            <CopyButton text={phone} />
                                        </div>
                                        <a
                                            href={`tel:${phone}`}
                                            className="text-emerald-400 hover:text-emerald-300 text-sm"
                                        >
                                            {phone}
                                        </a>
                                    </motion.div>
                                )
                            )}
                        </div>
                    </div>
                )}

                {/* Safety Tips */}
                {quickHelp?.tips && (
                    <div className="p-8 rounded-2xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-slate-700/50">
                        <h2 className="text-2xl font-bold mb-6">
                            <span className="gradient-text">Safety</span> Tips
                        </h2>
                        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                            {quickHelp.tips.map((tip: string, index: number) => (
                                <div
                                    key={index}
                                    className="flex items-start gap-3 p-4 rounded-xl bg-slate-900/50"
                                >
                                    <div className="w-6 h-6 rounded-full bg-emerald-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                                        <Check className="w-3 h-3 text-emerald-400" />
                                    </div>
                                    <span className="text-slate-300">{tip}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Quick Action Bar */}
                <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50">
                    <motion.div
                        initial={{ y: 100, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        transition={{ delay: 1 }}
                        className="flex items-center gap-4 px-6 py-4 rounded-2xl bg-slate-900/95 backdrop-blur-md border border-slate-700/50 shadow-2xl"
                    >
                        <span className="text-slate-400 text-sm">Quick Call:</span>
                        <a
                            href="tel:112"
                            className="flex items-center gap-2 px-4 py-2 bg-red-500 hover:bg-red-600 rounded-lg text-white font-medium transition-colors"
                        >
                            <Phone className="w-4 h-4" />
                            112
                        </a>
                        <a
                            href="tel:100"
                            className="flex items-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg text-white font-medium transition-colors"
                        >
                            <Shield className="w-4 h-4" />
                            100
                        </a>
                        <a
                            href="tel:102"
                            className="flex items-center gap-2 px-4 py-2 bg-emerald-500 hover:bg-emerald-600 rounded-lg text-white font-medium transition-colors"
                        >
                            <Ambulance className="w-4 h-4" />
                            102
                        </a>
                    </motion.div>
                </div>
            </div>
        </div>
    );
}
