"""
Quiz Blueprint - Handles quiz taking and scoring.
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from models import db, Quiz, Question, Score, User, UserBadge, BADGE_DEFINITIONS
from blueprints.auth import login_required
import json

quiz_bp = Blueprint('quiz', __name__)


@quiz_bp.route('/<int:quiz_id>')
@login_required
def start_quiz(quiz_id):
    """Start a new quiz and show questions."""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    if not questions:
        flash('This quiz has no questions yet!', 'warning')
        return redirect(url_for('main.subject_detail', subject_id=quiz.subject_id))

    return render_template('quiz.html', quiz=quiz, questions=questions)


@quiz_bp.route('/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    """Submit quiz answers and calculate score."""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    user = User.query.get(session['user_id'])

    answers = request.form
    correct = 0
    total_questions = len(questions)
    total_points = 0
    earned_points = 0

    # Calculate results
    results = []
    for question in questions:
        user_answer = answers.get(f'q{question.id}', '')
        is_correct = user_answer == question.correct_answer

        if is_correct:
            correct += 1
            earned_points += question.points

        results.append({
            'question_id': question.id,
            'text': question.text,
            'user_answer': user_answer,
            'correct_answer': question.correct_answer,
            'is_correct': is_correct,
            'explanation': question.explanation,
            'points': question.points if is_correct else 0
        })

    # Calculate score percentage
    score_percentage = int((correct / total_questions) * 100) if total_questions > 0 else 0

    # Save score to database
    new_score = Score(
        user_id=user.id,
        quiz_id=quiz_id,
        score=score_percentage,
        points_earned=earned_points
    )
    db.session.add(new_score)

    # Add points to user and check for level up
    leveled_up = user.add_points(earned_points)

    # Check for new badges
    new_badges = check_and_award_badges(user)

    db.session.commit()

    return render_template(
        'quiz_result.html',
        quiz=quiz,
        questions=questions,
        results=results,
        score=score_percentage,
        correct=correct,
        total=total_questions,
        earned_points=earned_points,
        leveled_up=leveled_up,
        new_badges=new_badges
    )


@quiz_bp.route('/<int:quiz_id>/check', methods=['POST'])
@login_required
def check_answer(quiz_id):
    """Check a single answer (for AJAX)."""
    data = request.get_json()
    question_id = data.get('question_id')
    user_answer = data.get('answer')

    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    is_correct = user_answer == question.correct_answer

    return jsonify({
        'is_correct': is_correct,
        'correct_answer': question.correct_answer,
        'explanation': question.explanation,
        'points': question.points if is_correct else 0
    })


def check_and_award_badges(user):
    """Check if user qualifies for any new badges and award them."""
    new_badges = []

    # Count total quizzes completed
    total_quizzes = Score.query.filter_by(user_id=user.id).count()

    # Count quizzes per subject
    math_quizzes = Score.query.join(Quiz).filter(
        Score.user_id == user.id,
        Quiz.subject_id == 1
    ).count()

    reading_quizzes = Score.query.join(Quiz).filter(
        Score.user_id == user.id,
        Quiz.subject_id == 2
    ).count()

    science_quizzes = Score.query.join(Quiz).filter(
        Score.user_id == user.id,
        Quiz.subject_id == 3
    ).count()

    # Check for perfect scores
    has_perfect = Score.query.filter_by(
        user_id=user.id,
        score=100
    ).first()

    # Badge checks
    badge_checks = [
        (total_quizzes >= 1, 'first_quiz'),
        (has_perfect is not None, 'perfect_score'),
        (math_quizzes >= 3, 'math_star'),
        (reading_quizzes >= 3, 'reading_pro'),
        (science_quizzes >= 3, 'science_wiz'),
        (total_quizzes >= 5, 'five_quiz'),
        (total_quizzes >= 10, 'ten_quiz'),
        (user.level >= 5, 'level_5'),
    ]

    for condition, badge_key in badge_checks:
        if condition:
            # Check if already earned
            existing = UserBadge.query.filter_by(
                user_id=user.id,
                badge_name=BADGE_DEFINITIONS[badge_key]['name']
            ).first()

            if not existing:
                badge_def = BADGE_DEFINITIONS[badge_key]
                new_badge = UserBadge(
                    user_id=user.id,
                    badge_name=badge_def['name'],
                    badge_icon=badge_def['icon'],
                    badge_description=badge_def['description']
                )
                db.session.add(new_badge)
                new_badges.append(badge_def)

    return new_badges
