"""
Progress Blueprint - User dashboard and progress tracking.
"""
from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import db, User, Score, Quiz, Subject, UserBadge
from blueprints.auth import login_required
from sqlalchemy import func

progress_bp = Blueprint('progress', __name__)


@progress_bp.route('/')
@login_required
def dashboard():
    """User progress dashboard."""
    user = User.query.get(session['user_id'])

    # Get all scores for this user
    scores = Score.query.filter_by(user_id=user.id).order_by(Score.completed_at.desc()).all()

    # Calculate total quizzes completed
    total_quizzes = len(scores)

    # Calculate average score
    if scores:
        avg_score = int(sum(s.score for s in scores) / len(scores))
    else:
        avg_score = 0

    # Progress by subject
    subject_progress = []
    subjects = Subject.query.all()
    for subject in subjects:
        subject_scores = Score.query.join(Quiz).filter(
            Score.user_id == user.id,
            Quiz.subject_id == subject.id
        ).all()

        completed = len(subject_scores)
        total_quizzes_for_subject = Quiz.query.filter_by(subject_id=subject.id).count()

        # Calculate best score for this subject
        if subject_scores:
            best_score = max(s.score for s in subject_scores)
        else:
            best_score = 0

        subject_progress.append({
            'id': subject.id,
            'name': subject.name,
            'icon': subject.icon,
            'color': subject.color,
            'completed': completed,
            'total': total_quizzes_for_subject,
            'best_score': best_score,
            'percentage': int((completed / total_quizzes_for_subject) * 100) if total_quizzes_for_subject > 0 else 0
        })

    # Get badges
    badges = UserBadge.query.filter_by(user_id=user.id).order_by(UserBadge.earned_at.desc()).all()

    # Recent activity (last 5 scores)
    recent_activity = []
    for score in scores[:5]:
        quiz = Quiz.query.get(score.quiz_id)
        subject = Subject.query.get(quiz.subject_id)
        recent_activity.append({
            'quiz_title': quiz.title,
            'subject_name': subject.name,
            'subject_icon': subject.icon,
            'score': score.score,
            'points_earned': score.points_earned,
            'completed_at': score.completed_at
        })

    # Points to next level
    points_for_next_level = (user.level * 100)
    current_level_points = user.total_points % 100
    progress_to_next = int((current_level_points / 100) * 100)

    return render_template(
        'progress.html',
        user=user,
        total_quizzes=total_quizzes,
        avg_score=avg_score,
        subject_progress=subject_progress,
        badges=badges,
        recent_activity=recent_activity,
        points_for_next_level=points_for_next_level,
        current_level_points=current_level_points,
        progress_to_next=progress_to_next
    )
