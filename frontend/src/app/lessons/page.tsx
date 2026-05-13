'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import { ChevronRight, BookOpen, Calculator, Beaker, Globe, Music, Palette, Sparkles, ArrowLeft } from 'lucide-react';

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

interface Grade {
  id: string;
  label: string;
  icon: React.ReactNode;
  color: string;
  bgColor: string;
  subjects: Subject[];
}

interface Subject {
  id: string;
  name: string;
  icon: React.ReactNode;
  color: string;
  topics: number;
  lessons: number;
  progress: number;
}

const grades: Grade[] = [
  {
    id: 'PP1', label: 'Pre-Primary 1', icon: <Sparkles className="h-6 w-6" />, color: 'from-emerald-400 to-emerald-600', bgColor: 'bg-emerald-50 dark:bg-emerald-500/10',
    subjects: [
      { id: 'pp1-eng', name: 'Language Activities', icon: <BookOpen className="h-4 w-4" />, color: 'text-blue-500', topics: 6, lessons: 24, progress: 75 },
      { id: 'pp1-math', name: 'Mathematical Activities', icon: <Calculator className="h-4 w-4" />, color: 'text-purple-500', topics: 5, lessons: 20, progress: 60 },
    ],
  },
  {
    id: 'PP2', label: 'Pre-Primary 2', icon: <Sparkles className="h-6 w-6" />, color: 'from-teal-400 to-teal-600', bgColor: 'bg-teal-50 dark:bg-teal-500/10',
    subjects: [
      { id: 'pp2-eng', name: 'Language Activities', icon: <BookOpen className="h-4 w-4" />, color: 'text-blue-500', topics: 6, lessons: 24, progress: 50 },
      { id: 'pp2-math', name: 'Mathematical Activities', icon: <Calculator className="h-4 w-4" />, color: 'text-purple-500', topics: 5, lessons: 20, progress: 30 },
    ],
  },
  {
    id: 'G1', label: 'Grade 1', icon: <BookOpen className="h-6 w-6" />, color: 'from-blue-400 to-blue-600', bgColor: 'bg-blue-50 dark:bg-blue-500/10',
    subjects: [
      { id: 'g1-eng', name: 'English', icon: <BookOpen className="h-4 w-4" />, color: 'text-blue-500', topics: 8, lessons: 32, progress: 40 },
      { id: 'g1-math', name: 'Mathematics', icon: <Calculator className="h-4 w-4" />, color: 'text-purple-500', topics: 7, lessons: 28, progress: 55 },
      { id: 'g1-sci', name: 'Science', icon: <Beaker className="h-4 w-4" />, color: 'text-green-500', topics: 5, lessons: 20, progress: 20 },
    ],
  },
  {
    id: 'G2', label: 'Grade 2', icon: <BookOpen className="h-6 w-6" />, color: 'from-cyan-400 to-cyan-600', bgColor: 'bg-cyan-50 dark:bg-cyan-500/10',
    subjects: [
      { id: 'g2-eng', name: 'English', icon: <BookOpen className="h-4 w-4" />, color: 'text-blue-500', topics: 8, lessons: 32, progress: 25 },
      { id: 'g2-math', name: 'Mathematics', icon: <Calculator className="h-4 w-4" />, color: 'text-purple-500', topics: 7, lessons: 28, progress: 35 },
    ],
  },
  {
    id: 'G3', label: 'Grade 3', icon: <BookOpen className="h-6 w-6" />, color: 'from-sky-400 to-sky-600', bgColor: 'bg-sky-50 dark:bg-sky-500/10',
    subjects: [
      { id: 'g3-eng', name: 'English', icon: <BookOpen className="h-4 w-4" />, color: 'text-blue-500', topics: 9, lessons: 36, progress: 10 },
      { id: 'g3-math', name: 'Mathematics', icon: <Calculator className="h-4 w-4" />, color: 'text-purple-500', topics: 8, lessons: 32, progress: 15 },
    ],
  },
  {
    id: 'G4', label: 'Grade 4', icon: <BookOpen className="h-6 w-6" />, color: 'from-indigo-400 to-indigo-600', bgColor: 'bg-indigo-50 dark:bg-indigo-500/10',
    subjects: [
      { id: 'g4-eng', name: 'English', icon: <BookOpen className="h-4 w-4" />, color: 'text-blue-500', topics: 10, lessons: 40, progress: 5 },
      { id: 'g4-math', name: 'Mathematics', icon: <Calculator className="h-4 w-4" />, color: 'text-purple-500', topics: 9, lessons: 36, progress: 8 },
      { id: 'g4-sci', name: 'Science', icon: <Beaker className="h-4 w-4" />, color: 'text-green-500', topics: 7, lessons: 28, progress: 12 },
    ],
  },
  {
    id: 'G5', label: 'Grade 5', icon: <BookOpen className="h-6 w-6" />, color: 'from-violet-400 to-violet-600', bgColor: 'bg-violet-50 dark:bg-violet-500/10',
    subjects: [
      { id: 'g5-eng', name: 'English', icon: <BookOpen className="h-4 w-4" />, color: 'text-blue-500', topics: 10, lessons: 40, progress: 0 },
      { id: 'g5-math', name: 'Mathematics', icon: <Calculator className="h-4 w-4" />, color: 'text-purple-500', topics: 9, lessons: 36, progress: 0 },
    ],
  },
  {
    id: 'G6', label: 'Grade 6', icon: <BookOpen className="h-6 w-6" />, color: 'from-purple-400 to-purple-600', bgColor: 'bg-purple-50 dark:bg-purple-500/10',
    subjects: [
      { id: 'g6-eng', name: 'English', icon: <BookOpen className="h-4 w-4" />, color: 'text-blue-500', topics: 11, lessons: 44, progress: 0 },
      { id: 'g6-math', name: 'Mathematics', icon: <Calculator className="h-4 w-4" />, color: 'text-purple-500', topics: 10, lessons: 40, progress: 0 },
      { id: 'g6-sci', name: 'Science', icon: <Beaker className="h-4 w-4" />, color: 'text-green-500', topics: 8, lessons: 32, progress: 0 },
    ],
  },
  {
    id: 'G7', label: 'Grade 7', icon: <Globe className="h-6 w-6" />, color: 'from-fuchsia-400 to-fuchsia-600', bgColor: 'bg-fuchsia-50 dark:bg-fuchsia-500/10',
    subjects: [
      { id: 'g7-eng', name: 'English', icon: <BookOpen className="h-4 w-4" />, color: 'text-blue-500', topics: 12, lessons: 48, progress: 0 },
      { id: 'g7-math', name: 'Mathematics', icon: <Calculator className="h-4 w-4" />, color: 'text-purple-500', topics: 11, lessons: 44, progress: 0 },
    ],
  },
  {
    id: 'G8', label: 'Grade 8', icon: <Globe className="h-6 w-6" />, color: 'from-pink-400 to-pink-600', bgColor: 'bg-pink-50 dark:bg-pink-500/10',
    subjects: [
      { id: 'g8-eng', name: 'English', icon: <BookOpen className="h-4 w-4" />, color: 'text-blue-500', topics: 12, lessons: 48, progress: 0 },
      { id: 'g8-math', name: 'Mathematics', icon: <Calculator className="h-4 w-4" />, color: 'text-purple-500', topics: 12, lessons: 48, progress: 0 },
    ],
  },
  {
    id: 'G9', label: 'Grade 9', icon: <Globe className="h-6 w-6" />, color: 'from-rose-400 to-rose-600', bgColor: 'bg-rose-50 dark:bg-rose-500/10',
    subjects: [
      { id: 'g9-eng', name: 'English', icon: <BookOpen className="h-4 w-4" />, color: 'text-blue-500', topics: 13, lessons: 52, progress: 0 },
      { id: 'g9-math', name: 'Mathematics', icon: <Calculator className="h-4 w-4" />, color: 'text-purple-500', topics: 12, lessons: 48, progress: 0 },
    ],
  },
];

export default function LessonsPage() {
  const [selectedGrade, setSelectedGrade] = useState<string | null>(null);
  const currentGrade = grades.find((g) => g.id === selectedGrade);

  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={staggerContainer}
          className="space-y-8"
        >
          <motion.div variants={fadeUp}>
            {selectedGrade ? (
              <div className="flex items-center gap-3 mb-2">
                <button
                  onClick={() => setSelectedGrade(null)}
                  className="flex items-center gap-1 text-sm text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 transition-colors"
                  aria-label="Back to grades"
                >
                  <ArrowLeft className="h-4 w-4" />
                  Back
                </button>
              </div>
            ) : null}
            <h1 className="text-2xl sm:text-3xl font-bold text-surface-900 dark:text-surface-50">
              {selectedGrade ? `${currentGrade?.label} Subjects` : 'Choose Your Grade'}
            </h1>
            <p className="text-surface-500 mt-1">
              {selectedGrade ? 'Select a subject to start learning' : 'Pick your grade to explore lessons'}
            </p>
          </motion.div>

          <AnimatePresence mode="wait">
            {!selectedGrade ? (
              <motion.div
                key="grades"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                variants={staggerContainer}
                className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4"
              >
                {grades.map((grade, i) => (
                  <motion.button
                    key={grade.id}
                    variants={fadeUp}
                    custom={i}
                    whileHover={{ y: -6, boxShadow: '0 12px 24px rgba(99,102,241,0.1)' }}
                    whileTap={{ scale: 0.97 }}
                    onClick={() => setSelectedGrade(grade.id)}
                    className={cn(
                      'flex flex-col items-center gap-3 p-6 rounded-xl border-2 transition-all duration-200',
                      'bg-white dark:bg-surface-800 border-surface-200 dark:border-surface-700 hover:border-primary-300 dark:hover:border-primary-600'
                    )}
                    aria-label={`Select ${grade.label}`}
                  >
                    <div className={cn(
                      'flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br text-white shadow-lg',
                      grade.color
                    )}>
                      {grade.icon}
                    </div>
                    <span className="text-sm font-semibold text-surface-900 dark:text-surface-50 text-center">
                      {grade.label}
                    </span>
                    <span className="text-xs text-surface-400">
                      {grade.subjects.length} subjects
                    </span>
                  </motion.button>
                ))}
              </motion.div>
            ) : (
              <motion.div
                key="subjects"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
              >
                {currentGrade?.subjects.map((subject, i) => (
                  <motion.a
                    key={subject.id}
                    href={`/lessons/${subject.id}`}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.1 }}
                    whileHover={{ y: -4, boxShadow: '0 12px 24px rgba(99,102,241,0.1)' }}
                    className="block p-6 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 shadow-sm"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className={cn(
                        'flex h-12 w-12 items-center justify-center rounded-xl bg-surface-100 dark:bg-surface-700',
                        subject.color
                      )}>
                        {subject.icon}
                      </div>
                      <span className={cn(
                        'text-xs font-medium px-2 py-1 rounded-full',
                        subject.progress === 100
                          ? 'bg-success-50 text-success-600 dark:bg-success-500/10'
                          : subject.progress > 0
                          ? 'bg-primary-50 text-primary-600 dark:bg-primary-500/10'
                          : 'bg-surface-100 text-surface-500 dark:bg-surface-700'
                      )}>
                        {subject.progress === 100 ? 'Completed' : subject.progress > 0 ? `${subject.progress}%` : 'Not started'}
                      </span>
                    </div>

                    <h3 className="text-base font-semibold text-surface-900 dark:text-surface-50 mb-1">
                      {subject.name}
                    </h3>
                    <p className="text-xs text-surface-400 mb-4">
                      {subject.topics} topics &middot; {subject.lessons} lessons
                    </p>

                    <div className="h-2 rounded-full bg-surface-100 dark:bg-surface-700 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${subject.progress}%` }}
                        transition={{ duration: 0.8, ease: 'easeOut', delay: i * 0.15 }}
                        className={cn(
                          'h-full rounded-full',
                          subject.progress === 100 ? 'bg-success-500' : 'bg-primary-500'
                        )}
                      />
                    </div>
                  </motion.a>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  );
}
