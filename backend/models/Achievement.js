const mongoose = require('mongoose');

const achievementSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Achievement name is required'],
      trim: true,
    },
    icon: {
      type: String,
      default: '🏆',
    },
    description: {
      type: String,
      default: '',
    },
    criteria: {
      type: {
        type: String,
        required: [true, 'Criteria type is required'],
      },
      value: {
        type: Number,
        required: [true, 'Criteria value is required'],
      },
    },
    pointsReward: {
      type: Number,
      default: 50,
    },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model('Achievement', achievementSchema);
