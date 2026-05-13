const express = require('express');
const Quiz = require('../models/Quiz');
const Question = require('../models/Question');
const Score = require('../models/Score');
const User = require('../models/User');
const Subject = require('../models/Subject');
const { verifyToken, requireRole } = require('../middleware/auth');
const { quizCreationValidation } = require('../middleware/validation');

const router = express.Router();

const shuffleArray = (arr) => {
  const shuffled = [...arr];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
};

router.get('/', verifyToken, async (req, res) => {
  try {
    const { subject, grade, difficulty, page = 1, limit = 20 } = req.query;

    const filter = {};
    if (subject) filter.subjectId = subject;
    if (grade) filter.grade = grade;
    if (difficulty) filter.difficulty = difficulty;

    const skip = (parseInt(page) - 1) * parseInt(limit);
    const total = await Quiz.countDocuments(filter);

    const quizzes = await Quiz.find(filter)
      .populate('subjectId', 'name icon color')
      .populate('topicId', 'title')
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    res.status(200).json({
      success: true,
      data: {
        quizzes,
        pagination: {
          page: parseInt(page),
          limit: parseInt(limit),
          total,
          pages: Math.ceil(total / parseInt(limit)),
        },
      },
      message: 'Quizzes fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching quizzes',
      error: error.message,
    });
  }
});

router.get('/recommended', verifyToken, async (req, res) => {
  try {
    const user = req.user;

    const recentScores = await Score.find({ userId: user._id })
      .populate({
        path: 'quizId',
        select: 'subjectId grade difficulty',
      })
      .sort({ completedAt: -1 })
      .limit(10);

    const weakAreas = [];
    const strongAreas = [];

    for (const score of recentScores) {
      if (score.percentage < 50 && score.quizId) {
        weakAreas.push(score.quizId.subjectId?.toString());
      } else if (score.percentage >= 80 && score.quizId) {
        strongAreas.push(score.quizId.subjectId?.toString());
      }
    }

    const completedQuizIds = recentScores
      .filter(s => s.quizId)
      .map(s => s.quizId._id.toString());

    const subjectFilter = weakAreas.length > 0
      ? { subjectId: { $in: weakAreas } }
      : { grade: user.grade };

    const recommendations = await Quiz.find({
      _id: { $nin: completedQuizIds },
      ...subjectFilter,
      grade: user.grade || { $exists: true },
    })
      .populate('subjectId', 'name icon color')
      .limit(3);

    if (recommendations.length < 3) {
      const extraQuizzes = await Quiz.find({
        _id: { $nin: [...completedQuizIds, ...recommendations.map(r => r._id.toString())] },
        grade: user.grade || { $exists: true },
      })
        .populate('subjectId', 'name icon color')
        .limit(3 - recommendations.length);

      recommendations.push(...extraQuizzes);
    }

    const result = recommendations.map(quiz => ({
      quiz,
      reason: weakAreas.includes(quiz.subjectId?._id?.toString())
        ? `Practice more in ${quiz.subjectId?.name || 'this subject'} to improve your skills`
        : `Recommended for ${quiz.grade} level`,
    }));

    res.status(200).json({
      success: true,
      data: result,
      message: 'Recommendations fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching recommendations',
      error: error.message,
    });
  }
});

router.get('/:id', verifyToken, async (req, res) => {
  try {
    const quiz = await Quiz.findById(req.params.id)
      .populate('subjectId', 'name icon color')
      .populate('topicId', 'title')
      .populate('lessonId', 'title');

    if (!quiz) {
      return res.status(404).json({
        success: false,
        data: null,
        message: 'Quiz not found',
        error: 'Not found',
      });
    }

    const questions = await Question.find({ quizId: quiz._id }).select('-correctAnswer');
    const shuffledQuestions = shuffleArray(questions);

    res.status(200).json({
      success: true,
      data: {
        quiz,
        questions: shuffledQuestions,
      },
      message: 'Quiz fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching quiz',
      error: error.message,
    });
  }
});

router.post('/', verifyToken, requireRole('teacher', 'admin'), quizCreationValidation, async (req, res) => {
  try {
    const { title, subjectId, grade, difficulty, description, timeLimit, topicId, lessonId } = req.body;

    const quiz = await Quiz.create({
      title,
      subjectId,
      grade,
      difficulty: difficulty || 'easy',
      description: description || '',
      timeLimit: timeLimit || 10,
      topicId: topicId || undefined,
      lessonId: lessonId || undefined,
    });

    const populatedQuiz = await Quiz.findById(quiz._id)
      .populate('subjectId', 'name icon color');

    res.status(201).json({
      success: true,
      data: populatedQuiz,
      message: 'Quiz created successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error creating quiz',
      error: error.message,
    });
  }
});

router.put('/:id', verifyToken, requireRole('teacher', 'admin'), async (req, res) => {
  try {
    const { title, subjectId, grade, difficulty, description, timeLimit, topicId, lessonId } = req.body;

    const updateFields = {};
    if (title) updateFields.title = title;
    if (subjectId) updateFields.subjectId = subjectId;
    if (grade) updateFields.grade = grade;
    if (difficulty) updateFields.difficulty = difficulty;
    if (description !== undefined) updateFields.description = description;
    if (timeLimit) updateFields.timeLimit = timeLimit;
    if (topicId) updateFields.topicId = topicId;
    if (lessonId !== undefined) updateFields.lessonId = lessonId;

    const quiz = await Quiz.findByIdAndUpdate(req.params.id, updateFields, {
      new: true,
      runValidators: true,
    }).populate('subjectId', 'name icon color');

    if (!quiz) {
      return res.status(404).json({
        success: false,
        data: null,
        message: 'Quiz not found',
        error: 'Not found',
      });
    }

    res.status(200).json({
      success: true,
      data: quiz,
      message: 'Quiz updated successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error updating quiz',
      error: error.message,
    });
  }
});

router.delete('/:id', verifyToken, requireRole('teacher', 'admin'), async (req, res) => {
  try {
    const quiz = await Quiz.findByIdAndDelete(req.params.id);

    if (!quiz) {
      return res.status(404).json({
        success: false,
        data: null,
        message: 'Quiz not found',
        error: 'Not found',
      });
    }

    await Question.deleteMany({ quizId: quiz._id });

    res.status(200).json({
      success: true,
      data: null,
      message: 'Quiz deleted successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error deleting quiz',
      error: error.message,
    });
  }
});

router.post('/:id/submit', verifyToken, async (req, res) => {
  try {
    const { answers, timeTaken } = req.body;

    if (!answers || !Array.isArray(answers)) {
      return res.status(400).json({
        success: false,
        data: null,
        message: 'Answers array is required',
        error: 'Invalid input',
      });
    }

    const quiz = await Quiz.findById(req.params.id);
    if (!quiz) {
      return res.status(404).json({
        success: false,
        data: null,
        message: 'Quiz not found',
        error: 'Not found',
      });
    }

    const questions = await Question.find({ quizId: quiz._id });

    if (questions.length === 0) {
      return res.status(400).json({
        success: false,
        data: null,
        message: 'No questions found for this quiz',
        error: 'Empty quiz',
      });
    }

    let correctCount = 0;
    let totalPoints = 0;

    const detailedAnswers = answers.map((answer) => {
      const question = questions.find(
        (q) => q._id.toString() === answer.questionId
      );

      if (!question) {
        return {
          questionId: answer.questionId,
          selectedAnswer: answer.selectedAnswer || '',
          correct: false,
          timeSpent: answer.timeSpent || 0,
        };
      }

      const isCorrect = question.correctAnswer === answer.selectedAnswer;
      if (isCorrect) {
        correctCount++;
        totalPoints += question.points || 10;
      }

      return {
        questionId: question._id,
        selectedAnswer: answer.selectedAnswer || '',
        correct: isCorrect,
        timeSpent: answer.timeSpent || 0,
      };
    });

    const percentage = Math.round((correctCount / questions.length) * 100);

    const user = await User.findById(req.user._id);
    const pointsGained = Math.round(totalPoints * (percentage / 100));
    user.points += pointsGained;
    user.coins += Math.floor(pointsGained / 2);

    const now = new Date();
    const lastActive = user.lastActive;
    if (lastActive) {
      const diffDays = Math.floor((now - lastActive) / (1000 * 60 * 60 * 24));
      if (diffDays === 1) {
        user.streak += 1;
      } else if (diffDays > 1) {
        user.streak = 1;
      }
    } else {
      user.streak = 1;
    }
    user.lastActive = now;

    const newLevel = Math.floor(user.points / 500) + 1;
    if (newLevel > user.level) {
      user.level = newLevel;
    }

    await user.save();

    const score = await Score.create({
      userId: req.user._id,
      quizId: quiz._id,
      score: correctCount,
      totalQuestions: questions.length,
      percentage,
      pointsEarned: pointsGained,
      timeTaken: timeTaken || 0,
      answers: detailedAnswers,
    });

    const correctAnswers = questions.map((q) => ({
      questionId: q._id,
      text: q.text,
      correctAnswer: q.correctAnswer,
      explanation: q.explanation,
      options: q.options,
    }));

    res.status(200).json({
      success: true,
      data: {
        score: score._id,
        correctCount,
        totalQuestions: questions.length,
        percentage,
        pointsEarned: pointsGained,
        coinsEarned: Math.floor(pointsGained / 2),
        timeTaken: timeTaken || 0,
        streak: user.streak,
        level: user.level,
        totalPoints: user.points,
        correctAnswers,
      },
      message: 'Quiz submitted successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error submitting quiz',
      error: error.message,
    });
  }
});

module.exports = router;
