'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { Map, Navigation, AlertTriangle, Phone, Home } from 'lucide-react';
import dynamic from 'next/dynamic';

// Dynamic import to avoid SSR issues with auth
const AuthButton = dynamic(() => import('./AuthButton'), { ssr: false });

const navItems = [
    { href: '/', label: 'Home', icon: Home },
    { href: '/explore', label: 'Explore', icon: Map },
    { href: '/route', label: 'Safe Route', icon: Navigation },
    { href: '/emergency', label: 'Emergency', icon: Phone },
];

export function Navbar() {
    const pathname = usePathname();

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-slate-700/50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-2 group">
                        <div className="relative">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-emerald-500/25 group-hover:shadow-emerald-500/40 transition-shadow">
                                <Map className="w-5 h-5 text-white" />
                            </div>
                            <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full border-2 border-slate-900 animate-pulse" />
                        </div>
                        <div className="hidden sm:block">
                            <h1 className="text-lg font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                                SafeTravel India
                            </h1>
                            <p className="text-xs text-slate-400 -mt-1">Your Safety Companion</p>
                        </div>
                    </Link>

                    {/* Navigation Links */}
                    <div className="flex items-center gap-1">
                        {navItems.map((item) => {
                            const isActive = pathname === item.href;
                            const Icon = item.icon;

                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className="relative px-3 py-2 rounded-lg group"
                                >
                                    {isActive && (
                                        <motion.div
                                            layoutId="navbar-active"
                                            className="absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-cyan-500/20 rounded-lg border border-emerald-500/30"
                                            transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                                        />
                                    )}
                                    <span
                                        className={`relative flex items-center gap-2 text-sm font-medium transition-colors ${isActive
                                            ? 'text-emerald-400'
                                            : 'text-slate-400 group-hover:text-white'
                                            }`}
                                    >
                                        <Icon className="w-4 h-4" />
                                        <span className="hidden sm:inline">{item.label}</span>
                                    </span>
                                </Link>
                            );
                        })}
                    </div>

                    {/* Right side: Auth + SOS */}
                    <div className="flex items-center gap-3">
                        {/* Auth Button */}
                        <AuthButton />

                        {/* Emergency Button */}
                        <Link
                            href="/emergency"
                            className="flex items-center gap-2 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 rounded-lg text-red-400 hover:text-red-300 transition-all group"
                        >
                            <AlertTriangle className="w-4 h-4 group-hover:animate-pulse" />
                            <span className="hidden sm:inline text-sm font-medium">SOS</span>
                        </Link>
                    </div>
                </div>
            </div>
        </nav>
    );
}

