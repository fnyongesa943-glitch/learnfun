"""
Main Blueprint - Home page and subject browsing.
"""
from flask import Blueprint, render_template
from models import Subject, Quiz

main_bp = Blueprint('main', __name__)


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
