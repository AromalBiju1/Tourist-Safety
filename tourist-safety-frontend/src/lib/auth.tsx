'use client';

import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import api from './api';

// Types
interface User {
    id: number;
    email: string;
    name: string | null;
    picture: string | null;
    is_active: boolean;
}

interface AuthContextType {
    user: User | null;
    isLoading: boolean;
    isAuthenticated: boolean;
    login: (email: string, name?: string) => Promise<void>;
    loginWithGoogle: (token: string) => Promise<void>;
    logout: () => void;
    checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Storage keys
const TOKEN_KEY = 'tourist_safety_token';
const USER_KEY = 'tourist_safety_user';

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const isAuthenticated = !!user;

    // Load user from storage on mount
    useEffect(() => {
        const loadUser = () => {
            try {
                const savedUser = localStorage.getItem(USER_KEY);
                const savedToken = localStorage.getItem(TOKEN_KEY);

                if (savedUser && savedToken) {
                    setUser(JSON.parse(savedUser));
                    // Set auth header for API calls
                    api.defaults.headers.common['Authorization'] = `Bearer ${savedToken}`;
                }
            } catch (e) {
                console.error('Error loading user from storage:', e);
            } finally {
                setIsLoading(false);
            }
        };

        loadUser();
    }, []);

    // Mock login (for development without Google)
    const login = useCallback(async (email: string, name?: string) => {
        try {
            setIsLoading(true);

            const response = await api.post('/auth/mock-login', {
                email,
                name: name || 'User'
            });

            const { access_token, user: userData } = response.data;

            // Save to storage
            localStorage.setItem(TOKEN_KEY, access_token);
            localStorage.setItem(USER_KEY, JSON.stringify(userData));

            // Set auth header
            api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

            setUser(userData);
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        } finally {
            setIsLoading(false);
        }
    }, []);

    // Google OAuth login
    const loginWithGoogle = useCallback(async (token: string) => {
        try {
            setIsLoading(true);

            const response = await api.post('/auth/google', { token });

            const { access_token, user: userData } = response.data;

            // Save to storage
            localStorage.setItem(TOKEN_KEY, access_token);
            localStorage.setItem(USER_KEY, JSON.stringify(userData));

            // Set auth header
            api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

            setUser(userData);
        } catch (error) {
            console.error('Google login failed:', error);
            throw error;
        } finally {
            setIsLoading(false);
        }
    }, []);

    // Logout
    const logout = useCallback(() => {
        // Clear storage
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);

        // Clear auth header
        delete api.defaults.headers.common['Authorization'];

        setUser(null);
    }, []);

    // Check if user is still authenticated
    const checkAuth = useCallback(async () => {
        const token = localStorage.getItem(TOKEN_KEY);

        if (!token) {
            setUser(null);
            setIsLoading(false);
            return;
        }

        try {
            api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

            const response = await api.get('/auth/me');
            setUser(response.data);
        } catch (error) {
            // Token expired or invalid
            logout();
        } finally {
            setIsLoading(false);
        }
    }, [logout]);

    const value = {
        user,
        isLoading,
        isAuthenticated,
        login,
        loginWithGoogle,
        logout,
        checkAuth
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

// Custom hook to use auth context
export function useAuth() {
    const context = useContext(AuthContext);

    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }

    return context;
}

// Higher-order component for protected routes
export function withAuth<P extends object>(
    Component: React.ComponentType<P>,
    redirectTo: string = '/login'
) {
    return function AuthenticatedComponent(props: P) {
        const { isAuthenticated, isLoading } = useAuth();

        if (isLoading) {
            return (
                <div className="min-h-screen flex items-center justify-center">
                    <div className="animate-spin w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full"></div>
                </div>
            );
        }

        if (!isAuthenticated) {
            // In a real app, you'd redirect here
            return (
                <div className="min-h-screen flex items-center justify-center">
                    <div className="text-center">
                        <h2 className="text-2xl font-bold text-white mb-4">Please Sign In</h2>
                        <p className="text-gray-400">You need to be logged in to access this page.</p>
                    </div>
                </div>
            );
        }

        return <Component {...props} />;
    };
}
