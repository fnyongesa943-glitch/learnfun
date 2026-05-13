'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import Badge from '@/components/ui/Badge';
import { Search, BookOpen, Calculator, Beaker, Globe, Music, Palette, Sparkles, Clock, HelpCircle, Play, Filter, SlidersHorizontal } from 'lucide-react';

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: i * 0.08, ease: 'easeOut' },
  }),
};

const staggerContainer = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08 } },
};

const subjects = [
  { id: 'all', label: 'All', icon: Sparkles },
  { id: 'mathematics', label: 'Mathematics', icon: Calculator },
  { id: 'english', label: 'English', icon: BookOpen },
  { id: 'science', label: 'Science', icon: Beaker },
  { id: 'social-studies', label: 'Social Studies', icon: Globe },
  { id: 'music', label: 'Music', icon: Music },
  { id: 'art', label: 'Art & Craft', icon: Palette },
];

const difficulties = ['All', 'Easy', 'Medium', 'Hard'];

const grades = ['All', 'PP1', 'PP2', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'];

const allQuizzes = [
  { id: '1', title: 'Fractions & Decimals', subject: 'Mathematics', difficulty: 'medium', questions: 15, time: 20, attempted: true, score: 85 },
  { id: '2', title: 'Parts of Speech', subject: 'English', difficulty: 'easy', questions: 10, time: 15, attempted: false },
  { id: '3', title: 'Photosynthesis', subject: 'Science', difficulty: 'hard', questions: 20, time: 25, attempted: true, score: 60 },
  { id: '4', title: 'Addition & Subtraction', subject: 'Mathematics', difficulty: 'easy', questions: 12, time: 15, attempted: true, score: 95 },
  { id: '5', title: 'Grammar Basics', subject: 'English', difficulty: 'medium', questions: 15, time: 20, attempted: true, score: 70 },
  { id: '6', title: 'Human Body Systems', subject: 'Science', difficulty: 'medium', questions: 18, time: 22, attempted: false },
  { id: '7', title: 'East African Geography', subject: 'Social Studies', difficulty: 'medium', questions: 14, time: 18, attempted: false },
  { id: '8', title: 'Multiplication Tables', subject: 'Mathematics', difficulty: 'easy', questions: 20, time: 25, attempted: true, score: 100 },
  { id: '9', title: 'Creative Writing', subject: 'English', difficulty: 'hard', questions: 8, time: 30, attempted: false },
  { id: '10', title: 'Solar System', subject: 'Science', difficulty: 'easy', questions: 12, time: 15, attempted: true, score: 90 },
  { id: '11', title: 'Musical Notes', subject: 'Music', difficulty: 'medium', questions: 10, time: 12, attempted: false },
  { id: '12', title: 'Color Theory', subject: 'Art & Craft', difficulty: 'easy', questions: 8, time: 10, attempted: false },
];

const subjectIcons: Record<string, React.ReactNode> = {
  Mathematics: <Calculator className="h-4 w-4" />,
  English: <BookOpen className="h-4 w-4" />,
  Science: <Beaker className="h-4 w-4" />,
  'Social Studies': <Globe className="h-4 w-4" />,
  Music: <Music className="h-4 w-4" />,
  'Art & Craft': <Palette className="h-4 w-4" />,
};

export default function QuizzesPage() {
  const [search, setSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [activeSubject, setActiveSubject] = useState('all');
  const [activeDifficulty, setActiveDifficulty] = useState('All');
  const [activeGrade, setActiveGrade] = useState('All');
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(search), 300);
    return () => clearTimeout(timer);
  }, [search]);

  const filtered = allQuizzes.filter((q) => {
    const matchSearch = q.title.toLowerCase().includes(debouncedSearch.toLowerCase());
    const matchSubject = activeSubject === 'all' || q.subject.toLowerCase() === activeSubject;
    const matchDifficulty = activeDifficulty === 'All' || q.difficulty === activeDifficulty.toLowerCase();
    return matchSearch && matchSubject && matchDifficulty;
  });

  const getDiffVariant = (d: string) => {
    if (d === 'easy') return 'success' as const;
    if (d === 'medium') return 'warning' as const;
    return 'danger' as const;
  };

  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={staggerContainer}
          className="space-y-6"
        >
          <motion.div variants={fadeUp}>
            <h1 className="text-2xl sm:text-3xl font-bold text-surface-900 dark:text-surface-50">
              Explore Quizzes
            </h1>
            <p className="text-surface-500 mt-1">
              Choose a subject and test your knowledge
            </p>
          </motion.div>

          <motion.div variants={fadeUp} className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-surface-400" />
              <input
                type="text"
                placeholder="Search quizzes..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 text-sm text-surface-900 dark:text-surface-50 placeholder:text-surface-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                aria-label="Search quizzes"
              />
            </div>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 text-sm font-medium text-surface-600 dark:text-surface-400 hover:bg-surface-50 dark:hover:bg-surface-700 transition-colors"
              aria-label="Toggle filters"
            >
              <SlidersHorizontal className="h-4 w-4" />
              Filters
            </button>
          </motion.div>

          <motion.div variants={fadeUp} className="flex gap-2 overflow-x-auto pb-2 scrollbar-none">
            {subjects.map((subject) => {
              const Icon = subject.icon;
              return (
                <button
                  key={subject.id}
                  onClick={() => setActiveSubject(subject.id)}
                  className={cn(
                    'flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium whitespace-nowrap transition-all duration-200 border',
                    activeSubject === subject.id
                      ? 'bg-primary-500 text-white border-primary-500 shadow-sm'
                      : 'bg-white dark:bg-surface-800 text-surface-600 dark:text-surface-400 border-surface-200 dark:border-surface-700 hover:bg-surface-50 dark:hover:bg-surface-700'
                  )}
                  aria-label={`Filter by ${subject.label}`}
                >
                  <Icon className="h-4 w-4" />
                  {subject.label}
                </button>
              );
            })}
          </motion.div>

          {showFilters && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex flex-wrap gap-4 p-4 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700"
            >
              <div>
                <label className="block text-xs font-medium text-surface-500 mb-1.5">Grade</label>
                <select
                  value={activeGrade}
                  onChange={(e) => setActiveGrade(e.target.value)}
                  className="px-3 py-1.5 rounded-lg bg-surface-50 dark:bg-surface-700 border border-surface-200 dark:border-surface-600 text-sm text-surface-900 dark:text-surface-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  aria-label="Select grade"
                >
                  {grades.map((g) => (
                    <option key={g} value={g}>{g}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium text-surface-500 mb-1.5">Difficulty</label>
                <div className="flex gap-1.5">
                  {difficulties.map((d) => (
                    <button
                      key={d}
                      onClick={() => setActiveDifficulty(d)}
                      className={cn(
                        'px-3 py-1.5 rounded-lg text-xs font-medium transition-colors',
                        activeDifficulty === d
                          ? 'bg-primary-500 text-white'
                          : 'bg-surface-50 dark:bg-surface-700 text-surface-600 dark:text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-600'
                      )}
                      aria-label={`Filter ${d} difficulty`}
                    >
                      {d}
                    </button>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {filtered.length === 0 ? (
            <motion.div
              variants={fadeUp}
              className="flex flex-col items-center justify-center py-20 text-center"
            >
              <Search className="h-16 w-16 text-surface-300 dark:text-surface-600 mb-4" />
              <h3 className="text-lg font-semibold text-surface-900 dark:text-surface-50 mb-2">
                No quizzes found
              </h3>
              <p className="text-sm text-surface-500 max-w-sm">
                Try adjusting your search or filters to find what you&apos;re looking for.
              </p>
              <button
                onClick={() => { setSearch(''); setActiveSubject('all'); setActiveDifficulty('All'); }}
                className="mt-4 text-sm font-medium text-primary-500 hover:text-primary-600"
                aria-label="Clear filters"
              >
                Clear all filters
              </button>
            </motion.div>
          ) : (
            <motion.div
              variants={staggerContainer}
              className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
            >
              {filtered.map((quiz, i) => (
                <motion.div
                  key={quiz.id}
                  variants={fadeUp}
                  custom={i}
                  className="group relative overflow-hidden rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 shadow-sm hover:shadow-md transition-shadow"
                >
                  <div className={cn(
                    'h-1.5 w-full',
                    quiz.difficulty === 'easy' ? 'bg-success-500' : quiz.difficulty === 'medium' ? 'bg-accent-500' : 'bg-danger-500'
                  )} />
                  <div className="p-5">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-surface-100 dark:bg-surface-700 text-surface-600 dark:text-surface-400">
                        {subjectIcons[quiz.subject]}
                      </span>
                      <span className="text-xs font-medium text-surface-500">{quiz.subject}</span>
                    </div>

                    <h3 className="text-sm font-semibold text-surface-900 dark:text-surface-50 mb-3 line-clamp-2">
                      {quiz.title}
                    </h3>

                    <div className="flex items-center flex-wrap gap-2 mb-4">
                      <Badge variant={getDiffVariant(quiz.difficulty)} size="sm">
                        {quiz.difficulty}
                      </Badge>
                      <span className="flex items-center gap-1 text-xs text-surface-400">
                        <HelpCircle className="h-3 w-3" />
                        {quiz.questions}
                      </span>
                      <span className="flex items-center gap-1 text-xs text-surface-400">
                        <Clock className="h-3 w-3" />
                        {quiz.time}min
                      </span>
                    </div>

                    {quiz.attempted && quiz.score !== undefined && (
                      <div className="mb-3">
                        <div className="flex items-center justify-between text-xs mb-1">
                          <span className="text-surface-400">Best score</span>
                          <span className={cn('font-medium', quiz.score >= 80 ? 'text-success-500' : quiz.score >= 50 ? 'text-accent-500' : 'text-danger-500')}>
                            {quiz.score}%
                          </span>
                        </div>
                        <div className="h-1.5 rounded-full bg-surface-100 dark:bg-surface-700 overflow-hidden">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${quiz.score}%` }}
                            transition={{ duration: 0.8, ease: 'easeOut' }}
                            className={cn('h-full rounded-full', quiz.score >= 80 ? 'bg-success-500' : quiz.score >= 50 ? 'bg-accent-500' : 'bg-danger-500')}
                          />
                        </div>
                      </div>
                    )}

                    <a
                      href={`/quizzes/${quiz.id}`}
                      className="inline-flex items-center gap-1.5 mt-2 text-xs font-medium text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors"
                      aria-label={`Start quiz: ${quiz.title}`}
                    >
                      <Play className="h-3.5 w-3.5" />
                      {quiz.attempted ? 'Retry' : 'Start Quiz'}
                    </a>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
