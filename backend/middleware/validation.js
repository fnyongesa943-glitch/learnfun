const { body, validationResult } = require('express-validator');

const handleValidationErrors = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      success: false,
      data: null,
      message: 'Validation failed',
      error: errors.array().map(e => e.msg).join(', '),
    });
  }
  next();
};

const registerValidation = [
  body('name')
    .trim()
    .notEmpty().withMessage('Name is required')
    .isLength({ max: 50 }).withMessage('Name cannot exceed 50 characters'),
  body('email')
    .trim()
    .isEmail().withMessage('Please provide a valid email'),
  body('password')
    .isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
  body('grade')
    .optional()
    .isIn(['PP1', 'PP2', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'])
    .withMessage('Invalid grade'),
  handleValidationErrors,
];

const loginValidation = [
  body('email')
    .trim()
    .isEmail().withMessage('Please provide a valid email'),
  body('password')
    .notEmpty().withMessage('Password is required'),
  handleValidationErrors,
];

const quizCreationValidation = [
  body('title')
    .trim()
    .notEmpty().withMessage('Quiz title is required'),
  body('subjectId')
    .notEmpty().withMessage('Subject ID is required')
    .isMongoId().withMessage('Invalid Subject ID'),
  body('grade')
    .notEmpty().withMessage('Grade is required')
    .isIn(['PP1', 'PP2', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'])
    .withMessage('Invalid grade'),
  body('difficulty')
    .optional()
    .isIn(['easy', 'medium', 'hard']).withMessage('Invalid difficulty'),
  handleValidationErrors,
];

const questionValidation = [
  body('quizId')
    .notEmpty().withMessage('Quiz ID is required')
    .isMongoId().withMessage('Invalid Quiz ID'),
  body('text')
    .trim()
    .notEmpty().withMessage('Question text is required'),
  body('options')
    .isArray({ min: 2 }).withMessage('At least 2 options are required'),
  body('options.*.key')
    .notEmpty().withMessage('Option key is required'),
  body('options.*.value')
    .notEmpty().withMessage('Option value is required'),
  body('correctAnswer')
    .notEmpty().withMessage('Correct answer is required'),
  handleValidationErrors,
];

module.exports = {
  registerValidation,
  loginValidation,
  quizCreationValidation,
  questionValidation,
};
