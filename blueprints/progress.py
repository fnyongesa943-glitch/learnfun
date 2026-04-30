"""
Progress Blueprint - User dashboard and progress tracking.
"""
from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import db, User, Score, Quiz, Subject, UserBadge

progress_bp = Blueprint('progress', __name__)


@progress_bp.route('/')
def dashboard():
    """User progress dashboard."""
    if 'user_id' not in session:
        flash('Please log in to see progress.', 'warning')
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    
    # Update streak on visit
    user.update_streak()
    db.session.commit()

    scores = Score.query.filter_by(user_id=user.id).order_by(Score.completed_at.desc()).all()
    total_quizzes = len(scores)
    avg_score = int(sum(s.score for s in scores) / len(scores)) if scores else 0

    # Progress by subject
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

    # Leaderboard: Top 10 users by points
    leaderboard = User.query.order_by(User.total_points.desc()).limit(10).all()

    recent_activity = []
    for score in scores[:5]:
        quiz = Quiz.query.get(score.quiz_id)
        subject = Subject.query.get(quiz.subject_id)
        recent_activity.append({
            'quiz_title': quiz.title, 'subject_name': subject.name, 'subject_icon': subject.icon,
            'score': score.score, 'points_earned': score.points_earned, 'completed_at': score.completed_at
        })

    current_level_points = user.total_points % 100
    progress_to_next = int((current_level_points / 100) * 100)

    return render_template(
        'progress.html', user=user, total_quizzes=total_quizzes, avg_score=avg_score,
        subject_progress=subject_progress, badges=badges, leaderboard=enumerate(leaderboard, 1),
        recent_activity=recent_activity, progress_to_next=progress_to_next
    )
