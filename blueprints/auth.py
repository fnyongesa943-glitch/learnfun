"""
Authentication Blueprint - Handles user login, signup, and logout.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User
from functools import wraps

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    """Decorator to require login for certain routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue!', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        avatar = request.form.get('avatar', 'bear')

        # Validate input
        if not username or not email or not password:
            flash('Please fill in all fields!', 'error')
            return render_template('signup.html')

        if len(password) < 4:
            flash('Password must be at least 4 characters!', 'error')
            return render_template('signup.html')

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already taken! Try another one.', 'error')
            return render_template('signup.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered! Try logging in.', 'error')
            return render_template('signup.html')

        # Create new user
        new_user = User(username=username, email=email, avatar=avatar)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # Auto login after signup
        session['user_id'] = new_user.id
        flash(f'Welcome, {username}! Let\'s start learning! 🎉', 'success')
        return redirect(url_for('main.index'))

    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            flash(f'Welcome back, {user.username}! 🌟', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Wrong username or password. Try again!', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('user_id', None)
    flash('See you next time! Keep learning! 👋', 'info')
    return redirect(url_for('main.index'))
