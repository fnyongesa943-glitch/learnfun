'use client';

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import toast from 'react-hot-toast';
import { ChevronLeft, ChevronRight, SkipForward, Send, AlertTriangle, Clock } from 'lucide-react';

interface Question {
  id: string;
  text: string;
  options: string[];
  correctAnswer: number;
  explanation?: string;
}

const sampleQuestions: Question[] = [
  {
    id: '1',
    text: 'What is 2/3 + 1/3?',
    options: ['1/3', '2/3', '1', '4/3'],
    correctAnswer: 2,
    explanation: '2/3 + 1/3 = 3/3 = 1. When denominators are the same, add the numerators.',
  },
  {
    id: '2',
    text: 'Which of these is a proper fraction?',
    options: ['5/3', '3/4', '7/5', '9/8'],
    correctAnswer: 1,
    explanation: 'A proper fraction has numerator less than denominator. 3/4 is a proper fraction.',
  },
  {
    id: '3',
    text: 'What is 0.5 written as a fraction?',
    options: ['1/5', '1/4', '1/3', '1/2'],
    correctAnswer: 3,
    explanation: '0.5 = 5/10 = 1/2 in simplest form.',
  },
  {
    id: '4',
    text: 'What is 25% of 80?',
    options: ['15', '20', '25', '30'],
    correctAnswer: 1,
    explanation: '25% = 25/100 = 1/4. 80 × 1/4 = 20.',
  },
  {
    id: '5',
    text: 'Which symbol makes this true: 3/4 ___ 2/3',
    options: ['<', '>', '=', 'None'],
    correctAnswer: 1,
    explanation: '3/4 = 0.75, 2/3 = 0.667. So 3/4 > 2/3.',
  },
];

const optionLabels = ['A', 'B', 'C', 'D'];

export default function QuizAttemptPage() {
  const router = useRouter();
  const params = useParams();
  const [questions] = useState<Question[]>(sampleQuestions);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<(number | null)[]>(Array(sampleQuestions.length).fill(null));
  const [showFeedback, setShowFeedback] = useState(false);
  const [timeLeft, setTimeLeft] = useState(600);
  const [tabSwitches, setTabSwitches] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const submitRef = useRef<() => void>(() => {});
  const answersRef = useRef<(number | null)[]>(answers);
  const timeLeftRef = useRef<number>(timeLeft);

  const totalQuestions = questions.length;
  const currentQuestion = questions[currentIndex];
  const answeredCount = answers.filter((a) => a !== null).length;
  const progress = (answeredCount / totalQuestions) * 100;

  useEffect(() => {
    answersRef.current = answers;
  }, [answers]);

  useEffect(() => {
    timeLeftRef.current = timeLeft;
  }, [timeLeft]);

  const handleSubmit = useCallback(() => {
    if (isSubmitting) return;
    setIsSubmitting(true);
    const score = answers.reduce<number>((acc, ans, i) => {
      return acc + (ans === questions[i]?.correctAnswer ? 1 : 0);
    }, 0);
    const percentage = Math.round((score / totalQuestions) * 100);
    const timeTaken = 600 - timeLeftRef.current;
    router.push(
      `/quizzes/${params.id}/results?score=${percentage}&correct=${score}&total=${totalQuestions}&time=${timeTaken}`
    );
  }, [answers, questions, router, params.id, totalQuestions, isSubmitting]);

  useEffect(() => {
    submitRef.current = handleSubmit;
  }, [handleSubmit]);

  useEffect(() => {
    timerRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timerRef.current!);
          submitRef.current();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  useEffect(() => {
    const handleVisibility = () => {
      if (document.hidden) {
        setTabSwitches((prev) => {
          const newCount = prev + 1;
          if (newCount >= 3) {
            toast.error('Multiple tab switches detected! Submitting quiz.');
            submitRef.current();
          } else {
            toast(`Tab switch detected! (${newCount}/3 warnings)`, { icon: '⚠️', style: { background: '#fef3c7', color: '#92400e' } });
          }
          return newCount;
        });
      }
    };
    document.addEventListener('visibilitychange', handleVisibility);
    return () => document.removeEventListener('visibilitychange', handleVisibility);
  }, []);

  const handleAnswer = (optionIndex: number) => {
    if (showFeedback) return;
    const newAnswers = [...answers];
    newAnswers[currentIndex] = optionIndex;
    setAnswers(newAnswers);
    setShowFeedback(true);
  };

  const handleNext = () => {
    if (currentIndex < totalQuestions - 1) {
      setCurrentIndex(currentIndex + 1);
      setShowFeedback(false);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      setShowFeedback(false);
    }
  };

  const handleSkip = () => {
    if (currentIndex < totalQuestions - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  const isCorrect = answers[currentIndex] === currentQuestion?.correctAnswer;
  const isWarning = timeLeft <= 60;

  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-900">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 py-8">
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <button
              onClick={() => router.back()}
              className="flex items-center gap-1.5 text-sm text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 transition-colors"
              aria-label="Go back"
            >
              <ChevronLeft className="h-4 w-4" />
              Exit
            </button>
            <div className={cn(
              'flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium',
              isWarning
                ? 'bg-danger-50 dark:bg-danger-500/10 text-danger-600 dark:text-danger-400 animate-pulse'
                : 'bg-surface-100 dark:bg-surface-800 text-surface-600 dark:text-surface-400'
            )}>
              <Clock className="h-4 w-4" />
              {formatTime(timeLeft)}
            </div>
          </div>

          <div className="h-2 rounded-full bg-surface-200 dark:bg-surface-700 overflow-hidden">
            <motion.div
              className="h-full rounded-full bg-primary-500"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>

          <div className="flex items-center justify-center gap-1.5">
            {questions.map((_, i) => (
              <button
                key={i}
                onClick={() => { setCurrentIndex(i); setShowFeedback(answers[i] !== null); }}
                className={cn(
                  'h-2.5 rounded-full transition-all duration-300',
                  i === currentIndex
                    ? 'w-8 bg-primary-500'
                    : answers[i] !== null
                    ? 'w-2.5 bg-success-500'
                    : 'w-2.5 bg-surface-300 dark:bg-surface-600'
                )}
                aria-label={`Go to question ${i + 1}`}
              />
            ))}
          </div>

          {tabSwitches >= 2 && (
            <div className="flex items-center gap-2 p-3 rounded-lg bg-danger-50 dark:bg-danger-500/10 border border-danger-200 dark:border-danger-700/30">
              <AlertTriangle className="h-4 w-4 text-danger-500 shrink-0" />
              <p className="text-xs text-danger-600 dark:text-danger-400">
                Warning: Multiple tab switches detected. Further switches will auto-submit your quiz.
              </p>
            </div>
          )}

          <AnimatePresence mode="wait">
            <motion.div
              key={currentIndex}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.25 }}
              className="space-y-6"
            >
              <div className="text-xs font-medium text-surface-500">
                Question {currentIndex + 1} of {totalQuestions}
              </div>

              <h2 className="text-xl sm:text-2xl font-semibold text-surface-900 dark:text-surface-50 leading-relaxed">
                {currentQuestion?.text}
              </h2>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {currentQuestion?.options.map((option, i) => {
                  const isSelected = answers[currentIndex] === i;
                  const showCorrect = showFeedback && currentQuestion.correctAnswer === i;
                  const showIncorrect = showFeedback && isSelected && !isCorrect;

                  return (
                    <motion.button
                      key={i}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => handleAnswer(i)}
                      disabled={showFeedback}
                      className={cn(
                        'flex items-center gap-3 p-4 rounded-xl text-left transition-all duration-200 border-2',
                        'focus:outline-none focus:ring-2 focus:ring-primary-500',
                        isSelected && !showFeedback
                          ? 'border-primary-500 bg-primary-50 dark:bg-primary-500/10'
                          : showCorrect
                          ? 'border-success-500 bg-success-50 dark:bg-success-500/10'
                          : showIncorrect
                          ? 'border-danger-500 bg-danger-50 dark:bg-danger-500/10'
                          : 'border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-800 hover:border-primary-300 dark:hover:border-primary-600'
                      )}
                      aria-label={`Option ${optionLabels[i]}: ${option}`}
                    >
                      <span className={cn(
                        'flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-sm font-semibold',
                        isSelected && !showFeedback
                          ? 'bg-primary-500 text-white'
                          : showCorrect
                          ? 'bg-success-500 text-white'
                          : showIncorrect
                          ? 'bg-danger-500 text-white'
                          : 'bg-surface-100 dark:bg-surface-700 text-surface-600 dark:text-surface-400'
                      )}>
                        {optionLabels[i]}
                      </span>
                      <span className={cn(
                        'text-sm',
                        showCorrect && 'text-success-700 dark:text-success-400 font-medium',
                        showIncorrect && 'text-danger-700 dark:text-danger-400 font-medium'
                      )}>
                        {option}
                      </span>
                    </motion.button>
                  );
                })}
              </div>

              {showFeedback && currentQuestion?.explanation && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={cn(
                    'p-4 rounded-xl border',
                    isCorrect
                      ? 'bg-success-50 dark:bg-success-500/10 border-success-200 dark:border-success-700/30'
                      : 'bg-danger-50 dark:bg-danger-500/10 border-danger-200 dark:border-danger-700/30'
                  )}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span className={cn(
                      'text-sm font-semibold',
                      isCorrect ? 'text-success-700 dark:text-success-400' : 'text-danger-700 dark:text-danger-400'
                    )}>
                      {isCorrect ? 'Correct!' : 'Incorrect'}
                    </span>
                  </div>
                  <p className="text-sm text-surface-600 dark:text-surface-400">
                    {currentQuestion.explanation}
                  </p>
                </motion.div>
              )}
            </motion.div>
          </AnimatePresence>

          <div className="flex items-center justify-between pt-4 border-t border-surface-200 dark:border-surface-700">
            <button
              onClick={handlePrevious}
              disabled={currentIndex === 0}
              className="flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium text-surface-600 dark:text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-800 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              aria-label="Previous question"
            >
              <ChevronLeft className="h-4 w-4" />
              Previous
            </button>

            <div className="flex items-center gap-2">
              {answers[currentIndex] === null && (
                <button
                  onClick={handleSkip}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
                  aria-label="Skip question"
                >
                  <SkipForward className="h-4 w-4" />
                  Skip
                </button>
              )}

              {currentIndex === totalQuestions - 1 ? (
                <button
                  onClick={handleSubmit}
                  disabled={answeredCount < totalQuestions}
                  className="flex items-center gap-1.5 px-6 py-2 rounded-lg text-sm font-medium bg-primary-500 text-white hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  aria-label="Submit quiz"
                >
                  <Send className="h-4 w-4" />
                  Submit
                </button>
              ) : (
                <button
                  onClick={handleNext}
                  disabled={!showFeedback}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium bg-primary-500 text-white hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  aria-label="Next question"
                >
                  Next
                  <ChevronRight className="h-4 w-4" />
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
