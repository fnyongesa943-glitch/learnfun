"""
Quiz Blueprint - Handles quiz taking, scoring, hints, and streaks.
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from models import db, Quiz, Question, Score, User, UserBadge, BADGE_DEFINITIONS
from blueprints.auth import login_required

quiz_bp = Blueprint('quiz', __name__)


@quiz_bp.route('/<int:quiz_id>')
@login_required
def start_quiz(quiz_id):
    """Start a new quiz."""
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

    results = []
    for question in questions:
        user_answer = answers.get(f'q{question.id}', '')
        hint_used = answers.get(f'q{question.id}_hint_used') == 'true'
        is_correct = user_answer == question.correct_answer

        pts = 0
        if is_correct:
            correct += 1
            pts = question.points
            if hint_used:
                pts = max(0, pts - 2)  # Penalty for using hint
            earned_points += pts

        results.append({
            'question_id': question.id, 'text': question.text, 'user_answer': user_answer,
            'correct_answer': question.correct_answer, 'is_correct': is_correct,
            'explanation': question.explanation, 'points': pts, 'hint_used': hint_used
        })

    score_percentage = int((correct / total_questions) * 100) if total_questions > 0 else 0

    # Save score
    new_score = Score(user_id=user.id, quiz_id=quiz_id, score=score_percentage, points_earned=earned_points)
    db.session.add(new_score)

    # Add points & check level up
    leveled_up = user.add_points(earned_points)
    user.update_streak()  # Update streak on quiz completion

    # Check badges
    new_badges = check_and_award_badges(user)
    db.session.commit()

    return render_template(
        'quiz_result.html', quiz=quiz, questions=questions, results=results,
        score=score_percentage, correct=correct, total=total_questions,
        earned_points=earned_points, leveled_up=leveled_up, new_badges=new_badges
    )


def check_and_award_badges(user):
    """Check and award badges."""
    new_badges = []
    total_quizzes = Score.query.filter_by(user_id=user.id).count()
    
    math_q = Score.query.join(Quiz).filter(Score.user_id == user.id, Quiz.subject_id == 1).count()
    reading_q = Score.query.join(Quiz).filter(Score.user_id == user.id, Quiz.subject_id == 2).count()
    science_q = Score.query.join(Quiz).filter(Score.user_id == user.id, Quiz.subject_id == 3).count()
    geo_q = Score.query.join(Quiz).filter(Score.user_id == user.id, Quiz.subject_id == 4).count()
    
    has_perfect = Score.query.filter_by(user_id=user.id, score=100).first()

    checks = [
        (total_quizzes >= 1, 'first_quiz'), (has_perfect, 'perfect_score'),
        (math_q >= 3, 'math_star'), (reading_q >= 3, 'reading_pro'),
        (science_q >= 3, 'science_wiz'), (geo_q >= 3, 'geo_explorer'),
        (total_quizzes >= 5, 'five_quiz'), (total_quizzes >= 10, 'ten_quiz'),
        (user.level >= 5, 'level_5'), (user.streak_days >= 3, 'streak_3'), (user.streak_days >= 7, 'streak_7'),
    ]

    for cond, key in checks:
        if cond:
            defn = BADGE_DEFINITIONS.get(key)
            if defn and not UserBadge.query.filter_by(user_id=user.id, badge_name=defn['name']).first():
                db.session.add(UserBadge(user_id=user.id, badge_name=defn['name'], badge_icon=defn['icon'], badge_description=defn['description']))
                new_badges.append(defn)

    return new_badges
