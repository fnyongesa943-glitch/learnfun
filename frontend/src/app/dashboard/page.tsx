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
} from 'lucide-react';

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
    <div className="min-h-screen bg-surface-50 dark:bg-surface-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={staggerContainer}
          className="space-y-8"
        >
          <motion.div variants={fadeUp} className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <motion.h1
                className="text-2xl sm:text-3xl font-bold text-surface-900 dark:text-surface-50"
              >
                {greeting}, {user?.name || 'Learner'}!
              </motion.h1>
              <motion.p className="text-surface-500 mt-1">
                Here&apos;s your learning progress today
              </motion.p>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-primary-500/10 to-secondary-500/10 px-4 py-2 border border-primary-200/30 dark:border-primary-700/30">
                <Zap className="h-4 w-4 text-accent-500" />
                <span className="text-sm font-medium text-surface-700 dark:text-surface-300">
                  {user?.points || 0} pts
                </span>
              </div>
              <div className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-accent-500/10 to-orange-500/10 px-4 py-2 border border-accent-200/30 dark:border-accent-700/30">
                <Award className="h-4 w-4 text-accent-500" />
                <span className="text-sm font-medium text-surface-700 dark:text-surface-300">
                  Level {level}
                </span>
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
                className="rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 p-5 shadow-sm"
              >
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-sm font-semibold text-surface-900 dark:text-surface-50">
                    Weekly Scores
                  </h2>
                  <span className="text-xs text-surface-400">This week</span>
                </div>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" className="dark:opacity-20" />
                      <XAxis dataKey="day" tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                      <YAxis domain={[0, 100]} tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                      <Tooltip
                        contentStyle={{
                          borderRadius: '10px',
                          border: '1px solid #e2e8f0',
                          background: 'rgba(255,255,255,0.95)',
                          boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                        }}
                        formatter={(value: number) => [`${value}%`, 'Score']}
                      />
                      <Line
                        type="monotone"
                        dataKey="score"
                        stroke="#6366f1"
                        strokeWidth={2.5}
                        dot={{ fill: '#6366f1', strokeWidth: 2, r: 4 }}
                        activeDot={{ r: 6, fill: '#6366f1' }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </motion.div>

              <motion.div variants={fadeUp} custom={5}>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-sm font-semibold text-surface-900 dark:text-surface-50">
                    Continue Learning
                  </h2>
                  <button
                    className="text-xs text-primary-500 hover:text-primary-600 font-medium flex items-center gap-1"
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
                className="rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 p-5 shadow-sm"
              >
                <div className="flex items-center gap-2 mb-4">
                  <Brain className="h-4 w-4 text-danger-500" />
                  <h2 className="text-sm font-semibold text-surface-900 dark:text-surface-50">
                    Weak Topics
                  </h2>
                </div>
                <div className="space-y-3">
                  {weakTopics.map((topic, i) => (
                    <div key={i} className="p-3 rounded-lg bg-surface-50 dark:bg-surface-700/50">
                      <div className="flex items-center justify-between mb-1.5">
                        <span className="text-xs text-surface-500">{topic.subject}</span>
                        <span className="text-xs font-medium text-danger-500">{topic.score}%</span>
                      </div>
                      <p className="text-sm font-medium text-surface-900 dark:text-surface-50 mb-2">
                        {topic.topic}
                      </p>
                      <div className="h-1.5 rounded-full bg-surface-200 dark:bg-surface-600 overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${topic.score}%` }}
                          transition={{ duration: 0.8, delay: i * 0.2 }}
                          className={`h-full rounded-full bg-gradient-to-r ${topic.color}`}
                        />
                      </div>
                    </div>
                  ))}
                </div>
                <button
                  className="mt-3 w-full text-center text-xs font-medium text-primary-500 hover:text-primary-600 py-2"
                  aria-label="Practice weak topics"
                >
                  Practice these topics
                </button>
              </motion.div>

              <motion.div
                variants={fadeUp}
                custom={7}
                className="rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 p-5 shadow-sm"
              >
                <div className="flex items-center gap-2 mb-4">
                  <Clock className="h-4 w-4 text-primary-500" />
                  <h2 className="text-sm font-semibold text-surface-900 dark:text-surface-50">
                    Recent Activity
                  </h2>
                </div>
                <div className="space-y-3">
                  {recentActivity.map((activity, i) => (
                    <div
                      key={activity.id}
                      className="flex items-center gap-3 p-2 rounded-lg hover:bg-surface-50 dark:hover:bg-surface-700/50 transition-colors"
                    >
                      <div
                        className={`flex h-8 w-8 items-center justify-center rounded-lg ${
                          activity.score >= 80
                            ? 'bg-success-50 text-success-600 dark:bg-success-500/10'
                            : activity.score >= 50
                            ? 'bg-accent-50 text-accent-600 dark:bg-accent-500/10'
                            : 'bg-danger-50 text-danger-600 dark:bg-danger-500/10'
                        }`}
                      >
                        {activity.score >= 80 ? (
                          <CheckCircle2 className="h-4 w-4" />
                        ) : (
                          <XCircle className="h-4 w-4" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-surface-900 dark:text-surface-50 truncate">
                          {activity.title}
                        </p>
                        <p className="text-xs text-surface-400">
                          {activity.subject} &middot; {activity.date}
                        </p>
                      </div>
                      <span
                        className={`text-xs font-semibold ${
                          activity.score >= 80
                            ? 'text-success-500'
                            : activity.score >= 50
                            ? 'text-accent-500'
                            : 'text-danger-500'
                        }`}
                      >
                        {activity.score}%
                      </span>
                    </div>
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
