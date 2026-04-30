"""
Parent Dashboard Blueprint - Protected analytics and settings.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Score, Quiz, Subject, UserBadge

parent_bp = Blueprint('parent', __name__)

# Simple parent PIN (default 1234)
PARENT_PIN = '1234'


@parent_bp.route('/')
def login():
    """Parent login page (PIN protected)."""
    return render_template('parent_login.html')


@parent_bp.route('/check', methods=['POST'])
def check_pin():
    """Verify parent PIN."""
    pin = request.form.get('pin', '')
    if pin == PARENT_PIN:
        session['is_parent'] = True
        return redirect(url_for('parent.dashboard'))
    else:
        flash('Wrong PIN!', 'error')
        return redirect(url_for('parent.login'))


@parent_bp.route('/dashboard')
def dashboard():
    """Parent analytics dashboard."""
    if not session.get('is_parent'):
        flash('Please enter PIN first.', 'warning')
        return redirect(url_for('parent.login'))

    # Global stats
    total_users = User.query.count()
    total_quizzes = Score.query.count()
    active_today = Score.query.filter(
        Score.completed_at >= db.func.date_sub(db.func.now(), interval=1)
    ).count() if hasattr(db.func, 'date_sub') else 0

    # Top subjects
    subject_stats = []
    subjects = Subject.query.all()
    for sub in subjects:
        count = Score.query.join(Quiz).filter(Quiz.subject_id == sub.id).count()
        subject_stats.append({'name': sub.name, 'icon': sub.icon, 'count': count, 'color': sub.color})

    # Recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()

    return render_template(
        'parent_dashboard.html',
        total_users=total_users,
        total_quizzes=total_quizzes,
        active_today=active_today,
        subject_stats=subject_stats,
        recent_users=recent_users
    )


@parent_bp.route('/logout')
def logout():
    session.pop('is_parent', None)
    return redirect(url_for('parent.login'))
