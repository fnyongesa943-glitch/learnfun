'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { useTheme } from '@/context/ThemeContext';
import { useAuth } from '@/context/AuthContext';
import { cn, calculateLevel } from '@/lib/utils';
import {
  Sun,
  Moon,
  Menu,
  X,
  LayoutDashboard,
  FileQuestion,
  BookOpen,
  Trophy,
  Bot,
  User,
  Settings,
  LogOut,
  ChevronDown,
} from 'lucide-react';

const navLinks = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/quizzes', label: 'Quizzes', icon: FileQuestion },
  { href: '/lessons', label: 'Lessons', icon: BookOpen },
  { href: '/leaderboard', label: 'Leaderboard', icon: Trophy },
  { href: '/ai-tutor', label: 'AI Tutor', icon: Bot },
];

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const { theme, setTheme } = useTheme();
  const { user, logout } = useAuth();
  const pathname = usePathname();

  const isAuthPage = pathname?.startsWith('/auth');

  const sidebarVariants = {
    open: { x: 0, transition: { type: 'spring', stiffness: 300, damping: 30 } },
    closed: { x: '100%', transition: { type: 'spring', stiffness: 300, damping: 30 } },
  };

  const itemVariants = {
    open: (i: number) => ({
      opacity: 1,
      x: 0,
      transition: { delay: i * 0.05, type: 'spring', stiffness: 300 },
    }),
    closed: { opacity: 0, x: 50 },
  };

  return (
    <nav
      className={cn(
        'sticky top-0 z-50 w-full glass border-b border-surface-200/50 dark:border-surface-700/50',
        isAuthPage && 'relative'
      )}
      aria-label="Main navigation"
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center gap-2" aria-label="LearnFun Home">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary-500 to-secondary-500 text-white text-sm font-bold">
              L
            </div>
            <span className="text-xl font-bold text-gradient">LearnFun</span>
          </Link>

          <div className="hidden md:flex items-center gap-1">
            {!isAuthPage &&
              navLinks.map((link) => {
                const isActive = pathname === link.href || pathname?.startsWith(link.href + '/');
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={cn(
                      'relative flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                      isActive
                        ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-500/10'
                        : 'text-surface-600 dark:text-surface-400 hover:text-surface-900 dark:hover:text-surface-100 hover:bg-surface-100 dark:hover:bg-surface-800'
                    )}
                    aria-label={link.label}
                  >
                    <link.icon className="h-4 w-4" />
                    {link.label}
                  </Link>
                );
              })}
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              className="rounded-lg p-2 text-surface-500 hover:text-surface-900 dark:hover:text-surface-100 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500"
              aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
            >
              <AnimatePresence mode="wait">
                {theme === 'dark' ? (
                  <motion.div
                    key="sun"
                    initial={{ rotate: -90, opacity: 0 }}
                    animate={{ rotate: 0, opacity: 1 }}
                    exit={{ rotate: 90, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Sun className="h-5 w-5" />
                  </motion.div>
                ) : (
                  <motion.div
                    key="moon"
                    initial={{ rotate: 90, opacity: 0 }}
                    animate={{ rotate: 0, opacity: 1 }}
                    exit={{ rotate: -90, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Moon className="h-5 w-5" />
                  </motion.div>
                )}
              </AnimatePresence>
            </button>

            {user ? (
              <div className="relative">
                <button
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="flex items-center gap-2 rounded-lg p-1.5 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500"
                  aria-label="User menu"
                  aria-expanded={dropdownOpen}
                >
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-primary-400 to-secondary-500 text-white text-sm font-semibold">
                    {user.avatar || user.name?.charAt(0)?.toUpperCase() || 'U'}
                  </div>
                  <ChevronDown className="hidden md:block h-4 w-4 text-surface-400" />
                </button>
                <AnimatePresence>
                  {dropdownOpen && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      transition={{ duration: 0.15 }}
                      className="absolute right-0 mt-2 w-56 glass rounded-xl shadow-xl border border-surface-200 dark:border-surface-700 overflow-hidden"
                    >
                      <div className="p-3 border-b border-surface-100 dark:border-surface-700">
                        <p className="text-sm font-semibold text-surface-900 dark:text-surface-50">{user.name}</p>
                        <p className="text-xs text-surface-500">{user.email}</p>
                        <div className="flex items-center gap-2 mt-2">
                          <span className="text-xs font-medium text-primary-600 dark:text-primary-400">
                            Level {calculateLevel(user.points)}
                          </span>
                          <span className="text-xs text-surface-400">|</span>
                          <span className="text-xs text-surface-500">{user.points} pts</span>
                        </div>
                      </div>
                      <div className="p-1">
                        <DropdownItem href="/profile" icon={User} label="Profile" onClick={() => setDropdownOpen(false)} />
                        <DropdownItem href="/settings" icon={Settings} label="Settings" onClick={() => setDropdownOpen(false)} />
                        <button
                          onClick={() => { setDropdownOpen(false); logout(); }}
                          className="flex w-full items-center gap-3 px-3 py-2 rounded-lg text-sm text-danger-500 hover:bg-danger-50 dark:hover:bg-danger-500/10 transition-colors"
                          aria-label="Logout"
                        >
                          <LogOut className="h-4 w-4" />
                          Logout
                        </button>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ) : (
              !isAuthPage && (
                <Link
                  href="/auth/login"
                  className="rounded-lg bg-primary-500 px-4 py-2 text-sm font-medium text-white hover:bg-primary-600 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500"
                  aria-label="Sign in"
                >
                  Sign In
                </Link>
              )
            )}

            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="md:hidden rounded-lg p-2 text-surface-500 hover:text-surface-900 dark:hover:text-surface-100 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500"
              aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
            >
              {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>
      </div>

      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileOpen(false)}
              className="fixed inset-0 bg-black/20 backdrop-blur-sm md:hidden z-40"
            />
            <motion.div
              variants={sidebarVariants}
              initial="closed"
              animate="open"
              exit="closed"
              className="fixed top-0 right-0 bottom-0 w-72 glass border-l border-surface-200 dark:border-surface-700 z-50 md:hidden"
            >
              <div className="flex items-center justify-between p-4 border-b border-surface-100 dark:border-surface-700">
                <span className="text-lg font-bold text-gradient">LearnFun</span>
                <button
                  onClick={() => setMobileOpen(false)}
                  className="rounded-lg p-2 text-surface-500 hover:bg-surface-100 dark:hover:bg-surface-800 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  aria-label="Close menu"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              <div className="p-4 space-y-1">
                {!isAuthPage &&
                  navLinks.map((link, i) => {
                    const isActive = pathname === link.href;
                    return (
                      <motion.div
                        key={link.href}
                        custom={i}
                        variants={itemVariants}
                        initial="closed"
                        animate="open"
                      >
                        <Link
                          href={link.href}
                          onClick={() => setMobileOpen(false)}
                          className={cn(
                            'flex items-center gap-3 px-3 py-3 rounded-lg text-sm font-medium transition-colors',
                            isActive
                              ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-500/10'
                              : 'text-surface-600 dark:text-surface-400 hover:text-surface-900 dark:hover:text-surface-100 hover:bg-surface-100 dark:hover:bg-surface-800'
                          )}
                          aria-label={link.label}
                        >
                          <link.icon className="h-5 w-5" />
                          {link.label}
                        </Link>
                      </motion.div>
                    );
                  })}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </nav>
  );
}

function DropdownItem({
  href,
  icon: Icon,
  label,
  onClick,
}: {
  href: string;
  icon: any;
  label: string;
  onClick?: () => void;
}) {
  return (
    <Link
      href={href}
      onClick={onClick}
      className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-surface-700 dark:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
      aria-label={label}
    >
      <Icon className="h-4 w-4" />
      {label}
    </Link>
  );
}
