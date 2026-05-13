'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import Button from '@/components/ui/Button';
import ProgressBar from '@/components/ui/ProgressBar';
import {
  ChevronLeft,
  ChevronRight,
  CheckCircle2,
  Lightbulb,
  BookOpen,
  Sparkles,
  GraduationCap,
  ArrowRight,
  ListChecks,
  Beaker,
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

export default function LessonViewerPage() {
  const router = useRouter();
  const [completed, setCompleted] = useState(false);

  const handleComplete = () => {
    setCompleted(true);
  };

  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-900">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 py-8">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={staggerContainer}
          className="space-y-8"
        >
          <motion.div variants={fadeUp}>
            <nav className="flex items-center gap-2 text-sm text-surface-400 mb-4" aria-label="Breadcrumb">
              <button onClick={() => router.push('/lessons')} className="hover:text-surface-600 dark:hover:text-surface-300 transition-colors">
                Lessons
              </button>
              <ChevronRight className="h-3.5 w-3.5" />
              <span className="text-surface-500">Grade 1</span>
              <ChevronRight className="h-3.5 w-3.5" />
              <span className="text-surface-500">Mathematics</span>
              <ChevronRight className="h-3.5 w-3.5" />
              <span className="text-surface-900 dark:text-surface-50 font-medium">Addition Basics</span>
            </nav>

            <div className="flex items-center gap-3 mb-2">
              <span className="text-3xl">📐</span>
              <h1 className="text-2xl sm:text-3xl font-bold text-surface-900 dark:text-surface-50">
                Addition Basics
              </h1>
            </div>
            <p className="text-surface-500">
              Learn how to add numbers together with simple examples and fun exercises.
            </p>
          </motion.div>

          <motion.div variants={fadeUp}>
            <ProgressBar value={completed ? 100 : 35} max={100} size="md" label />
          </motion.div>

          <motion.div
            variants={fadeUp}
            className="prose prose-surface dark:prose-invert max-w-none space-y-6"
          >
            <section className="rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 p-6">
              <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50 flex items-center gap-2 mb-4">
                <BookOpen className="h-5 w-5 text-primary-500" />
                What is Addition?
              </h2>
              <p className="text-surface-600 dark:text-surface-400 leading-relaxed">
                Addition is the process of finding the total or sum by combining two or more numbers.
                When we add, we put things together and count how many there are in total.
              </p>
              <div className="mt-4 p-4 rounded-lg bg-primary-50 dark:bg-primary-500/10 border border-primary-200 dark:border-primary-700/30">
                <p className="text-sm font-medium text-primary-700 dark:text-primary-400">
                  Example: 2 + 3 = 5
                </p>
                <p className="text-xs text-primary-600 dark:text-primary-400/80 mt-1">
                  This means &ldquo;2 things plus 3 things equals 5 things in total.&rdquo;
                </p>
              </div>
            </section>

            <section className="rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 p-6">
              <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50 flex items-center gap-2 mb-4">
                <ListChecks className="h-5 w-5 text-success-500" />
                Key Points
              </h2>
              <ul className="space-y-3">
                {[
                  'Addition combines two or more numbers to find the total (sum).',
                  'The plus sign (+) means we are adding numbers together.',
                  'The equals sign (=) shows the result of the addition.',
                  'Numbers can be added in any order and the sum stays the same.',
                  'Adding zero to any number leaves it unchanged.',
                ].map((point, i) => (
                  <li key={i} className="flex items-start gap-3 text-sm text-surface-600 dark:text-surface-400">
                    <CheckCircle2 className="h-4 w-4 text-success-500 mt-0.5 shrink-0" />
                    <span>{point}</span>
                  </li>
                ))}
              </ul>
            </section>

            <section className="rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 p-6">
              <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50 flex items-center gap-2 mb-4">
                <Beaker className="h-5 w-5 text-accent-500" />
                Examples
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {[
                  { q: '3 + 2 = ?', a: '5', explain: 'Count: 1, 2, 3... then 4, 5' },
                  { q: '5 + 1 = ?', a: '6', explain: 'Start at 5 and count 1 more' },
                  { q: '4 + 4 = ?', a: '8', explain: 'Double of 4 is 8' },
                  { q: '7 + 0 = ?', a: '7', explain: 'Adding zero does not change the number' },
                ].map((ex, i) => (
                  <div key={i} className="p-4 rounded-lg bg-surface-50 dark:bg-surface-700/50 border border-surface-200 dark:border-surface-700">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-lg font-bold text-primary-500">{ex.q}</span>
                      <span className="flex items-center gap-1 text-sm">
                        <ArrowRight className="h-3.5 w-3.5 text-surface-400" />
                        <span className="font-bold text-success-500 text-lg">{ex.a}</span>
                      </span>
                    </div>
                    <p className="text-xs text-surface-500">{ex.explain}</p>
                  </div>
                ))}
              </div>
            </section>

            <section className="rounded-xl bg-amber-50 dark:bg-amber-500/10 border border-amber-200 dark:border-amber-700/30 p-6">
              <div className="flex gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-amber-100 dark:bg-amber-500/20">
                  <Lightbulb className="h-5 w-5 text-amber-600 dark:text-amber-400" />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-amber-800 dark:text-amber-300 mb-2">
                    Did You Know?
                  </h3>
                  <p className="text-sm text-amber-700 dark:text-amber-400/80 leading-relaxed">
                    The word &ldquo;addition&rdquo; comes from the Latin word &ldquo;addere,&rdquo; which means
                    &ldquo;to add to.&rdquo; People have been adding numbers for thousands of years!
                    Ancient Egyptians used hieroglyphs to represent addition.
                  </p>
                </div>
              </div>
            </section>

            <section className="rounded-xl bg-blue-50 dark:bg-blue-500/10 border border-blue-200 dark:border-blue-700/30 p-6">
              <div className="flex gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-100 dark:bg-blue-500/20">
                  <BookOpen className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-blue-800 dark:text-blue-300 mb-2">
                    Definition
                  </h3>
                  <p className="text-sm text-blue-700 dark:text-blue-400/80 leading-relaxed">
                    <strong className="text-blue-800 dark:text-blue-300">Addition</strong> (noun): The mathematical
                    operation of combining two or more numbers to find their total or sum.
                    The result of addition is called the <strong className="text-blue-800 dark:text-blue-300">sum</strong>.
                  </p>
                </div>
              </div>
            </section>
          </motion.div>

          <motion.div variants={fadeUp} className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-surface-200 dark:border-surface-700">
            <Button variant="ghost" icon={<ChevronLeft className="h-4 w-4" />} onClick={() => router.back()}>
              Previous Lesson
            </Button>

            <div className="flex items-center gap-3">
              {!completed ? (
                <Button
                  variant="primary"
                  icon={<CheckCircle2 className="h-4 w-4" />}
                  iconPosition="right"
                  onClick={handleComplete}
                >
                  Mark Complete
                </Button>
              ) : (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-success-50 dark:bg-success-500/10 border border-success-200 dark:border-success-700/30"
                >
                  <CheckCircle2 className="h-4 w-4 text-success-500" />
                  <span className="text-sm font-medium text-success-600 dark:text-success-400">Completed!</span>
                </motion.div>
              )}
            </div>

            <Button variant="ghost" icon={<ChevronRight className="h-4 w-4" />} iconPosition="right" onClick={() => {}}>
              Next Lesson
            </Button>
          </motion.div>

          <motion.div
            variants={fadeUp}
            className="rounded-xl bg-gradient-to-r from-primary-500/10 to-secondary-500/10 border border-primary-200/30 dark:border-primary-700/30 p-5"
          >
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary-500 text-white">
                <GraduationCap className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <h3 className="text-sm font-semibold text-surface-900 dark:text-surface-50">
                  Ready to test your knowledge?
                </h3>
                <p className="text-xs text-surface-500">Take a quick quiz on what you&apos;ve learned</p>
              </div>
              <Button variant="primary" size="sm" icon={<ArrowRight className="h-4 w-4" />} iconPosition="right" onClick={() => router.push('/quizzes/1')}>
                Start Quiz
              </Button>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
