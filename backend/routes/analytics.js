const express = require('express');
const Score = require('../models/Score');
const User = require('../models/User');
const Lesson = require('../models/Lesson');
const Analytics = require('../models/Analytics');
const { verifyToken, requireRole } = require('../middleware/auth');

const router = express.Router();

router.get('/dashboard', verifyToken, async (req, res) => {
  try {
    const userId = req.user._id;
    const user = await User.findById(userId);

    if (!user) {
      return res.status(404).json({
        success: false,
        data: null,
        message: 'User not found',
        error: 'Not found',
      });
    }

    const now = new Date();
    const weekStart = new Date(now);
    weekStart.setDate(now.getDate() - now.getDay());
    weekStart.setHours(0, 0, 0, 0);

    const thisWeekScores = await Score.find({
      userId,
      completedAt: { $gte: weekStart },
    });

    const totalScores = await Score.countDocuments({ userId });

    const avgScoreResult = await Score.aggregate([
      { $match: { userId } },
      { $group: { _id: null, avg: { $avg: '$percentage' } } },
    ]);
    const avgScore = avgScoreResult.length > 0 ? Math.round(avgScoreResult[0].avg) : 0;

    const weekAvg = thisWeekScores.length > 0
      ? Math.round(thisWeekScores.reduce((sum, s) => sum + s.percentage, 0) / thisWeekScores.length)
      : 0;

    const recentScores = await Score.find({ userId })
      .populate({
        path: 'quizId',
        select: 'title subjectId',
        populate: { path: 'subjectId', select: 'name icon color' },
      })
      .sort({ completedAt: -1 })
      .limit(5);

    const monthlyScores = await Score.aggregate([
      { $match: { userId } },
      {
        $group: {
          _id: {
            year: { $year: '$completedAt' },
            month: { $month: '$completedAt' },
          },
          avgScore: { $avg: '$percentage' },
          count: { $sum: 1 },
          totalPoints: { $sum: '$pointsEarned' },
        },
      },
      { $sort: { '_id.year': -1, '_id.month': -1 } },
      { $limit: 6 },
    ]);

    const monthlyData = monthlyScores.map(ms => ({
      month: `${ms._id.year}-${String(ms._id.month).padStart(2, '0')}`,
      avgScore: Math.round(ms.avgScore),
      quizzesTaken: ms.count,
      pointsEarned: ms.totalPoints,
    }));

    const subjectPerformance = await Score.aggregate([
      { $match: { userId } },
      {
        $lookup: {
          from: 'quizzes',
          localField: 'quizId',
          foreignField: '_id',
          as: 'quiz',
        },
      },
      { $unwind: { path: '$quiz', preserveNullAndEmptyArrays: true } },
      {
        $lookup: {
          from: 'subjects',
          localField: 'quiz.subjectId',
          foreignField: '_id',
          as: 'subject',
        },
      },
      { $unwind: { path: '$subject', preserveNullAndEmptyArrays: true } },
      {
        $group: {
          _id: '$subject._id',
          subjectName: { $first: '$subject.name' },
          subjectIcon: { $first: '$subject.icon' },
          subjectColor: { $first: '$subject.color' },
          avgScore: { $avg: '$percentage' },
          quizzesTaken: { $sum: 1 },
          totalPoints: { $sum: '$pointsEarned' },
        },
      },
      { $sort: { avgScore: -1 } },
    ]);

    res.status(200).json({
      success: true,
      data: {
        user: {
          name: user.name,
          grade: user.grade,
          points: user.points,
          coins: user.coins,
          level: user.level,
          streak: user.streak,
        },
        overview: {
          totalQuizzes: totalScores,
          overallAvgScore: avgScore,
          weekQuizzes: thisWeekScores.length,
          weekAvgScore: weekAvg,
        },
        recentScores,
        monthlyProgress: monthlyData,
        subjectPerformance,
      },
      message: 'Dashboard analytics fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching dashboard analytics',
      error: error.message,
    });
  }
});

router.get('/teacher/:id', verifyToken, requireRole('teacher', 'admin'), async (req, res) => {
  try {
    const teacherId = req.params.id;

    const students = await User.find({ role: 'student' }).select('_id name grade points level streak');

    const studentIds = students.map(s => s._id);

    const classStats = await Score.aggregate([
      { $match: { userId: { $in: studentIds } } },
      {
        $group: {
          _id: null,
          totalQuizzes: { $sum: 1 },
          avgScore: { $avg: '$percentage' },
          totalPoints: { $sum: '$pointsEarned' },
        },
      },
    ]);

    const gradeDistribution = {};
    for (const student of students) {
      const grade = student.grade || 'Unassigned';
      if (!gradeDistribution[grade]) {
        gradeDistribution[grade] = { count: 0, totalPoints: 0 };
      }
      gradeDistribution[grade].count += 1;
      gradeDistribution[grade].totalPoints += student.points;
    }

    const topStudents = students
      .sort((a, b) => b.points - a.points)
      .slice(0, 10)
      .map((s, i) => ({
        rank: i + 1,
        name: s.name,
        grade: s.grade,
        points: s.points,
        level: s.level,
        streak: s.streak,
      }));

    res.status(200).json({
      success: true,
      data: {
        totalStudents: students.length,
        avgScore: classStats.length > 0 ? Math.round(classStats[0].avgScore) : 0,
        totalQuizzesTaken: classStats.length > 0 ? classStats[0].totalQuizzes : 0,
        totalPointsEarned: classStats.length > 0 ? classStats[0].totalPoints : 0,
        gradeDistribution,
        topStudents,
      },
      message: 'Teacher analytics fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching teacher analytics',
      error: error.message,
    });
  }
});

router.get('/progress', verifyToken, async (req, res) => {
  try {
    const userId = req.user._id;
    const { period = 'weekly' } = req.query;

    const now = new Date();
    let startDate;

    if (period === 'monthly') {
      startDate = new Date(now);
      startDate.setMonth(now.getMonth() - 6);
    } else {
      startDate = new Date(now);
      startDate.setDate(now.getDate() - 42);
    }

    const scores = await Score.find({
      userId,
      completedAt: { $gte: startDate },
    }).sort({ completedAt: 1 });

    const chartData = [];

    if (period === 'monthly') {
      const monthlyMap = {};
      for (const score of scores) {
        const key = `${score.completedAt.getFullYear()}-${String(score.completedAt.getMonth() + 1).padStart(2, '0')}`;
        if (!monthlyMap[key]) {
          monthlyMap[key] = { scores: [], points: 0 };
        }
        monthlyMap[key].scores.push(score.percentage);
        monthlyMap[key].points += score.pointsEarned;
      }

      for (const [month, data] of Object.entries(monthlyMap)) {
        chartData.push({
          label: month,
          avgScore: Math.round(data.scores.reduce((s, v) => s + v, 0) / data.scores.length),
          quizzesTaken: data.scores.length,
          pointsEarned: data.points,
        });
      }
    } else {
      const weeklyMap = {};
      for (const score of scores) {
        const d = new Date(score.completedAt);
        const weekStart = new Date(d);
        weekStart.setDate(d.getDate() - d.getDay());
        const key = weekStart.toISOString().split('T')[0];
        if (!weeklyMap[key]) {
          weeklyMap[key] = { scores: [], points: 0, weekStart };
        }
        weeklyMap[key].scores.push(score.percentage);
        weeklyMap[key].points += score.pointsEarned;
      }

      for (const [week, data] of Object.entries(weeklyMap)) {
        chartData.push({
          label: week,
          avgScore: Math.round(data.scores.reduce((s, v) => s + v, 0) / data.scores.length),
          quizzesTaken: data.scores.length,
          pointsEarned: data.points,
        });
      }

      chartData.sort((a, b) => a.label.localeCompare(b.label));
    }

    const user = await User.findById(userId);

    res.status(200).json({
      success: true,
      data: {
        period,
        chartData,
        currentStats: {
          points: user?.points || 0,
          level: user?.level || 1,
          streak: user?.streak || 0,
        },
      },
      message: 'Progress chart data fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching progress chart data',
      error: error.message,
    });
  }
});

module.exports = router;
