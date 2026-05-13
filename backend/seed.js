const mongoose = require('mongoose');
const dotenv = require('dotenv');
const Achievement = require('./models/Achievement');
const Subject = require('./models/Subject');

dotenv.config();

const achievements = [
  {
    name: 'First Quiz',
    icon: '🎯',
    description: 'Complete your first quiz',
    criteria: { type: 'quizzes_taken', value: 1 },
    pointsReward: 50,
  },
  {
    name: 'Perfect Score',
    icon: '💯',
    description: 'Score 100% on any quiz',
    criteria: { type: 'perfect_score', value: 1 },
    pointsReward: 100,
  },
  {
    name: 'Math Star',
    icon: '⭐',
    description: 'Score above 80% in 5 Mathematics quizzes',
    criteria: { type: 'math_quizzes', value: 5 },
    pointsReward: 150,
  },
  {
    name: 'Reading Pro',
    icon: '📖',
    description: 'Complete 10 English lessons',
    criteria: { type: 'lessons_completed', value: 10 },
    pointsReward: 100,
  },
  {
    name: 'Streak Master',
    icon: '🔥',
    description: 'Achieve a 7-day learning streak',
    criteria: { type: 'streak_days', value: 7 },
    pointsReward: 200,
  },
  {
    name: 'Quiz Champion',
    icon: '🏆',
    description: 'Complete 20 quizzes',
    criteria: { type: 'quizzes_taken', value: 20 },
    pointsReward: 300,
  },
  {
    name: 'Science Explorer',
    icon: '🔬',
    description: 'Score above 70% in 5 Science quizzes',
    criteria: { type: 'science_quizzes', value: 5 },
    pointsReward: 150,
  },
  {
    name: 'Fast Learner',
    icon: '⚡',
    description: 'Complete a quiz in under 2 minutes with 80%+ score',
    criteria: { type: 'fast_quiz', value: 1 },
    pointsReward: 100,
  },
  {
    name: 'Knowledge Seeker',
    icon: '🧠',
    description: 'Reach level 5',
    criteria: { type: 'level_reached', value: 5 },
    pointsReward: 250,
  },
  {
    name: 'All Rounder',
    icon: '🌈',
    description: 'Take quizzes in 4 different subjects',
    criteria: { type: 'subjects_covered', value: 4 },
    pointsReward: 200,
  },
  {
    name: 'Consistent Scholar',
    icon: '📚',
    description: 'Complete at least one quiz every day for 30 days',
    criteria: { type: 'daily_quizzes', value: 30 },
    pointsReward: 500,
  },
  {
    name: 'Creative Genius',
    icon: '🎨',
    description: 'Complete all Creative Arts lessons',
    criteria: { type: 'creative_complete', value: 1 },
    pointsReward: 150,
  },
  {
    name: 'Math Whiz',
    icon: '🔢',
    description: 'Achieve 90%+ average in Mathematics over 10 quizzes',
    criteria: { type: 'math_average', value: 90 },
    pointsReward: 300,
  },
  {
    name: 'Rising Star',
    icon: '🌟',
    description: 'Improve your score by 20% or more on a retaken quiz',
    criteria: { type: 'score_improvement', value: 20 },
    pointsReward: 100,
  },
  {
    name: 'Helper Bee',
    icon: '🐝',
    description: 'Help 3 classmates by sharing study tips',
    criteria: { type: 'helped_others', value: 3 },
    pointsReward: 100,
  },
];

const subjects = [
  {
    name: 'Mathematics',
    icon: '🔢',
    color: '#4F46E5',
    description: 'Numbers, shapes, measurements, and problem solving',
    category: 'Core',
    grade: 'G1',
  },
  {
    name: 'English',
    icon: '📝',
    color: '#059669',
    description: 'Reading, writing, grammar, and communication skills',
    category: 'Core',
    grade: 'G1',
  },
  {
    name: 'Kiswahili',
    icon: '🗣️',
    color: '#DC2626',
    description: 'Lugha ya taifa, sarufi, ufahamu na msamiati',
    category: 'Core',
    grade: 'G1',
  },
  {
    name: 'Science & Technology',
    icon: '🔬',
    color: '#0891B2',
    description: 'Scientific inquiry, technology, and discovery',
    category: 'Core',
    grade: 'G4',
  },
  {
    name: 'Social Studies',
    icon: '🌍',
    color: '#D97706',
    description: 'Community, history, geography, and citizenship',
    category: 'Core',
    grade: 'G4',
  },
  {
    name: 'CRE',
    icon: '✝️',
    color: '#7C3AED',
    description: 'Christian Religious Education - values and faith',
    category: 'Religious',
    grade: 'G1',
  },
  {
    name: 'Islamic Religious Education',
    icon: '🕌',
    color: '#059669',
    description: 'Islamic Religious Education - values and faith',
    category: 'Religious',
    grade: 'G1',
  },
  {
    name: 'Hindu Religious Education',
    icon: '🕉️',
    color: '#D97706',
    description: 'Hindu Religious Education - values and faith',
    category: 'Religious',
    grade: 'G1',
  },
  {
    name: 'Agriculture',
    icon: '🌱',
    color: '#65A30D',
    description: 'Farming, plants, animals, and food production',
    category: 'Core',
    grade: 'G4',
  },
  {
    name: 'Home Science',
    icon: '🏠',
    color: '#E11D48',
    description: 'Cooking, sewing, hygiene, and home management',
    category: 'Life Skills',
    grade: 'G4',
  },
  {
    name: 'Physical Education',
    icon: '⚽',
    color: '#2563EB',
    description: 'Sports, fitness, teamwork, and healthy living',
    category: 'Life Skills',
    grade: 'G1',
  },
  {
    name: 'Creative Arts',
    icon: '🎨',
    color: '#F59E0B',
    description: 'Art, music, dance, and creative expression',
    category: 'Creative',
    grade: 'G1',
  },
  {
    name: 'Music',
    icon: '🎵',
    color: '#EC4899',
    description: 'Singing, instruments, rhythm, and musical appreciation',
    category: 'Creative',
    grade: 'G1',
  },
  {
    name: 'Indigenous Languages',
    icon: '🏛️',
    color: '#8B5CF6',
    description: 'Mother tongue and indigenous language learning',
    category: 'Core',
    grade: 'G1',
  },
  {
    name: 'Pastoral/Religious Instruction',
    icon: '📿',
    color: '#BE185D',
    description: 'Moral and religious instruction',
    category: 'Religious',
    grade: 'G1',
  },
  {
    name: 'Life Skills',
    icon: '💡',
    color: '#0D9488',
    description: 'Communication, cooperation, and daily living skills',
    category: 'Life Skills',
    grade: 'G4',
  },
];

const seedDB = async () => {
  try {
    const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017/learnfun';
    await mongoose.connect(uri);
    console.log('MongoDB connected for seeding...');

    await Achievement.deleteMany({});
    const createdAchievements = await Achievement.insertMany(achievements);
    console.log(`Seeded ${createdAchievements.length} achievements`);

    await Subject.deleteMany({});
    const createdSubjects = await Subject.insertMany(subjects);
    console.log(`Seeded ${createdSubjects.length} subjects`);

    console.log('Database seeding completed successfully!');
    process.exit(0);
  } catch (error) {
    console.error('Seeding error:', error.message);
    process.exit(1);
  }
};

seedDB();
