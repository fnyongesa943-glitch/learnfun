'use client';

import React, { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { authAPI } from '@/lib/api';
import toast from 'react-hot-toast';

interface User {
  _id: string;
  name: string;
  email: string;
  grade: string;
  points: number;
  avatar?: string;
  role: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string, grade: string, avatar?: string) => Promise<void>;
  googleLogin: (googleData: any) => Promise<void>;
  logout: () => void;
  updateProfile: (data: Partial<User>) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const fetchUser = useCallback(async () => {
    const token =
      typeof window !== 'undefined' ? localStorage.getItem('learnfun_token') : null;
    if (!token) {
      setLoading(false);
      return;
    }
    try {
      const res = await authAPI.getProfile();
      setUser(res.data.user || res.data);
    } catch {
      localStorage.removeItem('learnfun_token');
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  const login = async (email: string, password: string) => {
    const res = await authAPI.login(email, password);
    const { token, user: userData } = res.data;
    localStorage.setItem('learnfun_token', token);
    setUser(userData);
    toast.success('Welcome back!');
    router.push('/dashboard');
  };

  const register = async (name: string, email: string, password: string, grade: string, avatar?: string) => {
    const res = await authAPI.register(name, email, password, grade, avatar);
    const { token, user: userData } = res.data;
    localStorage.setItem('learnfun_token', token);
    setUser(userData);
    toast.success('Account created successfully!');
    router.push('/dashboard');
  };

  const googleLogin = async (googleData: any) => {
    try {
      const res = await authAPI.googleLogin(googleData);
      const { token, user: userData } = res.data;
      localStorage.setItem('learnfun_token', token);
      setUser(userData);
      toast.success('Welcome!');
      router.push('/dashboard');
    } catch {
      toast.error('Google login failed');
    }
  };

  const logout = () => {
    localStorage.removeItem('learnfun_token');
    setUser(null);
    toast.success('Logged out');
    router.push('/');
  };

  const updateProfile = async (data: Partial<User>) => {
    const res = await authAPI.updateProfile(data);
    setUser(res.data.user || res.data);
    toast.success('Profile updated');
  };

  return (
    <AuthContext.Provider
      value={{ user, loading, login, register, googleLogin, logout, updateProfile }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
