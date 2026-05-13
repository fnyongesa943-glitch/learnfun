'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import Avatar from '@/components/ui/Avatar';
import Badge from '@/components/ui/Badge';
import { calculateLevel } from '@/lib/utils';
import {
  Trophy,
  Medal,
  Crown,
  ChevronRight,
  Search,
  Users,
  BookOpen,
  Globe,
} from 'lucide-react';

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: i * 0.05, ease: 'easeOut' },
  }),
};

const staggerContainer = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.05 } },
};

const tabs = [
  { id: 'global', label: 'Global', icon: Globe },
  { id: 'grade', label: 'By Grade', icon: Users },
  { id: 'subject', label: 'By Subject', icon: BookOpen },
];

const topUsers = [
  { rank: 1, name: 'Grace Mwangi', grade: 'G7', points: 9850, level: 48, quizzes: 156, avatar: 'GM' },
  { rank: 2, name: 'James Ochieng', grade: 'G8', points: 9200, level: 45, quizzes: 142, avatar: 'JO' },
  { rank: 3, name: 'Faith Wanjiku', grade: 'G6', points: 8800, level: 43, quizzes: 138, avatar: 'FW' },
];

const otherUsers = [
  { rank: 4, name: 'Brian Kiprop', grade: 'G7', points: 8100, level: 40, quizzes: 125, avatar: 'BK' },
  { rank: 5, name: 'Sarah Akinyi', grade: 'G5', points: 7800, level: 38, quizzes: 118, avatar: 'SA' },
  { rank: 6, name: 'Daniel Mutua', grade: 'G7', points: 7400, level: 36, quizzes: 112, avatar: 'DM' },
  { rank: 7, name: 'Catherine Nyambura', grade: 'G8', points: 7100, level: 35, quizzes: 108, avatar: 'CN' },
  { rank: 8, name: 'Peter Kamau', grade: 'G6', points: 6800, level: 33, quizzes: 102, avatar: 'PK' },
  { rank: 9, name: 'Mary Wanjiku', grade: 'G5', points: 6500, level: 32, quizzes: 98, avatar: 'MW' },
  { rank: 10, name: 'Kevin Maina', grade: 'G7', points: 6200, level: 30, quizzes: 95, avatar: 'KM' },
];

const currentUserId = 7;

const podiumColors = [
  { bg: 'from-amber-400 to-yellow-500', medal: '🥇', shadow: 'shadow-amber-500/20' },
  { bg: 'from-slate-300 to-slate-400', medal: '🥈', shadow: 'shadow-slate-400/20' },
  { bg: 'from-orange-400 to-amber-600', medal: '🥉', shadow: 'shadow-orange-500/20' },
];

export default function LeaderboardPage() {
  const [activeTab, setActiveTab] = useState('global');
  const [search, setSearch] = useState('');

  const allUsers = [...topUsers, ...otherUsers];

  const filtered = allUsers.filter((u) =>
    u.name.toLowerCase().includes(search.toLowerCase())
  );

  const getRankIcon = (rank: number) => {
    if (rank === 1) return <Crown className="h-5 w-5 text-amber-500" />;
    if (rank === 2) return <Medal className="h-5 w-5 text-slate-400" />;
    if (rank === 3) return <Medal className="h-5 w-5 text-orange-500" />;
    return null;
  };

  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-900">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={staggerContainer}
          className="space-y-6"
        >
          <motion.div variants={fadeUp}>
            <h1 className="text-2xl sm:text-3xl font-bold text-surface-900 dark:text-surface-50">
              Leaderboard
            </h1>
            <p className="text-surface-500 mt-1">
              See how you rank against other learners
            </p>
          </motion.div>

          <motion.div variants={fadeUp} className="flex gap-1 p-1 rounded-xl bg-surface-100 dark:bg-surface-800 w-fit">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={cn(
                    'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                    activeTab === tab.id
                      ? 'bg-white dark:bg-surface-700 text-surface-900 dark:text-surface-50 shadow-sm'
                      : 'text-surface-500 hover:text-surface-700 dark:hover:text-surface-300'
                  )}
                  aria-label={tab.label}
                >
                  <Icon className="h-4 w-4" />
                  {tab.label}
                </button>
              );
            })}
          </motion.div>

          <motion.div variants={fadeUp} className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-surface-400" />
            <input
              type="text"
              placeholder="Search by name..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              aria-label="Search leaderboard"
            />
          </motion.div>

          <motion.div
            variants={fadeUp}
            className="flex items-end justify-center gap-4 pt-4"
          >
            {[topUsers[1], topUsers[0], topUsers[2]].map((user, idx) => {
              const isFirst = idx === 1;
              return (
                <motion.div
                  key={user.rank}
                  initial={{ opacity: 0, y: 40 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 + idx * 0.15, type: 'spring', stiffness: 200 }}
                  className={cn(
                    'flex flex-col items-center gap-2',
                    isFirst ? 'order-2' : idx === 0 ? 'order-1' : 'order-3'
                  )}
                >
                  <div className={cn(
                    'flex h-10 w-10 items-center justify-center rounded-full text-lg',
                    isFirst ? 'bg-amber-100 dark:bg-amber-500/20' : 'bg-surface-100 dark:bg-surface-700'
                  )}>
                    {podiumColors[isFirst ? 0 : idx === 0 ? 1 : 2].medal}
                  </div>
                  <div className={cn(
                    'flex items-center justify-center rounded-full bg-gradient-to-br text-white font-bold shadow-lg',
                    podiumColors[idx === 1 ? 0 : idx === 0 ? 1 : 2].bg,
                    podiumColors[idx === 1 ? 0 : idx === 0 ? 1 : 2].shadow,
                    isFirst ? 'h-20 w-20 text-2xl ring-4 ring-white dark:ring-surface-900' : 'h-16 w-16 text-lg'
                  )}>
                    {user.avatar || user.name.charAt(0)}
                  </div>
                  <div className="text-center">
                    <p className={cn(
                      'font-semibold text-surface-900 dark:text-surface-50',
                      isFirst ? 'text-base' : 'text-sm'
                    )}>
                      {user.name}
                    </p>
                    <p className="text-xs text-surface-500">Grade {user.grade}</p>
                    <p className="text-xs font-medium text-primary-500">{user.points.toLocaleString()} pts</p>
                  </div>
                  <div className={cn(
                    'h-2 rounded-t-lg w-16',
                    idx === 1 ? 'h-24 bg-gradient-to-t from-amber-400 to-amber-300' :
                    idx === 0 ? 'h-16 bg-gradient-to-t from-slate-300 to-slate-200' :
                    'h-12 bg-gradient-to-t from-orange-400 to-orange-300'
                  )} />
                </motion.div>
              );
            })}
          </motion.div>

          <motion.div variants={fadeUp} className="space-y-1">
            {filtered.map((user, i) => {
              const isCurrentUser = user.rank === currentUserId;
              const isTop3 = user.rank <= 3;
              return (
                <motion.div
                  key={user.rank}
                  variants={fadeUp}
                  custom={i}
                  className={cn(
                    'flex items-center gap-4 p-3 rounded-xl transition-colors',
                    isCurrentUser
                      ? 'bg-primary-50 dark:bg-primary-500/10 border border-primary-200 dark:border-primary-700/30'
                      : 'hover:bg-surface-100 dark:hover:bg-surface-800 border border-transparent'
                  )}
                >
                  <div className={cn(
                    'flex h-8 w-8 items-center justify-center rounded-lg text-sm font-bold',
                    isTop3 ? 'text-white' : 'text-surface-500'
                  )}>
                    {isTop3 ? (
                      <span className={cn(
                        'flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br',
                        podiumColors[user.rank - 1].bg
                      )}>
                        {getRankIcon(user.rank) || user.rank}
                      </span>
                    ) : (
                      <span className="text-surface-500">{user.rank}</span>
                    )}
                  </div>

                  <Avatar initials={user.avatar || user.name.charAt(0)} size="sm" />

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <p className="text-sm font-semibold text-surface-900 dark:text-surface-50 truncate">
                        {user.name}
                      </p>
                      {isCurrentUser && (
                        <Badge variant="primary" size="sm">You</Badge>
                      )}
                    </div>
                    <p className="text-xs text-surface-500">
                      Grade {user.grade} &middot; Level {user.level}
                    </p>
                  </div>

                  <div className="text-right">
                    <p className="text-sm font-semibold text-surface-900 dark:text-surface-50">
                      {user.points.toLocaleString()}
                    </p>
                    <p className="text-xs text-surface-500">{user.quizzes} quizzes</p>
                  </div>
                </motion.div>
              );
            })}
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
