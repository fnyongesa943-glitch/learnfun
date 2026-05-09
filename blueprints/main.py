"""
Main Blueprint - Home page and subject browsing.
"""
from flask import Blueprint, render_template, session
from models import Subject, Quiz, Grade, Topic, Lesson, UserLessonProgress

main_bp = Blueprint('main', __name__)

PHONICS_DATA = [
    {'letter': 'A', 'sound': 'ah', 'word': 'Apple', 'emoji': '🍎'},
    {'letter': 'B', 'sound': 'buh', 'word': 'Ball', 'emoji': '⚽'},
    {'letter': 'C', 'sound': 'kuh', 'word': 'Cat', 'emoji': '🐱'},
    {'letter': 'D', 'sound': 'duh', 'word': 'Dog', 'emoji': '🐶'},
    {'letter': 'E', 'sound': 'eh', 'word': 'Elephant', 'emoji': '🐘'},
    {'letter': 'F', 'sound': 'fff', 'word': 'Fish', 'emoji': '🐟'},
    {'letter': 'G', 'sound': 'guh', 'word': 'Guitar', 'emoji': '🎸'},
    {'letter': 'H', 'sound': 'hhh', 'word': 'Hat', 'emoji': '🎩'},
    {'letter': 'I', 'sound': 'ih', 'word': 'Igloo', 'emoji': '🏔️'},
    {'letter': 'J', 'sound': 'jjj', 'word': 'Juice', 'emoji': '🧃'},
    {'letter': 'K', 'sound': 'kuh', 'word': 'Kite', 'emoji': '🪁'},
    {'letter': 'L', 'sound': 'lll', 'word': 'Lion', 'emoji': '🦁'},
    {'letter': 'M', 'sound': 'mmm', 'word': 'Moon', 'emoji': '🌙'},
    {'letter': 'N', 'sound': 'nnn', 'word': 'Nest', 'emoji': '🐦'},
    {'letter': 'O', 'sound': 'oh', 'word': 'Octopus', 'emoji': '🐙'},
    {'letter': 'P', 'sound': 'puh', 'word': 'Pig', 'emoji': '🐷'},
    {'letter': 'Q', 'sound': 'kuh', 'word': 'Queen', 'emoji': '👸'},
    {'letter': 'R', 'sound': 'rrr', 'word': 'Rain', 'emoji': '🌧️'},
    {'letter': 'S', 'sound': 'sss', 'word': 'Sun', 'emoji': '☀️'},
    {'letter': 'T', 'sound': 'tuh', 'word': 'Tree', 'emoji': '🌳'},
    {'letter': 'U', 'sound': 'uh', 'word': 'Umbrella', 'emoji': '☂️'},
    {'letter': 'V', 'sound': 'vvv', 'word': 'Violin', 'emoji': '🎻'},
    {'letter': 'W', 'sound': 'www', 'word': 'Water', 'emoji': '💧'},
    {'letter': 'X', 'sound': 'ks', 'word': 'Box', 'emoji': '📦'},
    {'letter': 'Y', 'sound': 'yyy', 'word': 'Yellow', 'emoji': '💛'},
    {'letter': 'Z', 'sound': 'zzz', 'word': 'Zebra', 'emoji': '🦓'},
]


@main_bp.route('/')
def index():
    subjects = Subject.query.all()
    grades = Grade.query.order_by(Grade.sort_order).all()

    # Group grades by category
    grades_by_category = {}
    for g in grades:
        if g.category not in grades_by_category:
            grades_by_category[g.category] = []
        grades_by_category[g.category].append(g)

    # Sample lessons for homepage
    sample_lessons = Lesson.query.order_by(Lesson.id).limit(6).all()

    # Stats and recent lessons for logged-in user
    stats = None
    recent_lessons = []
    if 'user_id' in session:
        from models import User
        user = User.query.get(session['user_id'])
        completed = UserLessonProgress.query.filter_by(user_id=user.id, completed=True).count()
        stats = {'lessons_completed': completed}

        # Get recent completed lessons
        recent_progress = UserLessonProgress.query.filter_by(
            user_id=user.id, completed=True
        ).order_by(UserLessonProgress.completed_at.desc()).limit(3).all()
        recent_lessons = [p.lesson for p in recent_progress]

    return render_template('index.html',
                           subjects=subjects,
                           grades_by_category=grades_by_category,
                           sample_lessons=sample_lessons,
                           stats=stats,
                           recent_lessons=recent_lessons)


@main_bp.route('/subjects')
def subjects():
    subjects = Subject.query.all()
    subject_data = []
    for subject in subjects:
        subject_data.append({
            'id': subject.id, 'name': subject.name, 'icon': subject.icon,
            'color': subject.color, 'description': subject.description,
            'category': subject.category, 'quiz_count': len(subject.quizzes)
        })
    return render_template('subjects.html', subjects=subject_data)


@main_bp.route('/subjects/<int:subject_id>')
def subject_detail(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    quizzes = Quiz.query.filter_by(subject_id=subject_id).all()

    # Get topics grouped by grade for this subject
    topics = Topic.query.filter_by(subject_id=subject_id).order_by(Topic.grade_id, Topic.order_number).all()
    topics_by_grade = {}
    for topic in topics:
        grade_name = topic.grade.name if topic.grade else 'General'
        if grade_name not in topics_by_grade:
            topics_by_grade[grade_name] = []
        topics_by_grade[grade_name].append(topic)

    return render_template('subject_detail.html',
                           subject=subject, quizzes=quizzes,
                           topics_by_grade=topics_by_grade)


@main_bp.route('/phonics')
def phonics():
    return render_template('phonics.html', phonics=PHONICS_DATA)
