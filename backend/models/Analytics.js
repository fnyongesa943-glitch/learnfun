const mongoose = require('mongoose');

const analyticsSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: [true, 'User ID is required'],
    },
    weekStart: {
      type: Date,
      required: [true, 'Week start date is required'],
    },
    quizzesTaken: {
      type: Number,
      default: 0,
    },
    avgScore: {
      type: Number,
      default: 0,
    },
    totalPoints: {
      type: Number,
      default: 0,
    },
    lessonsCompleted: {
      type: Number,
      default: 0,
    },
    streakDays: {
      type: Number,
      default: 0,
    },
    weakTopics: [
      {
        type: String,
      },
    ],
    strongTopics: [
      {
        type: String,
      },
    ],
  },
  {
    timestamps: true,
  }
);

analyticsSchema.index({ userId: 1, weekStart: -1 });

module.exports = mongoose.model('Analytics', analyticsSchema);
