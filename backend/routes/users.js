const express = require('express');
const User = require('../models/User');
const Score = require('../models/Score');
const Subject = require('../models/Subject');
const { verifyToken, requireRole } = require('../middleware/auth');

const router = express.Router();

router.get('/', verifyToken, requireRole('admin'), async (req, res) => {
  try {
    const { role, grade, page = 1, limit = 50 } = req.query;
    const filter = {};
    if (role) filter.role = role;
    if (grade) filter.grade = grade;

    const skip = (parseInt(page) - 1) * parseInt(limit);
    const total = await User.countDocuments(filter);

    const users = await User.find(filter)
      .select('-password')
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    res.status(200).json({
      success: true,
      data: {
        users,
        pagination: {
          page: parseInt(page),
          limit: parseInt(limit),
          total,
          pages: Math.ceil(total / parseInt(limit)),
        },
      },
      message: 'Users fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching users',
      error: error.message,
    });
  }
});

router.get('/:id', verifyToken, async (req, res) => {
  try {
    const user = await User.findById(req.params.id).select('-password');

    if (!user) {
      return res.status(404).json({
        success: false,
        data: null,
        message: 'User not found',
        error: 'Not found',
      });
    }

    const scoreStats = await Score.aggregate([
      { $match: { userId: user._id } },
      {
        $group: {
          _id: null,
          totalQuizzes: { $sum: 1 },
          avgPercentage: { $avg: '$percentage' },
          totalPoints: { $sum: '$pointsEarned' },
        },
      },
    ]);

    res.status(200).json({
      success: true,
      data: {
        user,
        stats: scoreStats.length > 0 ? scoreStats[0] : {
          totalQuizzes: 0,
          avgPercentage: 0,
          totalPoints: 0,
        },
      },
      message: 'User fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching user',
      error: error.message,
    });
  }
});

router.put('/:id', verifyToken, async (req, res) => {
  try {
    if (req.user._id.toString() !== req.params.id && req.user.role !== 'admin') {
      return res.status(403).json({
        success: false,
        data: null,
        message: 'Not authorized to update this user',
        error: 'Forbidden',
      });
    }

    const { name, grade, avatar, points, coins, level } = req.body;

    const updateFields = {};
    if (name) updateFields.name = name;
    if (grade) updateFields.grade = grade;
    if (avatar !== undefined) updateFields.avatar = avatar;
    if (points !== undefined && req.user.role === 'admin') updateFields.points = points;
    if (coins !== undefined && req.user.role === 'admin') updateFields.coins = coins;
    if (level !== undefined && req.user.role === 'admin') updateFields.level = level;

    const user = await User.findByIdAndUpdate(req.params.id, updateFields, {
      new: true,
      runValidators: true,
    }).select('-password');

    if (!user) {
      return res.status(404).json({
        success: false,
        data: null,
        message: 'User not found',
        error: 'Not found',
      });
    }

    res.status(200).json({
      success: true,
      data: user,
      message: 'User updated successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error updating user',
      error: error.message,
    });
  }
});

router.get('/:id/progress', verifyToken, async (req, res) => {
  try {
    const userId = req.params.id;

    const user = await User.findById(userId).select('-password');
    if (!user) {
      return res.status(404).json({
        success: false,
        data: null,
        message: 'User not found',
        error: 'Not found',
      });
    }

    const scores = await Score.find({ userId })
      .populate({
        path: 'quizId',
        select: 'title subjectId grade difficulty',
        populate: { path: 'subjectId', select: 'name icon color category' },
      })
      .sort({ completedAt: -1 });

    const subjectBreakdown = {};
    for (const score of scores) {
      if (score.quizId?.subjectId) {
        const subId = score.quizId.subjectId._id.toString();
        if (!subjectBreakdown[subId]) {
          subjectBreakdown[subId] = {
            subject: score.quizId.subjectId,
            totalQuizzes: 0,
            totalScore: 0,
            bestScore: 0,
            quizzes: [],
          };
        }
        subjectBreakdown[subId].totalQuizzes += 1;
        subjectBreakdown[subId].totalScore += score.percentage;
        subjectBreakdown[subId].bestScore = Math.max(subjectBreakdown[subId].bestScore, score.percentage);
        subjectBreakdown[subId].quizzes.push({
          quizTitle: score.quizId.title,
          percentage: score.percentage,
          date: score.completedAt,
        });
      }
    }

    for (const key of Object.keys(subjectBreakdown)) {
      subjectBreakdown[key].avgScore = Math.round(
        subjectBreakdown[key].totalScore / subjectBreakdown[key].totalQuizzes
      );
    }

    const recentActivity = scores.slice(0, 10).map(s => ({
      quizTitle: s.quizId?.title || 'Unknown Quiz',
      subject: s.quizId?.subjectId?.name || 'Unknown',
      percentage: s.percentage,
      pointsEarned: s.pointsEarned,
      date: s.completedAt,
    }));

    weeklyProgress(scores);

    function weeklyProgress(scoreList) {
      const weeks = {};
      for (const s of scoreList) {
        const date = new Date(s.completedAt);
        const weekStart = new Date(date);
        weekStart.setDate(date.getDate() - date.getDay());
        const key = weekStart.toISOString().split('T')[0];
        if (!weeks[key]) {
          weeks[key] = { weekStart, quizzes: 0, totalPercentage: 0, totalPoints: 0 };
        }
        weeks[key].quizzes += 1;
        weeks[key].totalPercentage += s.percentage;
        weeks[key].totalPoints += s.pointsEarned;
      }
      return Object.entries(weeks).map(([key, val]) => ({
        week: key,
        quizzesDone: val.quizzes,
        avgScore: Math.round(val.totalPercentage / val.quizzes),
        pointsEarned: val.totalPoints,
      })).sort((a, b) => a.week.localeCompare(b.week));
    }

    res.status(200).json({
      success: true,
      data: {
        user: {
          id: user._id,
          name: user.name,
          grade: user.grade,
          points: user.points,
          coins: user.coins,
          level: user.level,
          streak: user.streak,
        },
        overallStats: {
          totalQuizzes: scores.length,
          avgScore: scores.length > 0
            ? Math.round(scores.reduce((sum, s) => sum + s.percentage, 0) / scores.length)
            : 0,
          totalPoints: scores.reduce((sum, s) => sum + s.pointsEarned, 0),
        },
        subjectBreakdown: Object.values(subjectBreakdown),
        recentActivity,
        weeklyProgress: weeklyProgress(scores),
      },
      message: 'Progress fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching progress',
      error: error.message,
    });
  }
});

router.get('/:id/weak-areas', verifyToken, async (req, res) => {
  try {
    const userId = req.params.id;

    const scores = await Score.find({ userId })
      .populate({
        path: 'quizId',
        select: 'title subjectId difficulty',
        populate: { path: 'subjectId', select: 'name icon' },
      })
      .sort({ completedAt: -1 })
      .limit(50);

    const subjectScores = {};

    for (const score of scores) {
      if (!score.quizId?.subjectId) continue;

      const subId = score.quizId.subjectId._id.toString();
      if (!subjectScores[subId]) {
        subjectScores[subId] = {
          subject: score.quizId.subjectId,
          scores: [],
          attempts: 0,
        };
      }
      subjectScores[subId].scores.push(score.percentage);
      subjectScores[subId].attempts += 1;
    }

    const weakAreas = [];
    const strongAreas = [];

    for (const key of Object.keys(subjectScores)) {
      const data = subjectScores[key];
      const avg = Math.round(
        data.scores.reduce((sum, s) => sum + s, 0) / data.scores.length
      );

      if (avg < 50 && data.attempts >= 2) {
        weakAreas.push({
          subject: data.subject,
          avgScore: avg,
          attempts: data.attempts,
          trend: data.scores.length >= 2
            ? (data.scores[0] > data.scores[data.scores.length - 1] ? 'improving' : 'needs attention')
            : 'insufficient data',
        });
      } else if (avg >= 70) {
        strongAreas.push({
          subject: data.subject,
          avgScore: avg,
          attempts: data.attempts,
        });
      }
    }

    weakAreas.sort((a, b) => a.avgScore - b.avgScore);
    strongAreas.sort((a, b) => b.avgScore - a.avgScore);

    const recommendations = weakAreas.map(area => ({
      subjectId: area.subject._id,
      subjectName: area.subject.name,
      currentAvg: area.avgScore,
      suggestedAction: `Focus on ${area.subject.name} - try practicing more quizzes to improve from ${area.avgScore}% average`,
      priority: 'high',
    }));

    if (recommendations.length === 0) {
      const user = await User.findById(userId);
      recommendations.push({
        subjectName: 'General',
        currentAvg: 0,
        suggestedAction: `Great job! Keep practicing to maintain your skills in Grade ${user?.grade || ''}`,
        priority: 'low',
      });
    }

    res.status(200).json({
      success: true,
      data: {
        weakAreas,
        strongAreas,
        recommendations,
      },
      message: 'Weak areas identified successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error analyzing weak areas',
      error: error.message,
    });
  }
});

module.exports = router;
