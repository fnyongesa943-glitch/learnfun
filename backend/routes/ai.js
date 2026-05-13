const express = require('express');
const OpenAI = require('openai');
const User = require('../models/User');
const Score = require('../models/Score');
const Quiz = require('../models/Quiz');
const Subject = require('../models/Subject');
const { verifyToken } = require('../middleware/auth');

const router = express.Router();

let openai = null;
if (process.env.OPENAI_API_KEY && process.env.OPENAI_API_KEY !== 'sk-your-openai-key') {
  openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  });
}

const getMockChatResponse = (message, history) => {
  const lowerMsg = message.toLowerCase();

  if (lowerMsg.includes('hello') || lowerMsg.includes('hi') || lowerMsg.includes('hey')) {
    return 'Hello there! I am your LearnFun AI tutor. How can I help you with your studies today? 😊';
  }

  if (lowerMsg.includes('math') || lowerMsg.includes('mathematics') || lowerMsg.includes('addition') || lowerMsg.includes('subtraction')) {
    return 'Great question about Mathematics! In the Kenyan CBC curriculum, mathematics helps develop problem-solving skills. Would you like me to explain a specific topic like addition, subtraction, multiplication, or division?';
  }

  if (lowerMsg.includes('english') || lowerMsg.includes('grammar') || lowerMsg.includes('reading')) {
    return 'English is an important subject in the CBC curriculum! It helps with communication skills. Would you like to practice grammar, reading comprehension, or vocabulary?';
  }

  if (lowerMsg.includes('kiswahili') || lowerMsg.includes('sarufi') || lowerMsg.includes('kusoma')) {
    return 'Kiswahili ni lugha ya taifa na ni muhimu katika mtaala wa CBC. Ningekusaidiaje leo? Unaweza kuniuza kuhusu sarufi, ufahamu, au msamiati?';
  }

  if (lowerMsg.includes('science') || lowerMsg.includes('technology') || lowerMsg.includes('experiment')) {
    return 'Science & Technology in CBC is all about understanding the world around us! From plants and animals to simple machines, what specific topic would you like to explore?';
  }

  if (lowerMsg.includes('social studies') || lowerMsg.includes('history') || lowerMsg.includes('geography') || lowerMsg.includes('community')) {
    return 'Social Studies helps us understand our community, country, and the world. In CBC, we learn about Kenya\'s history, geography, and our responsibilities as citizens. What interests you?';
  }

  if (lowerMsg.includes('cre') || lowerMsg.includes('religious') || lowerMsg.includes('christian')) {
    return 'CRE in the CBC curriculum teaches us about Christian values, the Bible, and how to live a good life. How can I help you with your CRE studies?';
  }

  if (lowerMsg.includes('grade') || lowerMsg.includes('class') || lowerMsg.includes('level')) {
    return 'The CBC curriculum has specific learning outcomes for each grade level. Let me know your grade and subject, and I can recommend appropriate topics for you!';
  }

  if (lowerMsg.includes('quiz') || lowerMsg.includes('test') || lowerMsg.includes('exam') || lowerMsg.includes('practice')) {
    return 'Ready for some practice? Quizzes are a great way to test your knowledge. Try the quizzes section in your dashboard to find exercises tailored for your grade and subjects!';
  }

  if (lowerMsg.includes('tip') || lowerMsg.includes('study') || lowerMsg.includes('how to') || lowerMsg.includes('advice')) {
    return 'Here are some study tips for CBC success: 1) Review your lessons daily 2) Practice with quizzes regularly 3) Focus on weak areas 4) Take short breaks while studying 5) Ask your teacher when stuck. Would you like more specific advice?';
  }

  if (lowerMsg.includes('help') || lowerMsg.includes('support') || lowerMsg.includes('confused')) {
    return 'No problem at all! I\'m here to help you learn. Could you tell me which subject and topic you\'re working on so I can give you the right support?';
  }

  if (lowerMsg.includes('thank')) {
    return 'You\'re welcome! Keep up the great work with your studies. Remember, every day is a chance to learn something new! 🎉';
  }

  return 'That\'s an interesting question! In the Kenyan CBC curriculum, we approach learning through hands-on experiences and critical thinking. Could you tell me more about what specific topic or subject you\'re studying so I can help you better?';
};

router.post('/chat', verifyToken, async (req, res) => {
  try {
    const { message, history = [] } = req.body;

    if (!message || !message.trim()) {
      return res.status(400).json({
        success: false,
        data: null,
        message: 'Message is required',
        error: 'Invalid input',
      });
    }

    let reply;

    if (openai) {
      const systemPrompt = {
        role: 'system',
        content: 'You are a friendly and knowledgeable AI tutor for the LearnFun educational platform. You teach students following the Kenyan CBC (Competency Based Curriculum) from Pre-Primary to Grade 9. Your subjects include Mathematics, English, Kiswahili, Science & Technology, Social Studies, CRE, Agriculture, and Life Skills. Be encouraging, use simple language appropriate for the student\'s grade level, and occasionally include emojis. Help students understand concepts, solve problems, and develop a love for learning.',
      };

      const messages = [systemPrompt];
      for (const msg of history.slice(-10)) {
        messages.push({ role: msg.role, content: msg.content });
      }
      messages.push({ role: 'user', content: message });

      const completion = await openai.chat.completions.create({
        model: 'gpt-3.5-turbo',
        messages,
        max_tokens: 500,
        temperature: 0.7,
      });

      reply = completion.choices[0]?.message?.content || 'I apologize, I could not generate a response at this time.';
    } else {
      reply = getMockChatResponse(message, history);
    }

    res.status(200).json({
      success: true,
      data: {
        reply,
        timestamp: new Date().toISOString(),
      },
      message: 'Chat response generated',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error generating chat response',
      error: error.message,
    });
  }
});

router.post('/recommend', verifyToken, async (req, res) => {
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

    const recentScores = await Score.find({ userId })
      .populate({
        path: 'quizId',
        select: 'title subjectId grade difficulty',
        populate: { path: 'subjectId', select: 'name icon color' },
      })
      .sort({ completedAt: -1 })
      .limit(20);

    const subjectPerformance = {};
    for (const score of recentScores) {
      if (!score.quizId?.subjectId) continue;
      const subId = score.quizId.subjectId._id.toString();
      if (!subjectPerformance[subId]) {
        subjectPerformance[subId] = {
          subject: score.quizId.subjectId,
          scores: [],
          totalPoints: 0,
        };
      }
      subjectPerformance[subId].scores.push(score.percentage);
      subjectPerformance[subId].totalPoints += score.pointsEarned;
    }

    const weakSubjectIds = [];
    for (const [subId, data] of Object.entries(subjectPerformance)) {
      const avg = data.scores.reduce((s, v) => s + v, 0) / data.scores.length;
      if (avg < 50) {
        weakSubjectIds.push(subId);
      }
    }

    const completedQuizIds = recentScores
      .filter(s => s.quizId)
      .map(s => s.quizId._id.toString());

    const uniqueSubjectIds = [...new Set(weakSubjectIds)];
    let recommendedQuizzes;

    if (uniqueSubjectIds.length > 0) {
      recommendedQuizzes = await Quiz.find({
        _id: { $nin: completedQuizIds },
        subjectId: { $in: uniqueSubjectIds },
        grade: user.grade,
      })
        .populate('subjectId', 'name icon color')
        .limit(3);
    }

    if (!recommendedQuizzes || recommendedQuizzes.length < 3) {
      const excludeIds = [...completedQuizIds, ...(recommendedQuizzes || []).map(r => r._id.toString())];
      const extraQuizzes = await Quiz.find({
        _id: { $nin: excludeIds },
        grade: user.grade || { $exists: true },
      })
        .populate('subjectId', 'name icon color')
        .sort({ createdAt: -1 })
        .limit(3 - (recommendedQuizzes?.length || 0));

      recommendedQuizzes = [...(recommendedQuizzes || []), ...extraQuizzes];
    }

    const result = recommendedQuizzes.map(quiz => {
      const reason = uniqueSubjectIds.includes(quiz.subjectId?._id?.toString())
        ? `Focus on improving in ${quiz.subjectId?.name} - your average needs attention`
        : `Recommended practice for Grade ${quiz.grade} students`;

      return { quiz, reason };
    });

    res.status(200).json({
      success: true,
      data: result,
      message: 'AI recommendations generated',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error generating recommendations',
      error: error.message,
    });
  }
});

router.post('/feedback', verifyToken, async (req, res) => {
  try {
    const { quizId, scoreId } = req.body;

    if (!quizId && !scoreId) {
      return res.status(400).json({
        success: false,
        data: null,
        message: 'Quiz ID or Score ID is required',
        error: 'Invalid input',
      });
    }

    let score;
    if (scoreId) {
      score = await Score.findById(scoreId)
        .populate({
          path: 'quizId',
          select: 'title grade difficulty',
          populate: { path: 'subjectId', select: 'name' },
        });
    } else {
      score = await Score.findOne({ quizId, userId: req.user._id })
        .sort({ completedAt: -1 })
        .populate({
          path: 'quizId',
          select: 'title grade difficulty',
          populate: { path: 'subjectId', select: 'name' },
        });
    }

    if (!score) {
      return res.status(404).json({
        success: false,
        data: null,
        message: 'Score not found',
        error: 'Not found',
      });
    }

    const correctCount = score.score;
    const totalQuestions = score.totalQuestions;
    const percentage = score.percentage;
    const subjectName = score.quizId?.subjectId?.name || 'Unknown';
    const quizTitle = score.quizId?.title || 'Quiz';

    let overallFeedback;
    let encouragement;
    let focusAreas = [];

    if (percentage >= 80) {
      overallFeedback = `Excellent work on "${quizTitle}"! You scored ${percentage}% in ${subjectName}.`;
      encouragement = 'You have a strong understanding of this topic. Keep up the great work! 🌟';
    } else if (percentage >= 60) {
      overallFeedback = `Good effort on "${quizTitle}"! You scored ${percentage}% in ${subjectName}.`;
      encouragement = 'You are on the right track. With a bit more practice, you can achieve even better results! 💪';
      focusAreas.push('Review the questions you got wrong and understand the correct answers');
    } else if (percentage >= 40) {
      overallFeedback = `You scored ${percentage}% on "${quizTitle}" in ${subjectName}.`;
      encouragement = 'Don\'t be discouraged! This shows us where you need to focus more.';
      focusAreas.push('Spend more time reviewing this subject');
      focusAreas.push('Practice with easier quizzes first and gradually increase difficulty');
    } else {
      overallFeedback = `You scored ${percentage}% on "${quizTitle}" in ${subjectName}.`;
      encouragement = 'Everyone learns at their own pace. Let\'s identify the areas that need more attention!';
      focusAreas.push('Start by reviewing the basic concepts of this topic');
      focusAreas.push('Ask your teacher or use the AI tutor to explain difficult concepts');
      focusAreas.push('Try the lesson materials before attempting quizzes again');
    }

    const incorrectAnswers = score.answers.filter(a => !a.correct);

    const result = {
      quizTitle,
      subject: subjectName,
      grade: score.quizId?.grade || 'N/A',
      difficulty: score.quizId?.difficulty || 'N/A',
      score: {
        correct: correctCount,
        total: totalQuestions,
        percentage,
        timeTaken: score.timeTaken,
        pointsEarned: score.pointsEarned,
      },
      feedback: overallFeedback,
      encouragement,
      focusAreas,
      incorrectCount: incorrectAnswers.length,
      completedAt: score.completedAt,
    };

    if (openai) {
      try {
        const completion = await openai.chat.completions.create({
          model: 'gpt-3.5-turbo',
          messages: [
            {
              role: 'system',
              content: 'You are an educational feedback assistant. Provide encouraging, constructive feedback for a student\'s quiz performance.',
            },
            {
              role: 'user',
              content: `Student scored ${percentage}% on a ${subjectName} quiz (${correctCount}/${totalQuestions} correct). Provide 2-3 specific improvement tips.`,
            },
          ],
          max_tokens: 300,
          temperature: 0.7,
        });

        const aiTips = completion.choices[0]?.message?.content;
        if (aiTips) {
          result.aiTips = aiTips;
        }
      } catch (aiError) {
        result.aiTips = 'Focus on understanding the concepts behind each question rather than memorizing answers.';
      }
    } else {
      result.aiTips = 'Focus on understanding the concepts behind each question rather than memorizing answers.';
    }

    res.status(200).json({
      success: true,
      data: result,
      message: 'Feedback generated successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error generating feedback',
      error: error.message,
    });
  }
});

router.post('/predict', verifyToken, async (req, res) => {
  try {
    const userId = req.user._id;

    const scores = await Score.find({ userId })
      .populate({
        path: 'quizId',
        select: 'subjectId grade difficulty',
        populate: { path: 'subjectId', select: 'name' },
      })
      .sort({ completedAt: 1 });

    if (scores.length < 3) {
      return res.status(200).json({
        success: true,
        data: {
          prediction: 'Complete at least 3 quizzes to receive a performance prediction',
          trend: 'insufficient_data',
          scoresNeeded: 3 - scores.length,
          currentAvg: scores.length > 0
            ? Math.round(scores.reduce((s, v) => s + v.percentage, 0) / scores.length)
            : 0,
        },
        message: 'Insufficient data for prediction',
        error: '',
      });
    }

    const recentScores = scores.slice(-10);
    const percentages = recentScores.map(s => s.percentage);
    const avgScore = Math.round(percentages.reduce((a, b) => a + b, 0) / percentages.length);

    const mid = Math.floor(percentages.length / 2);
    const firstHalf = percentages.slice(0, mid);
    const secondHalf = percentages.slice(mid);
    const firstAvg = firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length;
    const secondAvg = secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length;

    let trend;
    let predictedNext;
    let confidence;

    if (secondAvg > firstAvg + 5) {
      trend = 'improving';
      predictedNext = Math.min(100, avgScore + 8);
      confidence = 'high';
    } else if (secondAvg < firstAvg - 5) {
      trend = 'declining';
      predictedNext = Math.max(0, avgScore - 8);
      confidence = 'medium';
    } else {
      trend = 'stable';
      predictedNext = avgScore;
      confidence = 'medium';
    }

    const subjectPerformance = {};
    for (const score of scores) {
      if (!score.quizId?.subjectId) continue;
      const name = score.quizId.subjectId.name;
      if (!subjectPerformance[name]) {
        subjectPerformance[name] = { scores: [], trend: 'stable' };
      }
      subjectPerformance[name].scores.push(score.percentage);
    }

    const subjectPredictions = {};
    for (const [name, data] of Object.entries(subjectPerformance)) {
      if (data.scores.length >= 2) {
        const subScores = data.scores;
        const subMid = Math.floor(subScores.length / 2);
        const subFirst = subScores.slice(0, subMid).reduce((a, b) => a + b, 0) / subMid;
        const subSecond = subScores.slice(subMid).reduce((a, b) => a + b, 0) / (subScores.length - subMid);
        subjectPredictions[name] = {
          avgScore: Math.round(data.scores.reduce((a, b) => a + b, 0) / data.scores.length),
          trend: subSecond > subFirst + 5 ? 'improving' : subSecond < subFirst - 5 ? 'declining' : 'stable',
          predictedScore: Math.round((subSecond + (subSecond - subFirst) * 0.3)),
        };
      }
    }

    res.status(200).json({
      success: true,
      data: {
        overall: {
          trend,
          currentAvg: avgScore,
          predictedNextScore: Math.round(predictedNext),
          confidence,
          totalQuizzesAnalyzed: scores.length,
        },
        subjectPredictions,
        recommendations: trend === 'declining'
          ? ['Review past lessons', 'Focus on weak subjects', 'Take shorter, more frequent practice sessions']
          : trend === 'improving'
            ? ['Continue your current study routine', 'Challenge yourself with harder quizzes', 'Help classmates to reinforce learning']
            : ['Try different study methods', 'Set specific score goals for each quiz', 'Mix easy and hard topics in practice'],
      },
      message: 'Prediction generated successfully',
      error: '',
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      data: null,
      message: 'Server error generating prediction',
      error: error.message,
    });
  }
});

module.exports = router;
