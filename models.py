from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    avatar = db.Column(db.String(20), default='bear')
    avatar_frame = db.Column(db.String(20), default='none')
    total_points = db.Column(db.Integer, default=0)
    coins = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    streak_days = db.Column(db.Integer, default=0)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    parent_pin = db.Column(db.String(4), default='0000')
    parent_email = db.Column(db.String(120), default='')
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    scores = db.relationship('Score', backref='user', lazy=True, cascade='all, delete-orphan')
    badges = db.relationship('UserBadge', backref='user', lazy=True, cascade='all, delete-orphan')
    owned_items = db.relationship('UserOwnedItem', backref='user', lazy=True, cascade='all, delete-orphan')
    lesson_progress = db.relationship('UserLessonProgress', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_streak(self):
        today = datetime.utcnow().date()
        if self.last_active:
            last = self.last_active.date()
            if last == today:
                return False
            elif (today - last).days == 1:
                self.streak_days += 1
                self.coins += self.streak_days
                return True
            else:
                self.streak_days = 1
                self.coins += 1
                return True
        else:
            self.streak_days = 1
            self.coins += 1
            return True

    def add_points(self, points):
        self.total_points += points
        self.coins += int(points / 2)
        new_level = (self.total_points // 100) + 1
        if new_level > self.level:
            self.level = new_level
            return True
        return False

    def get_level_name(self):
        """Return themed level name based on total points."""
        if self.total_points <= 50:
            return 'Beginner'
        elif self.total_points <= 150:
            return 'Explorer'
        else:
            return 'Genius'

    def get_level_progress(self):
        """Return progress percentage to next level."""
        if self.total_points <= 50:
            return int((self.total_points / 50) * 100)
        elif self.total_points <= 150:
            return int(((self.total_points - 50) / 100) * 100)
        else:
            return min(100, int(((self.total_points - 150) / 350) * 100))

    def get_next_level_threshold(self):
        """Return points needed for next level."""
        if self.total_points <= 50:
            return 50
        elif self.total_points <= 150:
            return 150
        else:
            return 500

    def to_dict(self):
        return {
            'id': self.id, 'username': self.username, 'email': self.email,
            'avatar': self.avatar, 'total_points': self.total_points,
            'coins': self.coins, 'level': self.level,
            'streak_days': self.streak_days, 'created_at': self.created_at.isoformat()
        }


class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level_code = db.Column(db.String(10), unique=True, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    icon = db.Column(db.String(20), default='📚')
    color = db.Column(db.String(20), default='#6366F1')
    sort_order = db.Column(db.Integer, default=0)

    topics = db.relationship('Topic', backref='grade', lazy=True)

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'level_code': self.level_code,
            'category': self.category, 'icon': self.icon, 'color': self.color
        }


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), default='')
    category = db.Column(db.String(30), default='Core')
    quizzes = db.relationship('Quiz', backref='subject', lazy=True)
    topics = db.relationship('Topic', backref='subject', lazy=True)

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'icon': self.icon,
            'color': self.color, 'description': self.description,
            'category': self.category, 'quiz_count': len(self.quizzes)
        }


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200), default='')
    icon = db.Column(db.String(20), default='📖')
    order_number = db.Column(db.Integer, default=0)
    difficulty = db.Column(db.String(20), default='easy')
    estimated_minutes = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    lessons = db.relationship('Lesson', backref='topic', lazy=True, cascade='all, delete-orphan',
                              order_by='Lesson.order_number')

    def lesson_count(self):
        return len(self.lessons)

    def total_points(self):
        return sum(l.points_earned for l in self.lessons)

    def to_dict(self):
        return {
            'id': self.id, 'subject_id': self.subject_id, 'grade_id': self.grade_id,
            'title': self.title, 'subtitle': self.subtitle, 'icon': self.icon,
            'order_number': self.order_number, 'difficulty': self.difficulty,
            'lesson_count': self.lesson_count()
        }


class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    key_points = db.Column(db.Text, default='[]')
    examples = db.Column(db.Text, default='[]')
    did_you_know = db.Column(db.String(300), default='')
    definition = db.Column(db.String(200), default='')
    image_emoji = db.Column(db.String(20), default='📖')
    order_number = db.Column(db.Integer, default=0)
    points_earned = db.Column(db.Integer, default=15)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_key_points(self):
        return json.loads(self.key_points) if self.key_points else []

    def get_examples(self):
        return json.loads(self.examples) if self.examples else []

    def to_dict(self):
        return {
            'id': self.id, 'topic_id': self.topic_id, 'title': self.title,
            'order_number': self.order_number, 'points_earned': self.points_earned
        }


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    difficulty = db.Column(db.String(20), default='easy')
    description = db.Column(db.String(200), default='')
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=True)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=True)
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')

    lesson = db.relationship('Lesson', backref='quizzes')
    grade = db.relationship('Grade', backref='quizzes')
    topic = db.relationship('Topic', backref='quizzes')

    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'subject_id': self.subject_id,
            'difficulty': self.difficulty, 'description': self.description,
            'question_count': len(self.questions)
        }


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)
    explanation = db.Column(db.String(200), default='')
    hint = db.Column(db.String(200), default='')
    points = db.Column(db.Integer, default=10)

    def to_dict(self):
        return {
            'id': self.id, 'text': self.text, 'option_a': self.option_a,
            'option_b': self.option_b, 'option_c': self.option_c,
            'option_d': self.option_d, 'explanation': self.explanation,
            'hint': self.hint, 'points': self.points
        }


class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    points_earned = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    quiz = db.relationship('Quiz', backref='scores')

    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'quiz_id': self.quiz_id,
                'score': self.score, 'points_earned': self.points_earned,
                'completed_at': self.completed_at.isoformat()}


class UserLessonProgress(db.Model):
    __tablename__ = 'user_lesson_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, nullable=True)

    lesson = db.relationship('Lesson', backref='user_progress')

    def to_dict(self):
        return {
            'id': self.id, 'user_id': self.user_id, 'lesson_id': self.lesson_id,
            'completed': self.completed, 'score': self.score,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class UserBadge(db.Model):
    __tablename__ = 'user_badges'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_name = db.Column(db.String(50), nullable=False)
    badge_icon = db.Column(db.String(20), nullable=False)
    badge_description = db.Column(db.String(100), default='')
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)


class ShopItem(db.Model):
    __tablename__ = 'shop_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(20), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, default=50)
    description = db.Column(db.String(100), default='')


class UserOwnedItem(db.Model):
    __tablename__ = 'user_owned_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('shop_items.id'), nullable=False)
    purchased_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)
    item = db.relationship('ShopItem', backref='owners')


class Story(db.Model):
    __tablename__ = 'stories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    story_type = db.Column(db.String(50), nullable=False)
    age_range = db.Column(db.String(20), default='6-12')
    reading_time = db.Column(db.Integer, default=5)
    language = db.Column(db.String(10), default='en')
    related_subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=True)
    points_earned = db.Column(db.Integer, default=15)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    related_subject = db.relationship('Subject', backref='stories')


class UserStoryRead(db.Model):
    __tablename__ = 'user_story_reads'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    read_at = db.Column(db.DateTime, default=datetime.utcnow)
    points_awarded = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref='read_stories')
    story = db.relationship('Story', backref='read_by')


class StoryProgress(db.Model):
    __tablename__ = 'story_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    stage_id = db.Column(db.Integer, db.ForeignKey('adventure_stages.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, nullable=True)
    attempts = db.Column(db.Integer, default=0)
    user = db.relationship('User', backref='story_progress')
    stage = db.relationship('AdventureStage', backref='user_progress')


class AdventureStage(db.Model):
    __tablename__ = 'adventure_stages'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), default='')
    theme = db.Column(db.String(30), default='jungle')
    order_number = db.Column(db.Integer, default=0)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    points_reward = db.Column(db.Integer, default=20)
    is_boss = db.Column(db.Boolean, default=False)
    quiz = db.relationship('Quiz', backref='adventure_stage')

    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'description': self.description,
            'theme': self.theme, 'order_number': self.order_number,
            'quiz_id': self.quiz_id, 'points_reward': self.points_reward,
            'is_boss': self.is_boss
        }


BADGE_DEFINITIONS = {
    'first_quiz': {'icon': '🌟', 'name': 'First Steps', 'description': 'Complete your first quiz'},
    'perfect_score': {'icon': '💯', 'name': 'Perfect Score', 'description': 'Get 100% on any quiz'},
    'math_star': {'icon': '🔢', 'name': 'Math Star', 'description': 'Complete 3 math quizzes'},
    'reading_pro': {'icon': '📚', 'name': 'Reading Pro', 'description': 'Complete 3 reading quizzes'},
    'science_wiz': {'icon': '🔬', 'name': 'Science Wizard', 'description': 'Complete 3 science quizzes'},
    'geo_explorer': {'icon': '🌍', 'name': 'Geo Explorer', 'description': 'Complete 3 geography quizzes'},
    'five_quiz': {'icon': '🎯', 'name': 'Quiz Master', 'description': 'Complete 5 quizzes'},
    'ten_quiz': {'icon': '🏆', 'name': 'Champion', 'description': 'Complete 10 quizzes'},
    'level_5': {'icon': '🚀', 'name': 'Rocket Learner', 'description': 'Reach level 5'},
    'streak_3': {'icon': '🔥', 'name': 'On Fire', 'description': 'Maintain a 3-day streak'},
    'streak_7': {'icon': '💎', 'name': 'Dedicated', 'description': 'Maintain a 7-day streak'},
    'story_lover': {'icon': '📖', 'name': 'Story Lover', 'description': 'Read 5 stories'},
    'story_master': {'icon': '📚', 'name': 'Story Master', 'description': 'Read 15 stories'},
    'imagination_king': {'icon': '🦄', 'name': 'Imagination King', 'description': 'Read 5 imagination stories'},
    'first_lesson': {'icon': '📗', 'name': 'First Lesson', 'description': 'Complete your first lesson'},
    'five_lessons': {'icon': '📚', 'name': 'Eager Learner', 'description': 'Complete 5 lessons'},
    'topic_master': {'icon': '🏅', 'name': 'Topic Master', 'description': 'Complete all lessons in a topic'},
}
