const mongoose = require('mongoose');

const subjectSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Subject name is required'],
      trim: true,
    },
    icon: {
      type: String,
      default: '📚',
    },
    color: {
      type: String,
      default: '#4F46E5',
    },
    description: {
      type: String,
      default: '',
    },
    category: {
      type: String,
      enum: ['Core', 'Religious', 'Life Skills', 'Creative'],
      required: [true, 'Category is required'],
    },
    grade: {
      type: String,
      enum: ['PP1', 'PP2', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'],
    },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model('Subject', subjectSchema);
