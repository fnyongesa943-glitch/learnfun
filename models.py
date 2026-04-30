from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """User model for storing account information."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    avatar = db.Column(db.String(20), default='bear')  # Avatar type
    total_points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    scores = db.relationship('Score', backref='user', lazy=True, cascade='all, delete-orphan')
    badges = db.relationship('UserBadge', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def add_points(self, points):
        """Add points and check for level up."""
        self.total_points += points
        # Level up every 100 points
        new_level = (self.total_points // 100) + 1
        if new_level > self.level:
            self.level = new_level
            return True  # Level up occurred
        return False

    def to_dict(self):
        """Convert user to dictionary for API responses."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'total_points': self.total_points,
            'level': self.level,
            'created_at': self.created_at.isoformat()
        }


class Subject(db.Model):
    """Subject model for different learning categories."""
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(20), nullable=False)  # Emoji icon
    color = db.Column(db.String(20), nullable=False)  # Primary color
    description = db.Column(db.String(200), default='')
    quizzes = db.relationship('Quiz', backref='subject', lazy=True)

    def to_dict(self):
        """Convert subject to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'color': self.color,
            'description': self.description,
            'quiz_count': len(self.quizzes)
        }


class Quiz(db.Model):
    """Quiz model for storing quiz information."""
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    difficulty = db.Column(db.String(20), default='easy')  # easy, medium, hard
    description = db.Column(db.String(200), default='')
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Convert quiz to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'subject_id': self.subject_id,
            'difficulty': self.difficulty,
            'description': self.description,
            'question_count': len(self.questions)
        }


class Question(db.Model):
    """Question model for quiz questions."""
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', or 'D'
    explanation = db.Column(db.String(200), default='')
    points = db.Column(db.Integer, default=10)

    def to_dict(self):
        """Convert question to dictionary (excludes correct answer for security)."""
        return {
            'id': self.id,
            'text': self.text,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'explanation': self.explanation,
            'points': self.points
        }


class Score(db.Model):
    """Score model for tracking quiz attempts."""
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)  # Percentage (0-100)
    points_earned = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to quiz
    quiz = db.relationship('Quiz', backref='scores')

    def to_dict(self):
        """Convert score to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'quiz_id': self.quiz_id,
            'score': self.score,
            'points_earned': self.points_earned,
            'completed_at': self.completed_at.isoformat()
        }


class UserBadge(db.Model):
    """UserBadge model for tracking earned badges."""
    __tablename__ = 'user_badges'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_name = db.Column(db.String(50), nullable=False)
    badge_icon = db.Column(db.String(20), nullable=False)
    badge_description = db.Column(db.String(100), default='')
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert badge to dictionary."""
        return {
            'id': self.id,
            'badge_name': self.badge_name,
            'badge_icon': self.badge_icon,
            'badge_description': self.badge_description,
            'earned_at': self.earned_at.isoformat()
        }


# Badge definitions - available badges users can earn
BADGE_DEFINITIONS = {
    'first_quiz': {'icon': '🌟', 'name': 'First Steps', 'description': 'Complete your first quiz'},
    'perfect_score': {'icon': '💯', 'name': 'Perfect Score', 'description': 'Get 100% on any quiz'},
    'math_star': {'icon': '🔢', 'name': 'Math Star', 'description': 'Complete 3 math quizzes'},
    'reading_pro': {'icon': '📚', 'name': 'Reading Pro', 'description': 'Complete 3 reading quizzes'},
    'science_wiz': {'icon': '🔬', 'name': 'Science Wizard', 'description': 'Complete 3 science quizzes'},
    'five_quiz': {'icon': '🎯', 'name': 'Quiz Master', 'description': 'Complete 5 quizzes'},
    'ten_quiz': {'icon': '🏆', 'name': 'Champion', 'description': 'Complete 10 quizzes'},
    'level_5': {'icon': '🚀', 'name': 'Rocket Learner', 'description': 'Reach level 5'},
}
