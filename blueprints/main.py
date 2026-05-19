"""
Main Blueprint - Home page and subject browsing.
"""
from flask import Blueprint, render_template, session
from models import Subject, Quiz, Grade, Topic, Lesson, UserLessonProgress

main_bp = Blueprint('main', __name__)

PHONICS_DATA = [
    {'letter': 'A', 'sound': 'a', 'word': 'Apple', 'emoji': '🍎', 'color': '#EF4444'},
    {'letter': 'B', 'sound': 'b', 'word': 'Ball', 'emoji': '⚽', 'color': '#2196F3'},
    {'letter': 'C', 'sound': 'k', 'word': 'Cat', 'emoji': '🐱', 'color': '#4CAF50'},
    {'letter': 'D', 'sound': 'd', 'word': 'Dog', 'emoji': '🐶', 'color': '#FF9800'},
    {'letter': 'E', 'sound': 'e', 'word': 'Elephant', 'emoji': '🐘', 'color': '#9C27B0'},
    {'letter': 'F', 'sound': 'f', 'word': 'Fish', 'emoji': '🐟', 'color': '#00BCD4'},
    {'letter': 'G', 'sound': 'g', 'word': 'Guitar', 'emoji': '🎸', 'color': '#E91E63'},
    {'letter': 'H', 'sound': 'h', 'word': 'Hat', 'emoji': '🎩', 'color': '#795548'},
    {'letter': 'I', 'sound': 'i', 'word': 'Igloo', 'emoji': '🏠', 'color': '#03A9F4'},
    {'letter': 'J', 'sound': 'j', 'word': 'Juice', 'emoji': '🧃', 'color': '#FF5722'},
    {'letter': 'K', 'sound': 'k', 'word': 'Kite', 'emoji': '🪁', 'color': '#8BC34A'},
    {'letter': 'L', 'sound': 'l', 'word': 'Lion', 'emoji': '🦁', 'color': '#FFC107'},
    {'letter': 'M', 'sound': 'm', 'word': 'Moon', 'emoji': '🌙', 'color': '#3F51B5'},
    {'letter': 'N', 'sound': 'n', 'word': 'Nest', 'emoji': '🐦', 'color': '#009688'},
    {'letter': 'O', 'sound': 'o', 'word': 'Octopus', 'emoji': '🐙', 'color': '#673AB7'},
    {'letter': 'P', 'sound': 'p', 'word': 'Pig', 'emoji': '🐷', 'color': '#F48FB1'},
    {'letter': 'Q', 'sound': 'kw', 'word': 'Queen', 'emoji': '👸', 'color': '#CDDC39'},
    {'letter': 'R', 'sound': 'r', 'word': 'Rain', 'emoji': '🌧️', 'color': '#607D8B'},
    {'letter': 'S', 'sound': 's', 'word': 'Sun', 'emoji': '☀️', 'color': '#FFEB3B'},
    {'letter': 'T', 'sound': 't', 'word': 'Tree', 'emoji': '🌳', 'color': '#4CAF50'},
    {'letter': 'U', 'sound': 'u', 'word': 'Umbrella', 'emoji': '☂️', 'color': '#2196F3'},
    {'letter': 'V', 'sound': 'v', 'word': 'Violin', 'emoji': '🎻', 'color': '#D84315'},
    {'letter': 'W', 'sound': 'w', 'word': 'Water', 'emoji': '💧', 'color': '#00BCD4'},
    {'letter': 'X', 'sound': 'ks', 'word': 'Box', 'emoji': '📦', 'color': '#FF9800'},
    {'letter': 'Y', 'sound': 'y', 'word': 'Yellow', 'emoji': '💛', 'color': '#FFEB3B'},
    {'letter': 'Z', 'sound': 'z', 'word': 'Zebra', 'emoji': '🦓', 'color': '#9E9E9E'},
]


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    import traceback
    try:
        subjects = Subject.query.all()
        grades = Grade.query.order_by(Grade.sort_order).all()

        # Track which grades have content (topics)
        from models import Topic
        grade_counts = {}
        for g in grades:
            try:
                grade_counts[g.id] = Topic.query.filter_by(grade_id=g.id).count()
            except Exception:
                grade_counts[g.id] = 0

        grades_by_category = {}
        for g in grades:
            cat = getattr(g, 'category', 'General')
            if cat not in grades_by_category:
                grades_by_category[cat] = []
            grades_by_category[cat].append(g)

        sample_lessons = []
        try:
            sample_lessons = Lesson.query.order_by(Lesson.id).limit(6).all()
        except Exception:
            pass

        stats = None
        recent_lessons = []
        if 'user_id' in session:
            from models import User
            try:
                user = User.query.get(session['user_id'])
                if user is not None:
                    completed = UserLessonProgress.query.filter_by(user_id=user.id, completed=True).count()
                    stats = {'lessons_completed': completed}
                    recent_progress = UserLessonProgress.query.filter_by(
                        user_id=user.id, completed=True
                    ).order_by(UserLessonProgress.completed_at.desc()).limit(3).all()
                    recent_lessons = [p.lesson for p in recent_progress if p.lesson and getattr(p.lesson, 'topic', None)]
            except Exception:
                pass

        return render_template('index.html',
                               subjects=subjects,
                               grades_by_category=grades_by_category,
                               sample_lessons=sample_lessons,
                               stats=stats,
                               recent_lessons=recent_lessons,
                               grade_counts=grade_counts)
    except Exception as e:
        import logging
        logging.error(f"ERROR in index route: {e}")
        logging.error(traceback.format_exc())
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
        topics_by_grade[grade_name].append({
            'topic': topic,
            'quizzes': Quiz.query.filter_by(topic_id=topic.id).all()
        })

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
