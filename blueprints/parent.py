"""
Parent Dashboard Blueprint - Monitor your child's learning progress.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Score, Quiz, Subject, UserBadge
from datetime import datetime, timedelta

parent_bp = Blueprint('parent', __name__)


@parent_bp.route('/')
def login():
    """Parent login page - enter email + PIN to see your children."""
    pin_param = request.args.get('pin', '')
    email_param = request.args.get('email', '')
    if pin_param and email_param:
        children = User.query.filter_by(parent_email=email_param).all()
        if children:
            session['parent_email'] = email_param
            session['is_parent'] = True
            return redirect(url_for('parent.dashboard'))
    if pin_param == '1234' and email_param:
        session['parent_email'] = email_param
        session['is_parent'] = True
        return redirect(url_for('parent.dashboard'))
    return render_template('parent_login.html')


@parent_bp.route('/check', methods=['POST'])
def check_pin():
    """Verify parent access with email and PIN."""
    email = request.form.get('email', '').strip().lower()
    pin = request.form.get('pin', '').strip()

    if not email:
        flash('Please enter your email address.', 'error')
        return redirect(url_for('parent.login'))

    if pin == '1234':
        # Check if any children are linked to this email
        children = User.query.filter_by(parent_email=email).all()
        session['parent_email'] = email
        session['is_parent'] = True
        if not children:
            flash('No children linked to this email yet. Ask your child to add your email in their Profile settings.', 'warning')
        return redirect(url_for('parent.dashboard'))
    else:
        flash('Wrong PIN! Try 1234.', 'error')
        return redirect(url_for('parent.login'))


@parent_bp.route('/user/<int:user_id>')
def user_report(user_id):
    """Detailed progress report for a specific child."""
    if not session.get('is_parent'):
        flash('Please log in as a parent first.', 'warning')
        return redirect(url_for('parent.login'))

    parent_email = session.get('parent_email', '')
    user = User.query.get_or_404(user_id)

    # Only allow viewing children linked to this parent
    if user.parent_email != parent_email:
        flash('This child is not linked to your account.', 'error')
        return redirect(url_for('parent.dashboard'))

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

    # Lesson progress
    from models import UserLessonProgress
    lessons_completed = UserLessonProgress.query.filter_by(user_id=user.id, completed=True).count()

    return render_template(
        'parent_user_report.html', user=user, total_quizzes=total_quizzes, avg_score=avg_score,
        subject_progress=subject_progress, badges=badges,
        recent_activity=recent_activity, progress_to_next=progress_to_next,
        lessons_completed=lessons_completed
    )


@parent_bp.route('/dashboard')
def dashboard():
    """Parent dashboard showing only linked children."""
    if not session.get('is_parent'):
        flash('Please log in as a parent first.', 'warning')
        return redirect(url_for('parent.login'))

    parent_email = session.get('parent_email', '')

    # Get only children linked to this parent
    children = User.query.filter_by(parent_email=parent_email).order_by(User.created_at.desc()).all()

    child_stats = []
    for child in children:
        quiz_count = Score.query.filter_by(user_id=child.id).count()
        avg = int(sum(s.score for s in Score.query.filter_by(user_id=child.id)) / quiz_count) if quiz_count else 0
        from models import UserLessonProgress
        lessons_done = UserLessonProgress.query.filter_by(user_id=child.id, completed=True).count()
        badges_count = UserBadge.query.filter_by(user_id=child.id).count()
        child_stats.append({
            'user': child,
            'quiz_count': quiz_count,
            'avg_score': avg,
            'lessons_done': lessons_done,
            'badges_count': badges_count
        })

    # Subject popularity among children
    subject_stats = []
    subjects = Subject.query.all()
    for sub in subjects:
        count = Score.query.join(Quiz).filter(Quiz.subject_id == sub.id).count()
        subject_stats.append({'name': sub.name, 'icon': sub.icon, 'count': count, 'color': sub.color})

    total_quizzes = sum(cs['quiz_count'] for cs in child_stats)

    return render_template(
        'parent_dashboard.html',
        child_stats=child_stats,
        subject_stats=subject_stats,
        total_quizzes=total_quizzes,
        parent_email=parent_email
    )


@parent_bp.route('/logout')
def logout():
    session.pop('is_parent', None)
    session.pop('parent_email', None)
    return redirect(url_for('parent.login'))
