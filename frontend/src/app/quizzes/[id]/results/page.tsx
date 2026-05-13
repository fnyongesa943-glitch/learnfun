'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useRouter, useSearchParams, useParams } from 'next/navigation';
import { motion, useMotionValue, useSpring, useTransform, AnimatePresence } from 'framer-motion';
import { cn, formatTime } from '@/lib/utils';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import { CheckCircle2, XCircle, RotateCcw, Trophy, ArrowRight, ChevronDown, ChevronUp, Star, Zap, Sparkles } from 'lucide-react';

const sampleReview = [
  { id: '1', text: 'What is 2/3 + 1/3?', options: ['1/3', '2/3', '1', '4/3'], correctAnswer: 2, userAnswer: 2, explanation: '2/3 + 1/3 = 3/3 = 1.' },
  { id: '2', text: 'Which of these is a proper fraction?', options: ['5/3', '3/4', '7/5', '9/8'], correctAnswer: 1, userAnswer: 3, explanation: 'A proper fraction has numerator less than denominator.' },
  { id: '3', text: 'What is 0.5 written as a fraction?', options: ['1/5', '1/4', '1/3', '1/2'], correctAnswer: 3, userAnswer: 3, explanation: '0.5 = 5/10 = 1/2.' },
  { id: '4', text: 'What is 25% of 80?', options: ['15', '20', '25', '30'], correctAnswer: 1, userAnswer: 0, explanation: '25% = 1/4. 80 x 1/4 = 20.' },
  { id: '5', text: 'Which symbol makes this true: 3/4 ___ 2/3', options: ['<', '>', '=', 'None'], correctAnswer: 1, userAnswer: 1, explanation: '3/4 = 0.75, 2/3 = 0.667. 3/4 > 2/3.' },
];

function ScoreCircle({ percentage }: { percentage: number }) {
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const count = useMotionValue(0);
  const spring = useSpring(count, { stiffness: 60, damping: 15 });
  const dashOffset = useTransform(spring, (v) => circumference - (v / 100) * circumference);
  const displayValue = useTransform(spring, (v) => Math.round(v));
  const ref = useRef(null);

  useEffect(() => {
    count.set(percentage);
  }, [percentage, count]);

  const getColor = () => {
    if (percentage >= 80) return '#22c55e';
    if (percentage >= 50) return '#f97316';
    return '#ef4444';
  };

  const getEmoji = () => {
    if (percentage >= 80) return '🎉';
    if (percentage >= 50) return '👍';
    return '💪';
  };

  return (
    <div className="relative flex items-center justify-center" ref={ref}>
      <svg width="180" height="180" className="-rotate-90">
        <circle cx="90" cy="90" r={radius} fill="none" stroke="currentColor" strokeWidth="10" className="text-surface-200 dark:text-surface-700" />
        <motion.circle
          cx="90"
          cy="90"
          r={radius}
          fill="none"
          stroke={getColor()}
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circumference}
          style={{ strokeDashoffset: dashOffset }}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="text-4xl">{getEmoji()}</span>
        <motion.span className="text-3xl font-bold text-surface-900 dark:text-surface-50">
          {displayValue}
        </motion.span>
        <span className="text-sm text-surface-500">%</span>
      </div>
    </div>
  );
}

export default function QuizResultsPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const params = useParams();
  const [expanded, setExpanded] = useState<string | null>(null);
  const [showConfetti, setShowConfetti] = useState(false);
  const [xpCount, setXpCount] = useState(0);
  const [showXP, setShowXP] = useState(false);

  const score = parseInt(searchParams.get('score') || '70');
  const correct = parseInt(searchParams.get('correct') || '3');
  const total = parseInt(searchParams.get('total') || '5');
  const timeTaken = parseInt(searchParams.get('time') || '300');
  const xpEarned = Math.round((score / 100) * 50);

  const [newLevel, setNewLevel] = useState<number | null>(null);

  useEffect(() => {
    if (score > 80) {
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 5000);
    }
  }, [score]);

  useEffect(() => {
    if (score >= 70) {
      const timer = setTimeout(() => {
        setShowXP(true);
        const interval = setInterval(() => {
          setXpCount((prev) => {
            if (prev >= xpEarned) {
              clearInterval(interval);
              if (xpEarned >= 40) {
                setNewLevel(2);
              }
              return xpEarned;
            }
            return prev + 1;
          });
        }, 30);
      }, 800);
      return () => clearTimeout(timer);
    }
  }, [score, xpEarned]);

  const correctCount = sampleReview.filter((q) => q.userAnswer === q.correctAnswer).length;
  const incorrectCount = sampleReview.length - correctCount;

  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-900">
      {showConfetti && (
        <div className="fixed inset-0 pointer-events-none z-50 overflow-hidden">
          {Array.from({ length: 50 }).map((_, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 1, y: -20, x: Math.random() * window.innerWidth, rotate: 0 }}
              animate={{ opacity: 0, y: window.innerHeight + 20, rotate: 720 }}
              transition={{ duration: 3 + Math.random() * 2, delay: Math.random() * 2, ease: 'easeIn' }}
              className="absolute h-3 w-3 rounded-sm"
              style={{ backgroundColor: ['#6366f1', '#d946ef', '#f97316', '#22c55e', '#ef4444'][Math.floor(Math.random() * 5)] }}
            />
          ))}
        </div>
      )}

      <div className="mx-auto max-w-3xl px-4 sm:px-6 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-8"
        >
          <div className="text-center">
            <motion.h1
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-2xl sm:text-3xl font-bold text-surface-900 dark:text-surface-50 mb-2"
            >
              Quiz Complete!
            </motion.h1>
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="text-surface-500"
            >
              Here&apos;s how you performed
            </motion.p>
          </div>

          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.3, type: 'spring', stiffness: 200 }}
            className="flex justify-center"
          >
            <ScoreCircle percentage={score} />
          </motion.div>

          {showXP && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-center"
            >
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-50 dark:bg-primary-500/10 border border-primary-200 dark:border-primary-700/30">
                <Zap className="h-4 w-4 text-accent-500" />
                <span className="text-sm font-semibold text-surface-700 dark:text-surface-300">
                  +{xpCount} XP
                </span>
                {newLevel && (
                  <span className="flex items-center gap-1 text-sm font-semibold text-primary-600 dark:text-primary-400">
                    <Sparkles className="h-4 w-4" />
                    Level Up! ({newLevel})
                  </span>
                )}
              </div>
            </motion.div>
          )}

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="grid grid-cols-2 sm:grid-cols-4 gap-4"
          >
            <div className="text-center p-4 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
              <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">{score}%</p>
              <p className="text-xs text-surface-500 mt-1">Score</p>
            </div>
            <div className="text-center p-4 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
              <div className="flex items-center justify-center gap-1.5">
                <CheckCircle2 className="h-4 w-4 text-success-500" />
                <span className="text-2xl font-bold text-surface-900 dark:text-surface-50">{correctCount}</span>
                <span className="text-sm text-surface-400">/ {total}</span>
              </div>
              <p className="text-xs text-surface-500 mt-1">Correct</p>
            </div>
            <div className="text-center p-4 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
              <div className="flex items-center justify-center gap-1.5">
                <XCircle className="h-4 w-4 text-danger-500" />
                <span className="text-2xl font-bold text-surface-900 dark:text-surface-50">{incorrectCount}</span>
              </div>
              <p className="text-xs text-surface-500 mt-1">Incorrect</p>
            </div>
            <div className="text-center p-4 rounded-xl bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700">
              <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">{formatTime(timeTaken)}</p>
              <p className="text-xs text-surface-500 mt-1">Time Taken</p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50 mb-4">
              Question Review
            </h2>
            <div className="space-y-3">
              {sampleReview.map((q, i) => {
                const isCorrect = q.userAnswer === q.correctAnswer;
                const isExpanded = expanded === q.id;
                return (
                  <motion.div
                    key={q.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 + i * 0.1 }}
                    className={cn(
                      'rounded-xl border overflow-hidden transition-colors',
                      isCorrect
                        ? 'border-success-200 dark:border-success-700/30 bg-success-50/50 dark:bg-success-500/5'
                        : 'border-danger-200 dark:border-danger-700/30 bg-danger-50/50 dark:bg-danger-500/5'
                    )}
                  >
                    <button
                      onClick={() => setExpanded(isExpanded ? null : q.id)}
                      className="w-full flex items-center gap-3 p-4 text-left"
                      aria-label={`Toggle review for question ${i + 1}`}
                    >
                      <div className={cn(
                        'flex h-8 w-8 shrink-0 items-center justify-center rounded-lg',
                        isCorrect ? 'bg-success-500 text-white' : 'bg-danger-500 text-white'
                      )}>
                        {isCorrect ? <CheckCircle2 className="h-4 w-4" /> : <XCircle className="h-4 w-4" />}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-surface-900 dark:text-surface-50 line-clamp-1">
                          {q.text}
                        </p>
                        <p className="text-xs text-surface-500 mt-0.5">
                          {isCorrect ? 'Correct' : `Your answer: ${q.options[q.userAnswer]}`}
                        </p>
                      </div>
                      {isExpanded ? <ChevronUp className="h-4 w-4 text-surface-400" /> : <ChevronDown className="h-4 w-4 text-surface-400" />}
                    </button>
                    <AnimatePresence>
                      {isExpanded && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.2 }}
                          className="overflow-hidden"
                        >
                          <div className="px-4 pb-4 pt-0 border-t border-surface-200 dark:border-surface-700 mx-4 pt-3">
                            <div className="space-y-2 text-sm">
                              {!isCorrect && (
                                <p className="text-danger-600 dark:text-danger-400">
                                  <span className="font-medium">Your answer:</span> {q.options[q.userAnswer]}
                                </p>
                              )}
                              <p className="text-success-600 dark:text-success-400">
                                <span className="font-medium">Correct answer:</span> {q.options[q.correctAnswer]}
                              </p>
                              {q.explanation && (
                                <p className="text-surface-600 dark:text-surface-400 mt-2">{q.explanation}</p>
                              )}
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4"
          >
            <Button
              variant="primary"
              icon={<RotateCcw className="h-4 w-4" />}
              onClick={() => router.push(`/quizzes/${params.id}`)}
            >
              Retry Quiz
            </Button>
            <Button
              variant="outline"
              icon={<Trophy className="h-4 w-4" />}
              onClick={() => router.push('/leaderboard')}
            >
              View Leaderboard
            </Button>
            <Button
              variant="secondary"
              icon={<ArrowRight className="h-4 w-4" />}
              iconPosition="right"
              onClick={() => router.push('/quizzes')}
            >
              Next Quiz
            </Button>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
