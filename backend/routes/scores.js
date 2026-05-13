const express = require('express');
const Score = require('../models/Score');
const User = require('../models/User');
const { verifyToken } = require('../middleware/auth');

const router = express.Router();

router.get('/', verifyToken, async (req, res) => {
  try {
    const { page = 1, limit = 20 } = req.query;
    const skip = (parseInt(page) - 1) * parseInt(limit);

    const filter = { userId: req.user._id };
    const total = await Score.countDocuments(filter);

    const scores = await Score.find(filter)
      .populate({
        path: 'quizId',
        select: 'title subjectId grade difficulty',
        populate: { path: 'subjectId', select: 'name icon color' },
      })
      .sort({ completedAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    res.status(200).json({
      success: true,
      data: {
        scores,
        pagination: {
          page: parseInt(page),
          limit: parseInt(limit),
          total,
          pages: Math.ceil(total / parseInt(limit)),
        },
      },
      message: 'Scores fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching scores',
      error: error.message,
    });
  }
});

router.get('/leaderboard', verifyToken, async (req, res) => {
  try {
    const { grade, subject, limit = 20 } = req.query;

    const matchStage = {};
    if (grade) matchStage.grade = grade;

    const pipeline = [
      {
        $group: {
          _id: '$userId',
          avgPercentage: { $avg: '$percentage' },
          totalQuizzes: { $sum: 1 },
          totalPoints: { $sum: '$pointsEarned' },
          bestScore: { $max: '$percentage' },
        },
      },
      { $sort: { avgPercentage: -1 } },
      { $limit: parseInt(limit) },
      {
        $lookup: {
          from: 'users',
          localField: '_id',
          foreignField: '_id',
          as: 'user',
        },
      },
      { $unwind: { path: '$user', preserveNullAndEmptyArrays: true } },
    ];

    if (grade) {
      pipeline.push({ $match: { 'user.grade': grade } });
    }

    const leaderboard = await Score.aggregate(pipeline);

    const result = leaderboard.map((entry, index) => ({
      rank: index + 1,
      userId: entry._id,
      name: entry.user?.name || 'Unknown',
      grade: entry.user?.grade || 'N/A',
      avatar: entry.user?.avatar || '',
      avgPercentage: Math.round(entry.avgPercentage),
      totalQuizzes: entry.totalQuizzes,
      totalPoints: entry.totalPoints,
      bestScore: Math.round(entry.bestScore),
    }));

    res.status(200).json({
      success: true,
      data: result,
      message: 'Leaderboard fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching leaderboard',
      error: error.message,
    });
  }
});

router.get('/stats', verifyToken, async (req, res) => {
  try {
    const userId = req.user._id;

    const totalQuizzes = await Score.countDocuments({ userId });

    const avgResult = await Score.aggregate([
      { $match: { userId: userId } },
      { $group: { _id: null, avgPercentage: { $avg: '$percentage' } } },
    ]);

    const avgScore = avgResult.length > 0 ? Math.round(avgResult[0].avgPercentage) : 0;

    const totalPointsResult = await Score.aggregate([
      { $match: { userId: userId } },
      { $group: { _id: null, total: { $sum: '$pointsEarned' } } },
    ]);

    const totalPoints = totalPointsResult.length > 0 ? totalPointsResult[0].total : 0;

    const recentScores = await Score.find({ userId })
      .sort({ completedAt: -1 })
      .limit(5)
      .populate({
        path: 'quizId',
        select: 'title subjectId',
        populate: { path: 'subjectId', select: 'name icon' },
      });

    const maxStreak = await Score.aggregate([
      { $match: { userId: userId } },
      { $sort: { completedAt: -1 } },
      { $limit: 1 },
    ]);

    const user = await User.findById(userId);

    res.status(200).json({
      success: true,
      data: {
        totalQuizzes,
        avgScore,
        totalPoints,
        currentLevel: user?.level || 1,
        currentStreak: user?.streak || 0,
        totalCoins: user?.coins || 0,
        recentScores,
      },
      message: 'Stats fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching stats',
      error: error.message,
    });
  }
});

router.get('/:id', verifyToken, async (req, res) => {
  try {
    const score = await Score.findOne({
      _id: req.params.id,
      userId: req.user._id,
    })
      .populate({
        path: 'quizId',
        select: 'title subjectId grade difficulty description timeLimit',
        populate: { path: 'subjectId', select: 'name icon color' },
      })
      .populate({
        path: 'answers.questionId',
        select: 'text options correctAnswer explanation',
      });

    if (!score) {
      return res.status(404).json({
        success: false,
        data: null,
        message: 'Score not found',
        error: 'Not found',
      });
    }

    res.status(200).json({
      success: true,
      data: score,
      message: 'Score fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching score',
      error: error.message,
    });
  }
});

module.exports = router;
