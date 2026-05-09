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
    import traceback
    try:
        subjects = Subject.query.all()
        grades = Grade.query.order_by(Grade.sort_order).all()

        grades_by_category = {}
        for g in grades:
            if g.category not in grades_by_category:
                grades_by_category[g.category] = []
            grades_by_category[g.category].append(g)

        sample_lessons = Lesson.query.order_by(Lesson.id).limit(6).all()

        stats = None
        recent_lessons = []
        if 'user_id' in session:
            from models import User
            user = User.query.get(session['user_id'])
            completed = UserLessonProgress.query.filter_by(user_id=user.id, completed=True).count()
            stats = {'lessons_completed': completed}
            recent_progress = UserLessonProgress.query.filter_by(
                user_id=user.id, completed=True
            ).order_by(UserLessonProgress.completed_at.desc()).limit(3).all()
            recent_lessons = [p.lesson for p in recent_progress if p.lesson and p.lesson.topic]

        return render_template('index.html',
                               subjects=subjects,
                               grades_by_category=grades_by_category,
                               sample_lessons=sample_lessons,
                               stats=stats,
                               recent_lessons=recent_lessons)
    except Exception as e:
        print(f"ERROR in index route: {e}")
        traceback.print_exc()
        return f"<h1>Internal Error</h1><pre>{traceback.format_exc()}</pre>", 500


@main_bp.route('/subjects')
def subjects():
    import traceback
    try:
        subjects = Subject.query.all()
        subject_data = []
        for subject in subjects:
            subject_data.append({
                'id': subject.id, 'name': subject.name, 'icon': subject.icon,
                'color': subject.color, 'description': subject.description,
                'category': getattr(subject, 'category', 'Core'),
                'quiz_count': len(subject.quizzes)
            })
        return render_template('subjects.html', subjects=subject_data)
    except Exception as e:
        print(f"ERROR in subjects route: {e}")
        traceback.print_exc()
        return f"<h1>Internal Error</h1><pre>{traceback.format_exc()}</pre>", 500


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


@main_bp.route('/debug')
def debug():
    import sys
    info = [f"Python: {sys.version}"]
    info.append(f"DB URL: {__import__('os').environ.get('DATABASE_URL', 'sqlite:///local')[:40]}...")
    try:
        from sqlalchemy import inspect
        from models import db
        inspector = inspect(db.engine)
        info.append(f"Tables: {inspector.get_table_names()}")
        info.append(f"Grades: {Grade.query.count()}")
        info.append(f"Subjects: {Subject.query.count()}")
        info.append(f"Topics: {Topic.query.count()}")
        info.append(f"Lessons: {Lesson.query.count()}")
    except Exception as e:
        info.append(f"DB Error: {e}")
    return "<pre>" + "\n".join(info) + "</pre>"


@main_bp.route('/phonics')
def phonics():
    return render_template('phonics.html', phonics=PHONICS_DATA)
