const mongoose = require('mongoose');

const scoreSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: [true, 'User ID is required'],
    },
    quizId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Quiz',
      required: [true, 'Quiz ID is required'],
    },
    score: {
      type: Number,
      required: [true, 'Score is required'],
    },
    totalQuestions: {
      type: Number,
      required: [true, 'Total questions is required'],
    },
    percentage: {
      type: Number,
      required: [true, 'Percentage is required'],
    },
    pointsEarned: {
      type: Number,
      default: 0,
    },
    timeTaken: {
      type: Number,
      default: 0,
    },
    answers: [
      {
        questionId: {
          type: mongoose.Schema.Types.ObjectId,
          ref: 'Question',
        },
        selectedAnswer: {
          type: String,
        },
        correct: {
          type: Boolean,
        },
        timeSpent: {
          type: Number,
          default: 0,
        },
      },
    ],
    completedAt: {
      type: Date,
      default: Date.now,
    },
  },
  {
    timestamps: true,
  }
);

scoreSchema.index({ userId: 1, completedAt: -1 });
scoreSchema.index({ quizId: 1 });

module.exports = mongoose.model('Score', scoreSchema);
