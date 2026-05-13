const mongoose = require('mongoose');

const lessonSchema = new mongoose.Schema(
  {
    topicId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Topic',
      required: [true, 'Topic ID is required'],
    },
    title: {
      type: String,
      required: [true, 'Lesson title is required'],
      trim: true,
    },
    content: {
      type: String,
      required: [true, 'Lesson content is required'],
    },
    keyPoints: [
      {
        type: String,
      },
    ],
    examples: [
      {
        type: String,
      },
    ],
    didYouKnow: {
      type: String,
      default: '',
    },
    definition: {
      type: String,
      default: '',
    },
    imageEmoji: {
      type: String,
      default: '📝',
    },
    orderNumber: {
      type: Number,
      default: 0,
    },
    pointsEarned: {
      type: Number,
      default: 15,
    },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model('Lesson', lessonSchema);
