"""
Stories Blueprint - Children's stories of various genres.
"""
from flask import Blueprint, render_template, redirect, url_for, session, request, flash, jsonify
from models import db, Story, UserStoryRead, User, BADGE_DEFINITIONS
from datetime import datetime

stories_bp = Blueprint('stories', __name__)


@stories_bp.route('/')
def story_list():
    """Display all stories, filterable by type and language."""
    story_type = request.args.get('type', 'all')
    age = request.args.get('age', 'all')
    lang = request.args.get('lang', 'all')

    query = Story.query

    if story_type != 'all':
        query = query.filter_by(story_type=story_type)
    if age != 'all':
        query = query.filter_by(age_range=age)
    if lang != 'all':
        query = query.filter_by(language=lang)

    stories = query.order_by(Story.created_at.desc()).all()

    # Get unique story types and languages for filter
    story_types = db.session.query(Story.story_type).distinct().all()
    story_types = [t[0] for t in story_types]
    languages = db.session.query(Story.language).distinct().all()
    languages = [t[0] for t in languages]

    # Get user's read stories
    read_story_ids = []
    if 'user_id' in session:
        read_story_ids = [r.story_id for r in UserStoryRead.query.filter_by(user_id=session['user_id']).all()]

    return render_template('stories.html',
                           stories=stories,
                           story_types=story_types,
                           languages=languages,
                           read_story_ids=read_story_ids,
                           current_type=story_type,
                           current_age=age,
                           current_lang=lang)


@stories_bp.route('/<int:story_id>')
def story_detail(story_id):
    """Display a single story."""
    story = Story.query.get_or_404(story_id)

    # Check if user has read this story
    has_read = False
    earned_points = False
    if 'user_id' in session:
        read_record = UserStoryRead.query.filter_by(user_id=session['user_id'], story_id=story_id).first()
        if read_record:
            has_read = True
            earned_points = read_record.points_awarded

    return render_template('story_detail.html',
                           story=story,
                           has_read=has_read,
                           earned_points=earned_points)


@stories_bp.route('/<int:story_id>/read', methods=['POST'])
def mark_as_read(story_id):
    """Mark a story as read and award points."""
    if 'user_id' not in session:
        flash('Please log in to track your reading!', 'warning')
        return redirect(url_for('auth.login'))

    story = Story.query.get_or_404(story_id)
    user = User.query.get(session['user_id'])

    # Check if already read
    existing = UserStoryRead.query.filter_by(user_id=user.id, story_id=story_id).first()
    if existing:
        if not existing.points_awarded:
            # Award points if not already awarded
            level_up = user.add_points(story.points_earned)
            existing.points_awarded = True
            db.session.commit()
            flash(f'You earned {story.points_earned} points for reading!', 'success')
            if level_up:
                flash(f'Level up! You reached level {user.level}!', 'success')
        else:
            flash('You already read this story and earned points!', 'info')
    else:
        # First time reading
        read_record = UserStoryRead(user_id=user.id, story_id=story_id, points_awarded=True)
        db.session.add(read_record)
        level_up = user.add_points(story.points_earned)
        db.session.commit()

        flash(f'Great job reading! You earned {story.points_earned} points!', 'success')
        if level_up:
            flash(f'Level up! You reached level {user.level}!', 'success')

        # Check for story-related badges
        check_story_badges(user)

    return redirect(url_for('stories.story_detail', story_id=story_id))


def check_story_badges(user):
    """Check and award story-related badges."""
    read_count = UserStoryRead.query.filter_by(user_id=user.id).count()

    # Story Lover - 5 stories
    if read_count >= 5 and not UserBadge.query.filter_by(user_id=user.id, badge_name='story_lover').first():
        badge = UserBadge(user_id=user.id, badge_name='story_lover',
                          badge_icon=BADGE_DEFINITIONS['story_lover']['icon'],
                          badge_description=BADGE_DEFINITIONS['story_lover']['description'])
        db.session.add(badge)
        db.session.commit()
        flash(f"Badge earned: {BADGE_DEFINITIONS['story_lover']['icon']} Story Lover!", 'success')

    # Story Master - 15 stories
    if read_count >= 15 and not UserBadge.query.filter_by(user_id=user.id, badge_name='story_master').first():
        badge = UserBadge(user_id=user.id, badge_name='story_master',
                          badge_icon=BADGE_DEFINITIONS['story_master']['icon'],
                          badge_description=BADGE_DEFINITIONS['story_master']['description'])
        db.session.add(badge)
        db.session.commit()
        flash(f"Badge earned: {BADGE_DEFINITIONS['story_master']['icon']} Story Master!", 'success')

    # Imagination King - 5 imagination stories
    imagination_reads = db.session.query(UserStoryRead).join(Story).filter(
        UserStoryRead.user_id == user.id,
        Story.story_type == 'imagination'
    ).count()

    if imagination_reads >= 5 and not UserBadge.query.filter_by(user_id=user.id, badge_name='imagination_king').first():
        badge = UserBadge(user_id=user.id, badge_name='imagination_king',
                          badge_icon=BADGE_DEFINITIONS['imagination_king']['icon'],
                          badge_description=BADGE_DEFINITIONS['imagination_king']['description'])
        db.session.add(badge)
        db.session.commit()
        flash(f"Badge earned: {BADGE_DEFINITIONS['imagination_king']['icon']} Imagination King!", 'success')
