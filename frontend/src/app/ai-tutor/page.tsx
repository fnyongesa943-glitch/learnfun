'use client';

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Send, Bot, User, Sparkles, Lightbulb, BookOpen, Calculator, Beaker, Globe, RefreshCw } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

const subjects = [
  { id: 'general', label: 'General', icon: Sparkles },
  { id: 'mathematics', label: 'Mathematics', icon: Calculator },
  { id: 'english', label: 'English', icon: BookOpen },
  { id: 'science', label: 'Science', icon: Beaker },
  { id: 'social-studies', label: 'Social Studies', icon: Globe },
];

const suggestedQuestions = [
  'Help me with fractions',
  'Explain photosynthesis',
  'Tell me a fun math fact',
  'Quiz me on grammar',
  'What is the water cycle?',
];

function MarkdownRenderer({ content }: { content: string }) {
  const lines = content.split('\n');
  return (
    <div className="space-y-2 text-sm leading-relaxed">
      {lines.map((line, i) => {
        if (line.startsWith('### ')) {
          return <h3 key={i} className="text-base font-semibold text-surface-900 dark:text-surface-50">{line.slice(4)}</h3>;
        }
        if (line.startsWith('## ')) {
          return <h2 key={i} className="text-lg font-semibold text-surface-900 dark:text-surface-50">{line.slice(3)}</h2>;
        }
        if (line.startsWith('**') && line.endsWith('**')) {
          return <p key={i} className="font-semibold text-surface-900 dark:text-surface-50">{line.slice(2, -2)}</p>;
        }
        if (line.startsWith('- ')) {
          return (
            <div key={i} className="flex items-start gap-2 pl-2">
              <span className="text-primary-500 mt-1">•</span>
              <span className="text-surface-600 dark:text-surface-400">{line.slice(2)}</span>
            </div>
          );
        }
        if (line.startsWith('1. ') || line.startsWith('2. ') || line.startsWith('3. ') || line.startsWith('4. ') || line.startsWith('5. ')) {
          return (
            <div key={i} className="flex items-start gap-2 pl-2">
              <span className="text-primary-500 font-medium">{line.slice(0, 2)}</span>
              <span className="text-surface-600 dark:text-surface-400">{line.slice(3)}</span>
            </div>
          );
        }
        if (line.trim() === '') {
          return <div key={i} className="h-2" />;
        }
        return <p key={i} className="text-surface-600 dark:text-surface-400">{line}</p>;
      })}
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="flex gap-2 items-center">
      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-surface-200 dark:bg-surface-700">
        <Bot className="h-4 w-4 text-surface-500" />
      </div>
      <div className="flex items-center gap-1 px-4 py-3 rounded-2xl bg-surface-100 dark:bg-surface-800">
        <motion.span
          animate={{ y: [0, -5, 0] }}
          transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
          className="h-2 w-2 rounded-full bg-primary-500"
        />
        <motion.span
          animate={{ y: [0, -5, 0] }}
          transition={{ duration: 0.6, repeat: Infinity, delay: 0.15 }}
          className="h-2 w-2 rounded-full bg-primary-500"
        />
        <motion.span
          animate={{ y: [0, -5, 0] }}
          transition={{ duration: 0.6, repeat: Infinity, delay: 0.3 }}
          className="h-2 w-2 rounded-full bg-primary-500"
        />
      </div>
    </div>
  );
}

export default function AiTutorPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'ai',
      content: "Hi there! I'm your LearnFun AI Tutor. I can help you with homework, explain concepts, quiz you, or just answer questions about any subject. What would you like to learn about today? 🎓",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [subject, setSubject] = useState('general');
  const [showSuggestions, setShowSuggestions] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const userMsg: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setShowSuggestions(false);

    setTimeout(() => {
      const aiMsg: Message = {
        id: `ai-${Date.now()}`,
        role: 'ai',
        content: generateResponse(input.trim(), subject),
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMsg]);
      setLoading(false);
    }, 1500);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSuggested = (q: string) => {
    setInput(q);
    inputRef.current?.focus();
  };

  const clearChat = () => {
    setMessages([
      {
        id: 'welcome',
        role: 'ai',
        content: "Hi there! I'm your LearnFun AI Tutor. I can help you with homework, explain concepts, quiz you, or just answer questions about any subject. What would you like to learn about today? 🎓",
        timestamp: new Date(),
      },
    ]);
    setShowSuggestions(true);
  };

  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-900 flex flex-col">
      <div className="mx-auto w-full max-w-3xl px-4 sm:px-6 flex-1 flex flex-col">
        <div className="flex items-center justify-between py-4 border-b border-surface-200 dark:border-surface-700">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 shadow-lg shadow-primary-500/20">
              <Bot className="h-5 w-5 text-white" />
            </div>
            <div>
              <h1 className="text-base font-semibold text-surface-900 dark:text-surface-50">AI Tutor</h1>
              <p className="text-xs text-surface-500">
                {subject === 'general' ? 'All subjects' : subjects.find((s) => s.id === subject)?.label}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={clearChat}
              className="p-2 rounded-lg text-surface-400 hover:text-surface-600 dark:hover:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
              aria-label="Clear chat"
            >
              <RefreshCw className="h-4 w-4" />
            </button>
          </div>
        </div>

        <div className="flex gap-1 overflow-x-auto py-3">
          {subjects.map((s) => {
            const Icon = s.icon;
            return (
              <button
                key={s.id}
                onClick={() => setSubject(s.id)}
                className={cn(
                  'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors',
                  subject === s.id
                    ? 'bg-primary-500 text-white'
                    : 'bg-surface-100 dark:bg-surface-800 text-surface-500 hover:text-surface-700 dark:hover:text-surface-300'
                )}
                aria-label={`Select ${s.label}`}
              >
                <Icon className="h-3.5 w-3.5" />
                {s.label}
              </button>
            );
          })}
        </div>

        <div className="flex-1 overflow-y-auto py-4 space-y-4">
          <AnimatePresence>
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className={cn(
                  'flex gap-3',
                  msg.role === 'user' ? 'justify-end' : 'justify-start'
                )}
              >
                {msg.role === 'ai' && (
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-primary-400 to-secondary-500 text-white shadow-sm">
                    <Bot className="h-4 w-4" />
                  </div>
                )}
                <div
                  className={cn(
                    'max-w-[85%] sm:max-w-[70%] rounded-2xl px-4 py-3',
                    msg.role === 'user'
                      ? 'bg-primary-500 text-white rounded-tr-md'
                      : 'bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-tl-md'
                  )}
                >
                  {msg.role === 'ai' ? (
                    <MarkdownRenderer content={msg.content} />
                  ) : (
                    <p className="text-sm">{msg.content}</p>
                  )}
                </div>
                {msg.role === 'user' && (
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-surface-200 dark:bg-surface-700">
                    <User className="h-4 w-4 text-surface-500" />
                  </div>
                )}
              </motion.div>
            ))}
            {loading && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </AnimatePresence>

          {showSuggestions && messages.length === 1 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="flex flex-wrap gap-2 pt-4"
            >
              {suggestedQuestions.map((q, i) => (
                <button
                  key={i}
                  onClick={() => handleSuggested(q)}
                  className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 text-surface-600 dark:text-surface-400 hover:bg-surface-50 dark:hover:bg-surface-700 hover:border-primary-300 dark:hover:border-primary-600 transition-colors"
                  aria-label={q}
                >
                  <Lightbulb className="h-3 w-3 text-primary-500" />
                  {q}
                </button>
              ))}
            </motion.div>
          )}
        </div>

        <div className="py-4 border-t border-surface-200 dark:border-surface-700">
          <div className="flex items-center gap-2 bg-white dark:bg-surface-800 rounded-xl border border-surface-200 dark:border-surface-700 p-1.5 focus-within:ring-2 focus-within:ring-primary-500 focus-within:border-transparent transition-all">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask me anything..."
              disabled={loading}
              className="flex-1 px-3 py-1.5 bg-transparent text-sm text-surface-900 dark:text-surface-50 placeholder:text-surface-400 focus:outline-none disabled:opacity-50"
              aria-label="Chat input"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="flex items-center justify-center h-9 w-9 rounded-lg bg-primary-500 text-white hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              aria-label="Send message"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function generateResponse(input: string, subject: string): string {
  const lower = input.toLowerCase();
  if (lower.includes('fraction')) {
    return "## Fractions 📐\n\nFractions represent parts of a whole. The **numerator** (top number) tells you how many parts you have, and the **denominator** (bottom number) tells you how many parts make up the whole.\n\n### Example:\n- 3/4 means you have 3 out of 4 equal parts\n- To add fractions with the same denominator, add the numerators: 1/4 + 2/4 = 3/4\n\nWould you like me to explain more about fractions?";
  }
  if (lower.includes('photosynthesis')) {
    return "## Photosynthesis 🌱\n\nPhotosynthesis is the process by which **green plants** make their own food using **sunlight**.\n\n### Key ingredients:\n- Carbon dioxide (CO₂) from the air\n- Water (H₂O) from the soil\n- Sunlight energy\n\n### What happens:\n1. Plants absorb sunlight through **chlorophyll** (the green pigment in leaves)\n2. They convert CO₂ and water into **glucose** (sugar) and **oxygen**\n\n### Equation:\n6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂";
  }
  if (lower.includes('quiz')) {
    return "## Quick Quiz! 🧠\n\nLet me test your knowledge:\n\n**Question:** What is the largest planet in our solar system?\n\nA) Mars\nB) Saturn\nC) Jupiter\nD) Neptune\n\nThink about it, then ask me for the answer!";
  }
  if (lower.includes('water cycle')) {
    return "## The Water Cycle 💧\n\nThe water cycle describes how water moves through the environment. It has **four main stages**:\n\n1. **Evaporation** - Sun heats water in lakes/rivers, turning it into water vapor\n2. **Condensation** - Water vapor rises, cools, and forms clouds\n3. **Precipitation** - Water falls back as rain, snow, or hail\n4. **Collection** - Water gathers in oceans, lakes, and rivers\n\nThis cycle repeats endlessly!";
  }
  if (lower.includes('math fact') || lower.includes('fun fact')) {
    return "## Fun Math Fact 🤯\n\nDid you know that **0 is the only number that can't be represented in Roman numerals**?\n\nAlso, the word 'hundred' comes from the Old Norse word 'hundrath,' which actually meant **120**, not 100!\n\nWant another fun fact? Just ask!";
  }
  return `## Great question! 💡\n\nThat's an interesting topic in **${subjects.find(s => s.id === subject)?.label || 'general'}**!\n\nHere are some key things to know:\n\n- Start by breaking down the problem into smaller parts\n- Practice regularly to build understanding\n- Don't be afraid to ask more questions - that's how we learn!\n\nWould you like me to go deeper into this topic, or do you have another question I can help with?`;
}
