"""
Main Blueprint - Home page and subject browsing.
"""
from flask import Blueprint, render_template
from models import Subject, Quiz

main_bp = Blueprint('main', __name__)

# Phonics data: letter, sound, word, emoji
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
    """Home page - welcome screen with subject overview."""
    subjects = Subject.query.all()
    return render_template('index.html', subjects=subjects)


@main_bp.route('/subjects')
def subjects():
    """List all subjects with quiz counts."""
    subjects = Subject.query.all()
    subject_data = []
    for subject in subjects:
        subject_data.append({
            'id': subject.id,
            'name': subject.name,
            'icon': subject.icon,
            'color': subject.color,
            'description': subject.description,
            'quiz_count': len(subject.quizzes)
        })
    return render_template('subjects.html', subjects=subject_data)


@main_bp.route('/subjects/<int:subject_id>')
def subject_detail(subject_id):
    """Show all quizzes for a specific subject."""
    subject = Subject.query.get_or_404(subject_id)
    quizzes = Quiz.query.filter_by(subject_id=subject_id).all()
    return render_template('subject_detail.html', subject=subject, quizzes=quizzes)


@main_bp.route('/phonics')
def phonics():
    """Interactive phonics chart for young learners."""
    return render_template('phonics.html', phonics=PHONICS_DATA)
