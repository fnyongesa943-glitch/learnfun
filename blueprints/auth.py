"""
Authentication Blueprint - Handles user login, signup, logout, and password reset.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User
from functools import wraps
from datetime import datetime, timedelta
import secrets

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue!', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        avatar = request.form.get('avatar', 'bear')

        if not username or not email or not password:
            flash('Please fill in all fields!', 'error')
            return render_template('signup.html')

        if len(password) < 4:
            flash('Password must be at least 4 characters!', 'error')
            return render_template('signup.html')

        if User.query.filter_by(username=username).first():
            flash('Username already taken!', 'error')
            return render_template('signup.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return render_template('signup.html')

        new_user = User(username=username, email=email, avatar=avatar, coins=10)  # Welcome bonus
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        flash(f'Welcome, {username}! You got 10 bonus coins! 🎉', 'success')
        return redirect(url_for('main.index'))

    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter((User.username == username) | (User.email == username)).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            user.update_streak()  # Update streak on login
            db.session.commit()
            flash(f'Welcome back, {user.username}! 🔥 {user.streak_days} day streak!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Wrong username or password.', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('See you next time!', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = User.query.filter_by(email=email).first()

        if user:
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
            reset_link = url_for('auth.reset_password', token=token, _external=True)
            flash(f'Reset link generated: {reset_link}', 'success')
        else:
            flash('If that email is registered, a reset link has been generated.', 'info')
        return redirect(url_for('auth.forgot_password'))

    return render_template('forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
        flash('Invalid or expired reset link.', 'error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if len(password) < 4:
            flash('Password must be at least 4 characters!', 'error')
            return render_template('reset_password.html', token=token)

        if password != confirm:
            flash('Passwords do not match!', 'error')
            return render_template('reset_password.html', token=token)

        user.set_password(password)
        user.reset_token = None
        user.reset_token_expires = None
        db.session.commit()
        flash('Password reset successfully! Log in with your new password.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', token=token)
