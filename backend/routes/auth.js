const express = require('express');
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const { verifyToken } = require('../middleware/auth');
const { registerValidation, loginValidation } = require('../middleware/validation');

const router = express.Router();

const generateToken = (userId) => {
  return jwt.sign({ id: userId }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRES_IN || '7d',
  });
};

router.post('/register', registerValidation, async (req, res) => {
  try {
    const { name, email, password, grade, role } = req.body;

    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({
        success: false,
        data: null,
        message: 'User with this email already exists',
        error: 'Duplicate email',
      });
    }

    const user = await User.create({
      name,
      email,
      password,
      grade: grade || undefined,
      role: role || 'student',
    });

    const token = generateToken(user._id);

    res.status(201).json({
      success: true,
      data: {
        token,
        user: {
          id: user._id,
          name: user.name,
          email: user.email,
          role: user.role,
          grade: user.grade,
          points: user.points,
          coins: user.coins,
          level: user.level,
          streak: user.streak,
          avatar: user.avatar,
        },
      },
      message: 'Registration successful',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error during registration',
      error: error.message,
    });
  }
});

router.post('/login', loginValidation, async (req, res) => {
  try {
    const { email, password } = req.body;

    const user = await User.findOne({ email }).select('+password');
    if (!user) {
      return res.status(401).json({
        success: false,
        data: null,
        message: 'Invalid email or password',
        error: 'Authentication failed',
      });
    }

    const isMatch = await user.matchPassword(password);
    if (!isMatch) {
      return res.status(401).json({
        success: false,
        data: null,
        message: 'Invalid email or password',
        error: 'Authentication failed',
      });
    }

    const token = generateToken(user._id);

    res.status(200).json({
      success: true,
      data: {
        token,
        user: {
          id: user._id,
          name: user.name,
          email: user.email,
          role: user.role,
          grade: user.grade,
          points: user.points,
          coins: user.coins,
          level: user.level,
          streak: user.streak,
          avatar: user.avatar,
        },
      },
      message: 'Login successful',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error during login',
      error: error.message,
    });
  }
});

router.post('/google', async (req, res) => {
  try {
    const { email, name, googleId, avatar } = req.body;

    if (!email || !googleId) {
      return res.status(400).json({
        success: false,
        data: null,
        message: 'Email and Google ID are required',
        error: 'Missing fields',
      });
    }

    let user = await User.findOne({ $or: [{ email }, { googleId }] });

    if (user) {
      if (!user.googleId) {
        user.googleId = googleId;
        await user.save();
      }
    } else {
      user = await User.create({
        name: name || 'Google User',
        email,
        password: googleId + process.env.JWT_SECRET,
        googleId,
        avatar: avatar || '',
      });
    }

    const token = generateToken(user._id);

    res.status(200).json({
      success: true,
      data: {
        token,
        user: {
          id: user._id,
          name: user.name,
          email: user.email,
          role: user.role,
          grade: user.grade,
          points: user.points,
          coins: user.coins,
          level: user.level,
          streak: user.streak,
          avatar: user.avatar,
        },
      },
      message: 'Google login successful',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error during Google login',
      error: error.message,
    });
  }
});

router.get('/me', verifyToken, async (req, res) => {
  try {
    const user = await User.findById(req.user._id);

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
      data: {
        id: user._id,
        name: user.name,
        email: user.email,
        role: user.role,
        grade: user.grade,
        points: user.points,
        coins: user.coins,
        level: user.level,
        streak: user.streak,
        avatar: user.avatar,
        achievements: user.achievements,
        lastActive: user.lastActive,
        createdAt: user.createdAt,
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

router.put('/profile', verifyToken, async (req, res) => {
  try {
    const { name, grade, avatar } = req.body;

    const updateFields = {};
    if (name) updateFields.name = name;
    if (grade) updateFields.grade = grade;
    if (avatar !== undefined) updateFields.avatar = avatar;

    const user = await User.findByIdAndUpdate(req.user._id, updateFields, {
      new: true,
      runValidators: true,
    });

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
      data: {
        id: user._id,
        name: user.name,
        email: user.email,
        role: user.role,
        grade: user.grade,
        points: user.points,
        coins: user.coins,
        level: user.level,
        streak: user.streak,
        avatar: user.avatar,
      },
      message: 'Profile updated successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error updating profile',
      error: error.message,
    });
  }
});

module.exports = router;
