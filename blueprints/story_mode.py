"""
Story Mode Blueprint - Adventure journey with locked stages.
"""
from flask import Blueprint, render_template, session, jsonify, redirect, url_for, flash
from models import db, User, AdventureStage, StoryProgress, Quiz, Question, Score
from blueprints.auth import login_required
from datetime import datetime

story_mode_bp = Blueprint('story_mode', __name__)


@story_mode_bp.route('/')
@login_required
def adventure_map():
    """Show the adventure map with all stages."""
    user = User.query.get(session['user_id'])
    stages = AdventureStage.query.order_by(AdventureStage.order_number).all()

    stage_data = []
    for stage in stages:
        progress = StoryProgress.query.filter_by(user_id=user.id, stage_id=stage.id).first()
        completed = progress.completed if progress else False
        score = progress.score if progress else 0
        attempts = progress.attempts if progress else 0

        stage_data.append({
            'stage': stage,
            'completed': completed,
            'score': score,
            'attempts': attempts,
            'unlocked': True
        })

    return render_template('story_mode.html', user=user, stages=stage_data)


@story_mode_bp.route('/<int:stage_id>/start')
@login_required
def start_stage(stage_id):
    """Start an adventure stage (redirects to quiz)."""
    user = User.query.get(session['user_id'])
    stage = AdventureStage.query.get_or_404(stage_id)
    
    progress = StoryProgress.query.filter_by(user_id=user.id, stage_id=stage_id).first()
    if not progress:
        progress = StoryProgress(user_id=user.id, stage_id=stage_id, attempts=0)
        db.session.add(progress)
        db.session.commit()

    return redirect(url_for('quiz.start_quiz', quiz_id=stage.quiz_id))


@story_mode_bp.route('/<int:stage_id>/complete', methods=['POST'])
@login_required
def complete_stage(stage_id):
    """Mark a stage as complete after quiz submission."""
    user = User.query.get(session['user_id'])
    stage = AdventureStage.query.get_or_404(stage_id)
    
    progress = StoryProgress.query.filter_by(user_id=user.id, stage_id=stage_id).first()
    if not progress:
        progress = StoryProgress(user_id=user.id, stage_id=stage_id, attempts=0)
        db.session.add(progress)

    progress.attempts += 1
    progress.completed = True
    progress.score = int(request.form.get('score', 0))
    progress.completed_at = datetime.utcnow()

    user.add_points(stage.points_reward)
    db.session.commit()

    return jsonify({'success': True, 'points': stage.points_reward, 'stage_title': stage.title})


@story_mode_bp.route('/api/check-unlock/<int:stage_id>')
@login_required
def check_unlock(stage_id):
    """Check if a stage is unlocked."""
    user = User.query.get(session['user_id'])
    stages = AdventureStage.query.order_by(AdventureStage.order_number).all()
    
    target = None
    prev_completed = True
    for s in stages:
        if s.id == stage_id:
            target = s
            break
        progress = StoryProgress.query.filter_by(user_id=user.id, stage_id=s.id).first()
        if not progress or not progress.completed:
            prev_completed = False

    if not target:
        return jsonify({'unlocked': False})

    return jsonify({'unlocked': prev_completed})
