'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { cn, calculateLevel } from '@/lib/utils';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import ProgressBar from '@/components/ui/ProgressBar';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from 'recharts';
import {
  BarChart3,
  TrendingUp,
  Calendar,
  Target,
  Download,
  Brain,
  AlertTriangle,
  ArrowRight,
  Sparkles,
  Clock,
  BookOpen,
  Zap,
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

const scoreTrend = [
  { month: 'Jan', score: 55 },
  { month: 'Feb', score: 62 },
  { month: 'Mar', score: 58 },
  { month: 'Apr', score: 70 },
  { month: 'May', score: 68 },
  { month: 'Jun', score: 78 },
  { month: 'Jul', score: 82 },
  { month: 'Aug', score: 75 },
  { month: 'Sep', score: 85 },
  { month: 'Oct', score: 88 },
  { month: 'Nov', score: 84 },
  { month: 'Dec', score: 90 },
];

const subjectPerformance = [
  { subject: 'Mathematics', score: 82, color: '#6366f1' },
  { subject: 'English', score: 75, color: '#22c55e' },
  { subject: 'Science', score: 65, color: '#f97316' },
  { subject: 'Social Studies', score: 70, color: '#d946ef' },
  { subject: 'Music', score: 90, color: '#14b8a6' },
  { subject: 'Art & Craft', score: 85, color: '#eab308' },
];

const weakTopics = [
  { topic: 'Verb Tenses', subject: 'English', score: 45, suggestion: 'Practice with daily grammar exercises and verb conjugation drills.' },
  { topic: 'Chemical Reactions', subject: 'Science', score: 48, suggestion: 'Review the periodic table and practice balancing chemical equations.' },
  { topic: 'Long Division', subject: 'Mathematics', score: 52, suggestion: 'Work on step-by-step division problems with remainders.' },
  { topic: 'Map Reading', subject: 'Social Studies', score: 55, suggestion: 'Practice with different types of maps and scale calculations.' },
];

const heatmapData = Array.from({ length: 28 }, (_, i) => ({
  day: i + 1,
  value: Math.floor(Math.random() * 5),
}));

const dateRanges = [
  { id: '7d', label: '7 days' },
  { id: '30d', label: '30 days' },
  { id: '90d', label: '90 days' },
];

export default function AnalyticsPage() {
  const [dateRange, setDateRange] = useState('30d');

  const avgScore = 78;
  const quizzesTaken = 42;
  const studyTime = 28;
  const level = 5;

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
              <h1 className="text-2xl sm:text-3xl font-bold text-surface-900 dark:text-surface-50">
                Analytics
              </h1>
              <p className="text-surface-500 mt-1">
                Track your learning progress and performance
              </p>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex gap-1 p-1 rounded-lg bg-surface-100 dark:bg-surface-800">
                {dateRanges.map((dr) => (
                  <button
                    key={dr.id}
                    onClick={() => setDateRange(dr.id)}
                    className={cn(
                      'px-3 py-1.5 rounded-md text-xs font-medium transition-all',
                      dateRange === dr.id
                        ? 'bg-white dark:bg-surface-700 text-surface-900 dark:text-surface-50 shadow-sm'
                        : 'text-surface-500 hover:text-surface-700 dark:hover:text-surface-300'
                    )}
                    aria-label={dr.label}
                  >
                    {dr.label}
                  </button>
                ))}
              </div>
              <Button variant="outline" size="sm" icon={<Download className="h-4 w-4" />}>
                Export
              </Button>
            </div>
          </motion.div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <motion.div variants={fadeUp} custom={0} className="p-5 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
              <div className="flex items-center gap-3 mb-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary-50 dark:bg-primary-500/10 text-primary-500">
                  <BarChart3 className="h-5 w-5" />
                </div>
              </div>
              <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">{avgScore}%</p>
              <p className="text-xs text-surface-500 mt-1">Average Score</p>
            </motion.div>
            <motion.div variants={fadeUp} custom={1} className="p-5 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
              <div className="flex items-center gap-3 mb-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-secondary-50 dark:bg-secondary-500/10 text-secondary-500">
                  <BookOpen className="h-5 w-5" />
                </div>
              </div>
              <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">{quizzesTaken}</p>
              <p className="text-xs text-surface-500 mt-1">Quizzes Taken</p>
            </motion.div>
            <motion.div variants={fadeUp} custom={2} className="p-5 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
              <div className="flex items-center gap-3 mb-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-accent-50 dark:bg-accent-500/10 text-accent-500">
                  <Clock className="h-5 w-5" />
                </div>
              </div>
              <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">{studyTime}h</p>
              <p className="text-xs text-surface-500 mt-1">Study Time</p>
            </motion.div>
            <motion.div variants={fadeUp} custom={3} className="p-5 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
              <div className="flex items-center gap-3 mb-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-success-50 dark:bg-success-500/10 text-success-500">
                  <Zap className="h-5 w-5" />
                </div>
              </div>
              <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">{level}</p>
              <p className="text-xs text-surface-500 mt-1">Current Level</p>
            </motion.div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <motion.div
              variants={fadeUp}
              custom={4}
              className="lg:col-span-2 p-5 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700"
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold text-surface-900 dark:text-surface-50">
                  Score Trend
                </h2>
                <TrendingUp className="h-4 w-4 text-success-500" />
              </div>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={scoreTrend}>
                    <defs>
                      <linearGradient id="scoreGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" className="dark:opacity-20" />
                    <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                    <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                    <Tooltip
                      contentStyle={{
                        borderRadius: '10px',
                        border: '1px solid #e2e8f0',
                        background: 'rgba(255,255,255,0.95)',
                      }}
                      formatter={(value: number) => [`${value}%`, 'Score']}
                    />
                    <Area type="monotone" dataKey="score" stroke="#6366f1" strokeWidth={2.5} fill="url(#scoreGradient)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </motion.div>

            <motion.div
              variants={fadeUp}
              custom={5}
              className="p-5 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700"
            >
              <h2 className="text-sm font-semibold text-surface-900 dark:text-surface-50 mb-4">
                Subject Performance
              </h2>
              <div className="space-y-4">
                {subjectPerformance.map((s) => (
                  <div key={s.subject}>
                    <div className="flex items-center justify-between text-xs mb-1.5">
                      <span className="text-surface-600 dark:text-surface-400">{s.subject}</span>
                      <span className="font-medium text-surface-900 dark:text-surface-50">{s.score}%</span>
                    </div>
                    <div className="h-2 rounded-full bg-surface-100 dark:bg-surface-700 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${s.score}%` }}
                        transition={{ duration: 0.8, ease: 'easeOut' }}
                        className="h-full rounded-full"
                        style={{ backgroundColor: s.color }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <motion.div
              variants={fadeUp}
              custom={6}
              className="p-5 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700"
            >
              <div className="flex items-center gap-2 mb-4">
                <AlertTriangle className="h-4 w-4 text-danger-500" />
                <h2 className="text-sm font-semibold text-surface-900 dark:text-surface-50">
                  Weakest Topics
                </h2>
              </div>
              <div className="space-y-3">
                {weakTopics.map((t, i) => (
                  <div key={i} className="p-3 rounded-lg bg-surface-50 dark:bg-surface-700/50">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-xs text-surface-500">{t.subject}</span>
                      <Badge variant="danger" size="sm">{t.score}%</Badge>
                    </div>
                    <p className="text-sm font-medium text-surface-900 dark:text-surface-50 mb-1">
                      {t.topic}
                    </p>
                    <p className="text-xs text-surface-500">{t.suggestion}</p>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div
              variants={fadeUp}
              custom={7}
              className="p-5 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700"
            >
              <div className="flex items-center gap-2 mb-4">
                <Calendar className="h-4 w-4 text-primary-500" />
                <h2 className="text-sm font-semibold text-surface-900 dark:text-surface-50">
                  Weekly Activity
                </h2>
              </div>
              <div className="grid grid-cols-7 gap-1.5">
                {heatmapData.map((d, i) => (
                  <div
                    key={i}
                    className={cn(
                      'aspect-square rounded-md',
                      d.value === 0 ? 'bg-surface-100 dark:bg-surface-700' :
                      d.value === 1 ? 'bg-primary-200 dark:bg-primary-800' :
                      d.value === 2 ? 'bg-primary-300 dark:bg-primary-700' :
                      d.value === 3 ? 'bg-primary-400 dark:bg-primary-600' :
                      'bg-primary-500'
                    )}
                    title={`Day ${d.day}: ${d.value} activities`}
                  />
                ))}
              </div>
              <div className="flex items-center justify-end gap-1.5 mt-3">
                <span className="text-xs text-surface-400">Less</span>
                {[0, 1, 2, 3, 4].map((v) => (
                  <div key={v} className={cn(
                    'h-3 w-3 rounded-sm',
                    v === 0 ? 'bg-surface-100 dark:bg-surface-700' :
                    v === 1 ? 'bg-primary-200 dark:bg-primary-800' :
                    v === 2 ? 'bg-primary-300 dark:bg-primary-700' :
                    v === 3 ? 'bg-primary-400 dark:bg-primary-600' :
                    'bg-primary-500'
                  )} />
                ))}
                <span className="text-xs text-surface-400">More</span>
              </div>

              <div className="mt-6 p-4 rounded-xl bg-gradient-to-r from-primary-500/10 to-secondary-500/10 border border-primary-200/30 dark:border-primary-700/30">
                <div className="flex items-center gap-2 mb-2">
                  <Sparkles className="h-4 w-4 text-accent-500" />
                  <h3 className="text-sm font-semibold text-surface-900 dark:text-surface-50">
                    Prediction
                  </h3>
                </div>
                <p className="text-sm text-surface-600 dark:text-surface-400">
                  On your current track, you&apos;ll reach <strong className="text-primary-500">Level {level + 3}</strong> by the end of the month. Keep up the great work!
                </p>
                <Button variant="ghost" size="sm" className="mt-3" icon={<ArrowRight className="h-3.5 w-3.5" />} iconPosition="right">
                  View study plan
                </Button>
              </div>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
