const express = require('express');
const Lesson = require('../models/Lesson');
const Topic = require('../models/Topic');
const User = require('../models/User');
const { verifyToken } = require('../middleware/auth');

const router = express.Router();

router.get('/', verifyToken, async (req, res) => {
  try {
    const { topic, grade, subject, page = 1, limit = 20 } = req.query;
    const filter = {};

    if (topic) filter.topicId = topic;
    if (grade) {
      const topics = await Topic.find({ grade }).select('_id');
      filter.topicId = { $in: topics.map(t => t._id) };
    }
    if (subject) {
      const topics = await Topic.find({ subjectId: subject }).select('_id');
      filter.topicId = { $in: topics.map(t => t._id) };
    }

    const skip = (parseInt(page) - 1) * parseInt(limit);
    const total = await Lesson.countDocuments(filter);

    const lessons = await Lesson.find(filter)
      .populate({
        path: 'topicId',
        select: 'title subjectId grade icon',
        populate: { path: 'subjectId', select: 'name icon color' },
      })
      .sort({ orderNumber: 1 })
      .skip(skip)
      .limit(parseInt(limit));

    res.status(200).json({
      success: true,
      data: {
        lessons,
        pagination: {
          page: parseInt(page),
          limit: parseInt(limit),
          total,
          pages: Math.ceil(total / parseInt(limit)),
        },
      },
      message: 'Lessons fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching lessons',
      error: error.message,
    });
  }
});

router.get('/:id', verifyToken, async (req, res) => {
  try {
    const lesson = await Lesson.findById(req.params.id)
      .populate({
        path: 'topicId',
        select: 'title subtitle subjectId grade icon difficulty',
        populate: { path: 'subjectId', select: 'name icon color description' },
      });

    if (!lesson) {
      return res.status(404).json({
        success: false,
        data: null,
        message: 'Lesson not found',
        error: 'Not found',
      });
    }

    const relatedLessons = await Lesson.find({
      topicId: lesson.topicId?._id,
      _id: { $ne: lesson._id },
    })
      .select('title imageEmoji orderNumber')
      .sort({ orderNumber: 1 });

    res.status(200).json({
      success: true,
      data: {
        lesson,
        relatedLessons,
      },
      message: 'Lesson fetched successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error fetching lesson',
      error: error.message,
    });
  }
});

router.post('/:id/complete', verifyToken, async (req, res) => {
  try {
    const lesson = await Lesson.findById(req.params.id);

    if (!lesson) {
      return res.status(404).json({
        success: false,
        data: null,
        message: 'Lesson not found',
        error: 'Not found',
      });
    }

    const user = await User.findById(req.user._id);
    user.points += lesson.pointsEarned;
    user.coins += Math.floor(lesson.pointsEarned / 2);
    user.lastActive = new Date();

    const newLevel = Math.floor(user.points / 500) + 1;
    if (newLevel > user.level) {
      user.level = newLevel;
    }

    await user.save();

    res.status(200).json({
      success: true,
      data: {
        lessonId: lesson._id,
        lessonTitle: lesson.title,
        pointsEarned: lesson.pointsEarned,
        coinsEarned: Math.floor(lesson.pointsEarned / 2),
        totalPoints: user.points,
        totalCoins: user.coins,
        level: user.level,
      },
      message: 'Lesson completed successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error completing lesson',
      error: error.message,
    });
  }
});

module.exports = router;
