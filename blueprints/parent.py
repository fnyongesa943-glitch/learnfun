"""
Parent Dashboard Blueprint - Protected analytics and settings.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Score, Quiz, Subject, UserBadge
from datetime import datetime, timedelta

parent_bp = Blueprint('parent', __name__)

# Simple parent PIN (default 1234)
PARENT_PIN = '1234'


@parent_bp.route('/')
def login():
    """Parent login page (PIN protected)."""
    # Allow direct access via ?pin=1234
    pin_param = request.args.get('pin', '')
    if pin_param == PARENT_PIN:
        session['is_parent'] = True
        return redirect(url_for('parent.dashboard'))
    return render_template('parent_login.html')


@parent_bp.route('/check', methods=['POST'])
def check_pin():
    """Verify parent PIN."""
    pin = request.form.get('pin', '').strip()
    if pin == PARENT_PIN:
        session['is_parent'] = True
        return redirect(url_for('parent.dashboard'))
    else:
        flash('Wrong PIN! Try 1234.', 'error')
        return redirect(url_for('parent.login'))


@parent_bp.route('/user/<int:user_id>')
def user_report(user_id):
    """Detailed progress report for a specific child (parent view)."""
    if not session.get('is_parent'):
        # Allow via PIN in URL
        pin_param = request.args.get('pin', '')
        if pin_param != PARENT_PIN:
            flash('Please enter PIN first.', 'warning')
            return redirect(url_for('parent.login'))
        session['is_parent'] = True

    user = User.query.get_or_404(user_id)
    scores = Score.query.filter_by(user_id=user.id).order_by(Score.completed_at.desc()).all()
    total_quizzes = len(scores)
    avg_score = int(sum(s.score for s in scores) / len(scores)) if scores else 0

    subject_progress = []
    subjects = Subject.query.all()
    for subject in subjects:
        subject_scores = Score.query.join(Quiz).filter(
            Score.user_id == user.id, Quiz.subject_id == subject.id
        ).all()
        completed = len(subject_scores)
        total_for_sub = Quiz.query.filter_by(subject_id=subject.id).count()
        best_score = max((s.score for s in subject_scores), default=0)
        subject_progress.append({
            'id': subject.id, 'name': subject.name, 'icon': subject.icon, 'color': subject.color,
            'completed': completed, 'total': total_for_sub, 'best_score': best_score,
            'percentage': int((completed / total_for_sub) * 100) if total_for_sub > 0 else 0
        })

    badges = UserBadge.query.filter_by(user_id=user.id).order_by(UserBadge.earned_at.desc()).all()

    recent_activity = []
    for score in scores[:10]:
        quiz = Quiz.query.get(score.quiz_id)
        subject = Subject.query.get(quiz.subject_id)
        recent_activity.append({
            'quiz_title': quiz.title, 'subject_name': subject.name, 'subject_icon': subject.icon,
            'score': score.score, 'points_earned': score.points_earned, 'completed_at': score.completed_at
        })

    current_level_points = user.total_points % 100
    progress_to_next = int((current_level_points / 100) * 100)

    return render_template(
        'parent_user_report.html', user=user, total_quizzes=total_quizzes, avg_score=avg_score,
        subject_progress=subject_progress, badges=badges,
        recent_activity=recent_activity, progress_to_next=progress_to_next
    )


@parent_bp.route('/dashboard')
def dashboard():
    """Parent analytics dashboard."""
    # Allow bypass if ?pin=1234 is in URL
    pin_param = request.args.get('pin', '')
    if pin_param != PARENT_PIN and not session.get('is_parent'):
        flash('Please enter PIN first.', 'warning')
        return redirect(url_for('parent.login'))
    
    session['is_parent'] = True

    # Global stats
    total_users = User.query.count()
    total_quizzes = Score.query.count()
    
    # Active in last 24 hours
    yesterday = datetime.utcnow() - timedelta(days=1)
    active_today = Score.query.filter(Score.completed_at >= yesterday).count()

    # Subject stats
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
