'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';
import { cn, calculateLevel } from '@/lib/utils';
import {
  LayoutDashboard,
  FileQuestion,
  BookOpen,
  Trophy,
  Bot,
  BarChart3,
  Settings,
  ChevronLeft,
  ChevronRight,
  GraduationCap,
  Star,
} from 'lucide-react';

const sidebarItems = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/quizzes', label: 'My Quizzes', icon: FileQuestion },
  { href: '/lessons', label: 'Lessons', icon: BookOpen },
  { href: '/leaderboard', label: 'Leaderboard', icon: Trophy },
  { href: '/ai-tutor', label: 'AI Tutor', icon: Bot },
  { href: '/analytics', label: 'Analytics', icon: BarChart3 },
  { href: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const { user } = useAuth();
  const pathname = usePathname();

  const sidebarVariants = {
    expanded: { width: 256, transition: { duration: 0.3, ease: 'easeInOut' } },
    collapsed: { width: 72, transition: { duration: 0.3, ease: 'easeInOut' } },
  };

  const itemVariants = {
    expanded: { opacity: 1, x: 0, transition: { duration: 0.2 } },
    collapsed: { opacity: 0, x: -10, transition: { duration: 0.1 } },
  };

  return (
    <motion.aside
      variants={sidebarVariants}
      animate={collapsed ? 'collapsed' : 'expanded'}
      initial="expanded"
      className="hidden md:flex flex-col fixed left-0 top-16 bottom-0 glass border-r border-surface-200/50 dark:border-surface-700/50 overflow-hidden z-30"
      aria-label="Sidebar navigation"
    >
      <div className="flex items-center justify-end p-2">
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="rounded-lg p-1.5 text-surface-400 hover:text-surface-600 dark:hover:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500"
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </button>
      </div>

      <AnimatePresence>
        {!collapsed && user && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="mx-3 mb-4 p-3 rounded-xl bg-gradient-to-br from-primary-500/10 to-secondary-500/10 border border-primary-200/30 dark:border-primary-700/30"
          >
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-primary-400 to-secondary-500 text-white text-sm font-bold">
                {user.name?.charAt(0)?.toUpperCase() || 'U'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-surface-900 dark:text-surface-50 truncate">
                  {user.name}
                </p>
                <div className="flex items-center gap-1.5">
                  <GraduationCap className="h-3 w-3 text-primary-500" />
                  <span className="text-xs text-surface-500">Grade {user.grade}</span>
                </div>
              </div>
            </div>
            <div className="mt-3 flex items-center justify-between">
              <div className="flex items-center gap-1">
                <Star className="h-3.5 w-3.5 text-accent-500 fill-accent-500" />
                <span className="text-xs font-medium text-surface-700 dark:text-surface-300">
                  Level {calculateLevel(user.points)}
                </span>
              </div>
              <span className="text-xs text-surface-500">{user.points} pts</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <nav className="flex-1 px-2 py-2 space-y-1 overflow-y-auto">
        {sidebarItems.map((item) => {
          const isActive = pathname === item.href || pathname?.startsWith(item.href + '/');
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group',
                isActive
                  ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-500/10 shadow-sm'
                  : 'text-surface-500 dark:text-surface-400 hover:text-surface-700 dark:hover:text-surface-200 hover:bg-surface-100 dark:hover:bg-surface-800'
              )}
              aria-label={item.label}
            >
              <item.icon className={cn('h-5 w-5 shrink-0', isActive && 'text-primary-500')} />
              {!collapsed && (
                <motion.span variants={itemVariants} animate="expanded" exit="collapsed">
                  {item.label}
                </motion.span>
              )}
            </Link>
          );
        })}
      </nav>
    </motion.aside>
  );
}
