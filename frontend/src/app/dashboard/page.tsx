'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';
import { calculateLevel } from '@/lib/utils';
import StatsCard from '@/components/dashboard/StatsCard';
import QuizCard from '@/components/dashboard/QuizCard';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
} from 'recharts';
import {
  FileQuestion,
  BarChart3,
  BookOpen,
  Flame,
  Brain,
  Clock,
  CheckCircle2,
  XCircle,
  ChevronRight,
  Sparkles,
  Zap,
  TrendingUp,
  Award,
  Target,
  AlertTriangle,
} from 'lucide-react';
import { cn } from '@/lib/utils';

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: i * 0.1, ease: 'easeOut' },
  }),
};

const staggerContainer = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
};

const chartData = [
  { day: 'Mon', score: 65 },
  { day: 'Tue', score: 72 },
  { day: 'Wed', score: 68 },
  { day: 'Thu', score: 85 },
  { day: 'Fri', score: 78 },
  { day: 'Sat', score: 92 },
  { day: 'Sun', score: 88 },
];

const recommendedQuizzes = [
  { id: '1', title: 'Fractions & Decimals', subject: 'Mathematics', difficulty: 'medium', questionCount: 15, timeLimit: 20, color: 'from-blue-400 to-blue-600' },
  { id: '2', title: 'Parts of Speech', subject: 'English', difficulty: 'easy', questionCount: 10, timeLimit: 15, color: 'from-emerald-400 to-emerald-600' },
  { id: '3', title: 'Photosynthesis', subject: 'Science', difficulty: 'hard', questionCount: 20, timeLimit: 25, color: 'from-purple-400 to-purple-600' },
];

const recentActivity = [
  { id: '1', title: 'Multiplication Tables', score: 85, total: 10, date: '2 hours ago', subject: 'Mathematics' },
  { id: '2', title: 'Verb Tenses', score: 60, total: 8, date: 'Yesterday', subject: 'English' },
  { id: '3', title: 'Solar System', score: 90, total: 12, date: '2 days ago', subject: 'Science' },
  { id: '4', title: 'Addition Skills', score: 100, total: 10, date: '3 days ago', subject: 'Mathematics' },
  { id: '5', title: 'Grammar Basics', score: 45, total: 10, date: '4 days ago', subject: 'English' },
];

const weakTopics = [
  { subject: 'English', topic: 'Verb Tenses', score: 55, color: 'from-red-400 to-red-500' },
  { subject: 'Mathematics', topic: 'Long Division', score: 40, color: 'from-orange-400 to-orange-500' },
  { subject: 'Science', topic: 'Chemical Reactions', score: 50, color: 'from-yellow-400 to-yellow-500' },
];

export default function DashboardPage() {
  const { user } = useAuth();
  const [greeting, setGreeting] = useState('');

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting('Good morning');
    else if (hour < 18) setGreeting('Good afternoon');
    else setGreeting('Good evening');
  }, []);

  const level = user ? calculateLevel(user.points) : 1;

  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-900 relative overflow-hidden">
      <div className="absolute inset-0 bg-grid dark:bg-grid-dark pointer-events-none" />
      <div className="absolute top-0 -left-40 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute top-1/3 -right-40 w-80 h-80 bg-secondary-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-1/3 w-96 h-96 bg-accent-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={staggerContainer}
          className="space-y-8"
        >
          <motion.div variants={fadeUp} className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <motion.h1 className="text-3xl sm:text-4xl font-extrabold text-surface-900 dark:text-surface-50 tracking-tight">
                {greeting}, {user?.name || 'Learner'}!
                <span className="inline-block ml-2 animate-float">👋</span>
              </motion.h1>
              <motion.p className="text-surface-400 mt-2 text-base">
                Here&apos;s your learning progress today
              </motion.p>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2.5 rounded-2xl bg-gradient-to-r from-primary-500/10 to-secondary-500/10 px-5 py-2.5 border border-primary-200/30 dark:border-primary-700/30 backdrop-blur-sm">
                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-gradient-to-br from-primary-500 to-secondary-500 shadow-lg shadow-primary-500/20">
                  <Zap className="h-3.5 w-3.5 text-white" />
                </div>
                <div>
                  <span className="text-xs text-surface-400 font-medium">Points</span>
                  <span className="block text-sm font-bold text-surface-700 dark:text-surface-300 leading-none">
                    {user?.points || 0}
                  </span>
                </div>
              </div>
              <div className="flex items-center gap-2.5 rounded-2xl bg-gradient-to-r from-accent-500/10 to-orange-500/10 px-5 py-2.5 border border-accent-200/30 dark:border-accent-700/30 backdrop-blur-sm">
                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-gradient-to-br from-accent-500 to-orange-500 shadow-lg shadow-accent-500/20">
                  <Award className="h-3.5 w-3.5 text-white" />
                </div>
                <div>
                  <span className="text-xs text-surface-400 font-medium">Level</span>
                  <span className="block text-sm font-bold text-surface-700 dark:text-surface-300 leading-none">
                    {level}
                  </span>
                </div>
              </div>
            </div>
          </motion.div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <motion.div variants={fadeUp} custom={0}>
              <StatsCard
                icon={<FileQuestion className="h-5 w-5" />}
                label="Total Quizzes"
                value={42}
                gradient="from-primary-500 to-blue-500"
                trend={{ value: 12, positive: true }}
              />
            </motion.div>
            <motion.div variants={fadeUp} custom={1}>
              <StatsCard
                icon={<BarChart3 className="h-5 w-5" />}
                label="Average Score"
                value={78}
                suffix="%"
                gradient="from-secondary-500 to-purple-500"
                trend={{ value: 5, positive: true }}
              />
            </motion.div>
            <motion.div variants={fadeUp} custom={2}>
              <StatsCard
                icon={<BookOpen className="h-5 w-5" />}
                label="Lessons Done"
                value={18}
                gradient="from-accent-500 to-orange-500"
                trend={{ value: 3, positive: true }}
              />
            </motion.div>
            <motion.div variants={fadeUp} custom={3}>
              <StatsCard
                icon={<Flame className="h-5 w-5" />}
                label="Streak Days"
                value={7}
                gradient="from-red-500 to-pink-500"
                trend={{ value: 2, positive: true }}
              />
            </motion.div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-6">
              <motion.div
                variants={fadeUp}
                custom={4}
                className="rounded-2xl bg-white/80 dark:bg-surface-800/80 backdrop-blur-sm border border-surface-200/50 dark:border-surface-700/50 p-6 shadow-sm"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary-500/10 to-secondary-500/10">
                      <TrendingUp className="h-4 w-4 text-primary-600 dark:text-primary-400" />
                    </div>
                    <h2 className="text-base font-bold text-surface-900 dark:text-surface-50">
                      Weekly Scores
                    </h2>
                  </div>
                  <span className="text-xs font-medium text-surface-400 bg-surface-100 dark:bg-surface-700/50 px-3 py-1 rounded-full">
                    This week
                  </span>
                </div>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={chartData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                      <defs>
                        <linearGradient id="scoreGradient" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                          <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" className="dark:opacity-20" vertical={false} />
                      <XAxis dataKey="day" tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                      <YAxis domain={[0, 100]} tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                      <Tooltip
                        contentStyle={{
                          borderRadius: '12px',
                          border: '1px solid rgba(226,232,240,0.5)',
                          background: 'rgba(255,255,255,0.95)',
                          backdropFilter: 'blur(8px)',
                          boxShadow: '0 8px 24px rgba(0,0,0,0.08)',
                        }}
                        formatter={(value: number) => [`${value}%`, 'Score']}
                      />
                      <Area type="monotone" dataKey="score" stroke="none" fill="url(#scoreGradient)" />
                      <Line
                        type="monotone"
                        dataKey="score"
                        stroke="#6366f1"
                        strokeWidth={3}
                        dot={{ fill: '#6366f1', strokeWidth: 2, r: 4, stroke: '#fff' }}
                        activeDot={{ r: 7, fill: '#6366f1', strokeWidth: 3, stroke: '#fff' }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </motion.div>

              <motion.div variants={fadeUp} custom={5}>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-accent-500/10 to-orange-500/10">
                      <Sparkles className="h-4 w-4 text-accent-600 dark:text-accent-400" />
                    </div>
                    <h2 className="text-base font-bold text-surface-900 dark:text-surface-50">
                      Continue Learning
                    </h2>
                  </div>
                  <button
                    className="text-xs font-semibold text-primary-500 hover:text-primary-600 flex items-center gap-1 bg-primary-500/5 hover:bg-primary-500/10 px-3 py-1.5 rounded-full transition-colors"
                    aria-label="View all quizzes"
                  >
                    View all <ChevronRight className="h-3 w-3" />
                  </button>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {recommendedQuizzes.map((quiz) => (
                    <QuizCard key={quiz.id} {...quiz} />
                  ))}
                </div>
              </motion.div>
            </div>

            <div className="space-y-6">
              <motion.div
                variants={fadeUp}
                custom={6}
                className="rounded-2xl bg-white/80 dark:bg-surface-800/80 backdrop-blur-sm border border-surface-200/50 dark:border-surface-700/50 p-6 shadow-sm"
              >
                <div className="flex items-center gap-2.5 mb-5">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-red-500/10 to-pink-500/10">
                    <Target className="h-4 w-4 text-red-500" />
                  </div>
                  <h2 className="text-base font-bold text-surface-900 dark:text-surface-50">
                    Weak Topics
                  </h2>
                </div>
                <div className="space-y-3">
                  {weakTopics.map((topic, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.15, duration: 0.4 }}
                      className="p-4 rounded-xl bg-surface-50 dark:bg-surface-700/30 border border-surface-100 dark:border-surface-700/30"
                    >
                      <div className="flex items-center justify-between mb-1.5">
                        <span className="text-xs font-semibold text-surface-400 uppercase tracking-wide">{topic.subject}</span>
                        <div className="flex items-center gap-1">
                          <AlertTriangle className="h-3 w-3 text-danger-400" />
                          <span className="text-xs font-bold text-danger-500">{topic.score}%</span>
                        </div>
                      </div>
                      <p className="text-sm font-semibold text-surface-900 dark:text-surface-50 mb-3">
                        {topic.topic}
                      </p>
                      <div className="h-2 rounded-full bg-surface-200 dark:bg-surface-600 overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${topic.score}%` }}
                          transition={{ duration: 0.8, delay: i * 0.2, ease: 'easeOut' }}
                          className={cn(
                            'h-full rounded-full bg-gradient-to-r',
                            topic.color,
                            'relative'
                          )}
                        >
                          <div className="absolute inset-0 bg-white/20 rounded-full animate-pulse-slow" />
                        </motion.div>
                      </div>
                    </motion.div>
                  ))}
                </div>
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="mt-4 w-full text-center text-xs font-semibold text-white bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-600 hover:to-secondary-600 py-2.5 rounded-xl shadow-lg shadow-primary-500/20 transition-all"
                  aria-label="Practice weak topics"
                >
                  Practice these topics
                </motion.button>
              </motion.div>

              <motion.div
                variants={fadeUp}
                custom={7}
                className="rounded-2xl bg-white/80 dark:bg-surface-800/80 backdrop-blur-sm border border-surface-200/50 dark:border-surface-700/50 p-6 shadow-sm"
              >
                <div className="flex items-center gap-2.5 mb-5">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary-500/10 to-blue-500/10">
                    <Clock className="h-4 w-4 text-primary-600 dark:text-primary-400" />
                  </div>
                  <h2 className="text-base font-bold text-surface-900 dark:text-surface-50">
                    Recent Activity
                  </h2>
                </div>
                <div className="space-y-2">
                  {recentActivity.map((activity, i) => (
                    <motion.div
                      key={activity.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.08, duration: 0.3 }}
                      className="flex items-center gap-3 p-3 rounded-xl hover:bg-surface-50 dark:hover:bg-surface-700/30 transition-all cursor-pointer group/item"
                    >
                      <div
                        className={cn(
                          'flex h-9 w-9 items-center justify-center rounded-xl transition-transform group-hover/item:scale-110',
                          activity.score >= 80
                            ? 'bg-success-500/10 text-success-600 dark:text-success-400'
                            : activity.score >= 50
                            ? 'bg-accent-500/10 text-accent-600 dark:text-accent-400'
                            : 'bg-danger-500/10 text-danger-600 dark:text-danger-400'
                        )}
                      >
                        {activity.score >= 80 ? (
                          <CheckCircle2 className="h-4 w-4" />
                        ) : (
                          <XCircle className="h-4 w-4" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-semibold text-surface-900 dark:text-surface-50 truncate">
                          {activity.title}
                        </p>
                        <p className="text-xs text-surface-400 mt-0.5">
                          {activity.subject} &middot; {activity.date}
                        </p>
                      </div>
                      <div className={cn(
                        'text-sm font-bold',
                        activity.score >= 80
                          ? 'text-success-500'
                          : activity.score >= 50
                          ? 'text-accent-500'
                          : 'text-danger-500'
                      )}>
                        {activity.score}%
                      </div>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}


