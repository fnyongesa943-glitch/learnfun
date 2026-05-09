"""
Lessons Blueprint - CBC subject topics, lessons, and learning content.
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from models import db, Grade, Subject, Topic, Lesson, UserLessonProgress, User, UserBadge, BADGE_DEFINITIONS
from blueprints.auth import login_required
from datetime import datetime
import json

lessons_bp = Blueprint('lessons', __name__)


@lessons_bp.route('/')
def grade_select():
    """Show all grade levels for browsing."""
    grades = Grade.query.order_by(Grade.sort_order).all()
    subjects = Subject.query.order_by(Subject.name).all()

    # Count topics per grade and subject
    grade_stats = {}
    for g in grades:
        topic_count = Topic.query.filter_by(grade_id=g.id).count()
        subject_ids = db.session.query(Topic.subject_id).filter_by(grade_id=g.id).distinct().all()
        grade_stats[g.id] = {
            'topic_count': topic_count,
            'subject_count': len(subject_ids),
            'has_content': topic_count > 0
        }

    return render_template('topics.html', grades=grades, subjects=subjects, grade_stats=grade_stats)


@lessons_bp.route('/grade/<int:grade_id>')
def grade_subjects(grade_id):
    """Show subjects for a specific grade with topics."""
    grade = Grade.query.get_or_404(grade_id)
    subjects = Subject.query.order_by(Subject.name).all()

    # Get topics grouped by subject for this grade
    grade_subjects = []
    for subj in subjects:
        topics = Topic.query.filter_by(subject_id=subj.id, grade_id=grade_id).order_by(Topic.order_number).all()
        if topics:
            completed = 0
            total = len(topics)
            if 'user_id' in session:
                lesson_ids = [l.id for t in topics for l in t.lessons]
                completed = UserLessonProgress.query.filter(
                    UserLessonProgress.user_id == session['user_id'],
                    UserLessonProgress.lesson_id.in_(lesson_ids),
                    UserLessonProgress.completed == True
                ).count()
                total_lessons = len(lesson_ids)

            grade_subjects.append({
                'subject': subj,
                'topics': topics,
                'total_lessons': sum(t.lesson_count() for t in topics),
                'completed_lessons': completed
            })

    return render_template('grade_subjects.html', grade=grade, grade_subjects=grade_subjects)


@lessons_bp.route('/topic/<int:topic_id>')
def topic_detail(topic_id):
    """Show all lessons in a topic."""
    topic = Topic.query.get_or_404(topic_id)
    lessons = Lesson.query.filter_by(topic_id=topic_id).order_by(Lesson.order_number).all()

    # Track progress
    completed_lessons = []
    if 'user_id' in session:
        completed_lessons = [
            p.lesson_id for p in UserLessonProgress.query.filter_by(
                user_id=session['user_id'], completed=True
            ).all()
        ]

    progress_pct = int((len(completed_lessons) / len(lessons)) * 100) if lessons else 0

    return render_template('topic_detail.html',
                           topic=topic, lessons=lessons,
                           completed_lessons=completed_lessons,
                           progress_pct=progress_pct)


@lessons_bp.route('/<int:lesson_id>')
def view_lesson(lesson_id):
    """View a specific lesson."""
    lesson = Lesson.query.get_or_404(lesson_id)
    topic = lesson.topic
    all_lessons = Lesson.query.filter_by(topic_id=topic.id).order_by(Lesson.order_number).all()

    # Find prev/next
    prev_lesson = None
    next_lesson = None
    for i, l in enumerate(all_lessons):
        if l.id == lesson_id:
            if i > 0:
                prev_lesson = all_lessons[i - 1]
            if i < len(all_lessons) - 1:
                next_lesson = all_lessons[i + 1]
            break

    # Check completion
    is_completed = False
    if 'user_id' in session:
        prog = UserLessonProgress.query.filter_by(
            user_id=session['user_id'], lesson_id=lesson_id
        ).first()
        if prog:
            is_completed = prog.completed

    return render_template('lesson.html',
                           lesson=lesson, topic=topic,
                           prev_lesson=prev_lesson, next_lesson=next_lesson,
                           is_completed=is_completed,
                           lesson_number=next((i + 1 for i, l in enumerate(all_lessons) if l.id == lesson_id), 1),
                           total_lessons=len(all_lessons))


@lessons_bp.route('/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    """Mark a lesson as completed and award points."""
    lesson = Lesson.query.get_or_404(lesson_id)
    user = User.query.get(session['user_id'])

    existing = UserLessonProgress.query.filter_by(
        user_id=user.id, lesson_id=lesson_id
    ).first()

    if existing and existing.completed:
        flash('You already completed this lesson!', 'info')
    else:
        if existing:
            existing.completed = True
            existing.completed_at = datetime.utcnow()
        else:
            prog = UserLessonProgress(
                user_id=user.id, lesson_id=lesson_id,
                completed=True, completed_at=datetime.utcnow()
            )
            db.session.add(prog)

        leveled_up = user.add_points(lesson.points_earned)

        # Check lesson badges
        total_completed = UserLessonProgress.query.filter_by(
            user_id=user.id, completed=True
        ).count()

        # Check first_lesson badge
        if total_completed >= 1:
            check_badge(user, 'first_lesson')
        if total_completed >= 5:
            check_badge(user, 'five_lessons')

        # Check topic mastery
        topic = lesson.topic
        topic_lessons = Lesson.query.filter_by(topic_id=topic.id).count()
        topic_completed = UserLessonProgress.query.join(Lesson).filter(
            UserLessonProgress.user_id == user.id,
            Lesson.topic_id == topic.id,
            UserLessonProgress.completed == True
        ).count()
        if topic_completed >= topic_lessons and topic_lessons > 0:
            check_badge(user, 'topic_master')

        db.session.commit()

        flash(f'🎉 Great job! You earned {lesson.points_earned} points!', 'success')
        if leveled_up:
            flash(f'⭐ Level up! You reached level {user.level}!', 'success')

    return redirect(url_for('lessons.view_lesson', lesson_id=lesson_id))


def check_badge(user, badge_key):
    defn = BADGE_DEFINITIONS.get(badge_key)
    if defn and not UserBadge.query.filter_by(user_id=user.id, badge_name=defn['name']).first():
        db.session.add(UserBadge(
            user_id=user.id, badge_name=defn['name'],
            badge_icon=defn['icon'], badge_description=defn['description']
        ))
        flash(f'🏆 Badge earned: {defn["icon"]} {defn["name"]}!', 'success')


@lessons_bp.route('/api/search')
def search_lessons():
    """Search topics and lessons."""
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    topics = Topic.query.filter(Topic.title.ilike(f'%{q}%')).limit(10).all()
    lessons = Lesson.query.filter(Lesson.title.ilike(f'%{q}%')).limit(10).all()

    results = []
    for t in topics:
        results.append({
            'type': 'topic',
            'id': t.id,
            'title': t.title,
            'subject': t.subject.name,
            'grade': t.grade.name,
            'icon': t.icon,
            'url': url_for('lessons.topic_detail', topic_id=t.id)
        })
    for l in lessons:
        results.append({
            'type': 'lesson',
            'id': l.id,
            'title': l.title,
            'topic': l.topic.title,
            'icon': l.image_emoji,
            'url': url_for('lessons.view_lesson', lesson_id=l.id)
        })

    return jsonify(results[:20])
