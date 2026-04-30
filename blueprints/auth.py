"""
Authentication Blueprint - Handles user login, signup, and logout.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User
from functools import wraps

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
