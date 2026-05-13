'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';
import { Mail, Lock, Eye, EyeOff, ArrowRight, Sparkles, User, GraduationCap } from 'lucide-react';
import { cn } from '@/lib/utils';

const GRADES = [
  'PP1', 'PP2', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
];

const emojiAvatars = [
  '😎', '🚀', '🌟', '🎓', '💡', '🎨', '🌈', '🦸', '🧠', '📚',
  '🎯', '💪', '🔥', '⭐', '🏆', '🦁', '🐯', '🦅', '🐉', '🦋',
];

interface FormErrors {
  name?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
  grade?: string;
}

export default function RegisterPage() {
  const [form, setForm] = useState({ name: '', email: '', password: '', confirmPassword: '', grade: '', avatar: '😎' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});
  const { register } = useAuth();

  const updateField = (field: string, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    if (errors[field as keyof FormErrors]) {
      setErrors((prev) => ({ ...prev, [field]: undefined }));
    }
  };

  const validate = (): boolean => {
    const errs: FormErrors = {};
    if (!form.name.trim()) errs.name = 'Full name is required';
    if (!form.email) errs.email = 'Email is required';
    else if (!/\S+@\S+\.\S+/.test(form.email)) errs.email = 'Invalid email address';
    if (!form.password) errs.password = 'Password is required';
    else if (form.password.length < 6) errs.password = 'Password must be at least 6 characters';
    if (!form.confirmPassword) errs.confirmPassword = 'Please confirm your password';
    else if (form.password !== form.confirmPassword) errs.confirmPassword = 'Passwords do not match';
    if (!form.grade) errs.grade = 'Please select your grade';
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);
    try {
      await register(form.name, form.email, form.password, form.grade, form.avatar);
    } catch (err: any) {
      const msg = err.response?.data?.message || 'Registration failed. Please try again.';
      setErrors({ email: msg });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-secondary-50 via-white to-primary-50 dark:from-surface-900 dark:via-surface-900 dark:to-surface-800 p-4 py-8">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-secondary-400/20 rounded-full blur-[100px]" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-primary-400/20 rounded-full blur-[100px]" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="relative w-full max-w-md"
      >
        <div className="glass rounded-2xl p-8 shadow-xl shadow-secondary-500/5 border border-surface-200/50 dark:border-surface-700/50">
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 300, delay: 0.1 }}
              className="inline-flex items-center justify-center h-14 w-14 rounded-xl bg-gradient-to-br from-secondary-500 to-primary-500 text-white mb-4 shadow-lg shadow-secondary-500/20"
            >
              <Sparkles className="h-7 w-7" />
            </motion.div>
            <h1 className="text-2xl font-bold text-surface-900 dark:text-surface-50">
              Create your account
            </h1>
            <p className="text-surface-500 mt-1">Start your learning journey today</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4" noValidate>
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-surface-700 dark:text-surface-300 mb-1.5">
                Full Name
              </label>
              <div className="relative">
                <User className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-surface-400" />
                <input
                  id="name"
                  type="text"
                  value={form.name}
                  onChange={(e) => updateField('name', e.target.value)}
                  placeholder="John Doe"
                  className={cn(
                    'w-full rounded-xl border bg-white dark:bg-surface-800/50 py-2.5 pl-10 pr-4 text-sm text-surface-900 dark:text-surface-50 placeholder-surface-400 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500',
                    errors.name
                      ? 'border-danger-400 focus:ring-danger-500/50 focus:border-danger-500'
                      : 'border-surface-200 dark:border-surface-700'
                  )}
                  aria-label="Full name"
                  aria-invalid={!!errors.name}
                  aria-describedby={errors.name ? 'name-error' : undefined}
                  autoComplete="name"
                />
              </div>
              {errors.name && (
                <motion.p initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} id="name-error" className="mt-1.5 text-xs text-danger-500">
                  {errors.name}
                </motion.p>
              )}
            </div>

            <div>
              <label htmlFor="reg-email" className="block text-sm font-medium text-surface-700 dark:text-surface-300 mb-1.5">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-surface-400" />
                <input
                  id="reg-email"
                  type="email"
                  value={form.email}
                  onChange={(e) => updateField('email', e.target.value)}
                  placeholder="you@example.com"
                  className={cn(
                    'w-full rounded-xl border bg-white dark:bg-surface-800/50 py-2.5 pl-10 pr-4 text-sm text-surface-900 dark:text-surface-50 placeholder-surface-400 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500',
                    errors.email
                      ? 'border-danger-400 focus:ring-danger-500/50 focus:border-danger-500'
                      : 'border-surface-200 dark:border-surface-700'
                  )}
                  aria-label="Email address"
                  aria-invalid={!!errors.email}
                  aria-describedby={errors.email ? 'reg-email-error' : undefined}
                  autoComplete="email"
                />
              </div>
              {errors.email && (
                <motion.p initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} id="reg-email-error" className="mt-1.5 text-xs text-danger-500">
                  {errors.email}
                </motion.p>
              )}
            </div>

            <div>
              <label htmlFor="grade" className="block text-sm font-medium text-surface-700 dark:text-surface-300 mb-1.5">
                Grade
              </label>
              <div className="relative">
                <GraduationCap className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-surface-400 z-10" />
                <select
                  id="grade"
                  value={form.grade}
                  onChange={(e) => updateField('grade', e.target.value)}
                  className={cn(
                    'w-full rounded-xl border bg-white dark:bg-surface-800/50 py-2.5 pl-10 pr-4 text-sm text-surface-900 dark:text-surface-50 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 appearance-none',
                    !form.grade && 'text-surface-400',
                    errors.grade
                      ? 'border-danger-400 focus:ring-danger-500/50 focus:border-danger-500'
                      : 'border-surface-200 dark:border-surface-700'
                  )}
                  aria-label="Grade level"
                  aria-invalid={!!errors.grade}
                  aria-describedby={errors.grade ? 'grade-error' : undefined}
                >
                  <option value="" disabled>Select your grade</option>
                  {GRADES.map((g) => (
                    <option key={g} value={g}>{g}</option>
                  ))}
                </select>
              </div>
              {errors.grade && (
                <motion.p initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} id="grade-error" className="mt-1.5 text-xs text-danger-500">
                  {errors.grade}
                </motion.p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-surface-700 dark:text-surface-300 mb-1.5">
                Choose Your Avatar
              </label>
              <div className="grid grid-cols-5 gap-2">
                {emojiAvatars.map((emoji) => (
                  <button
                    key={emoji}
                    type="button"
                    onClick={() => setForm((prev) => ({ ...prev, avatar: emoji }))}
                    className={cn(
                      'flex items-center justify-center h-10 w-10 rounded-lg text-xl transition-all border-2',
                      form.avatar === emoji
                        ? 'border-primary-500 bg-primary-50 dark:bg-primary-500/10 scale-110'
                        : 'border-surface-200 dark:border-surface-700 hover:border-primary-300 dark:hover:border-primary-600'
                    )}
                    aria-label={`Select avatar ${emoji}`}
                  >
                    {emoji}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label htmlFor="reg-password" className="block text-sm font-medium text-surface-700 dark:text-surface-300 mb-1.5">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-surface-400" />
                <input
                  id="reg-password"
                  type={showPassword ? 'text' : 'password'}
                  value={form.password}
                  onChange={(e) => updateField('password', e.target.value)}
                  placeholder="Create a password"
                  className={cn(
                    'w-full rounded-xl border bg-white dark:bg-surface-800/50 py-2.5 pl-10 pr-10 text-sm text-surface-900 dark:text-surface-50 placeholder-surface-400 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500',
                    errors.password
                      ? 'border-danger-400 focus:ring-danger-500/50 focus:border-danger-500'
                      : 'border-surface-200 dark:border-surface-700'
                  )}
                  aria-label="Password"
                  aria-invalid={!!errors.password}
                  aria-describedby={errors.password ? 'reg-password-error' : undefined}
                  autoComplete="new-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-surface-400 hover:text-surface-600 dark:hover:text-surface-300"
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              {errors.password && (
                <motion.p initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} id="reg-password-error" className="mt-1.5 text-xs text-danger-500">
                  {errors.password}
                </motion.p>
              )}
            </div>

            <div>
              <label htmlFor="confirm-password" className="block text-sm font-medium text-surface-700 dark:text-surface-300 mb-1.5">
                Confirm Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-surface-400" />
                <input
                  id="confirm-password"
                  type={showPassword ? 'text' : 'password'}
                  value={form.confirmPassword}
                  onChange={(e) => updateField('confirmPassword', e.target.value)}
                  placeholder="Confirm your password"
                  className={cn(
                    'w-full rounded-xl border bg-white dark:bg-surface-800/50 py-2.5 pl-10 pr-4 text-sm text-surface-900 dark:text-surface-50 placeholder-surface-400 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500',
                    errors.confirmPassword
                      ? 'border-danger-400 focus:ring-danger-500/50 focus:border-danger-500'
                      : 'border-surface-200 dark:border-surface-700'
                  )}
                  aria-label="Confirm password"
                  aria-invalid={!!errors.confirmPassword}
                  aria-describedby={errors.confirmPassword ? 'confirm-password-error' : undefined}
                  autoComplete="new-password"
                />
              </div>
              {errors.confirmPassword && (
                <motion.p initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} id="confirm-password-error" className="mt-1.5 text-xs text-danger-500">
                  {errors.confirmPassword}
                </motion.p>
              )}
            </div>

            <motion.button
              type="submit"
              disabled={loading}
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
              className={cn(
                'w-full inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-secondary-500 to-primary-500 py-2.5 text-sm font-semibold text-white shadow-lg shadow-secondary-500/20 hover:shadow-xl hover:shadow-secondary-500/30 transition-all duration-300',
                loading && 'opacity-70 cursor-not-allowed'
              )}
              aria-label="Create account"
            >
              {loading ? (
                <div className="h-5 w-5 rounded-full border-2 border-white/30 border-t-white animate-spin" />
              ) : (
                <>
                  Create Account
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </motion.button>
          </form>

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-surface-200 dark:border-surface-700" />
            </div>
            <div className="relative flex justify-center text-xs">
              <span className="bg-white dark:bg-surface-800 px-3 text-surface-500">or sign up with</span>
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            className="w-full inline-flex items-center justify-center gap-3 rounded-xl border border-surface-200 dark:border-surface-700 py-2.5 text-sm font-medium text-surface-700 dark:text-surface-300 hover:bg-surface-50 dark:hover:bg-surface-800 transition-colors"
            aria-label="Sign up with Google"
          >
            <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4" />
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
            </svg>
            Sign up with Google
          </motion.button>

          <p className="mt-6 text-center text-sm text-surface-500">
            Already have an account?{' '}
            <Link href="/auth/login" className="text-primary-500 hover:text-primary-600 font-medium">
              Sign in
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
}
