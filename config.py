import os


class Config:
    """Base configuration for the Kids Learning App."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'kids-learning-secret-key-2024')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Handle both SQLite (local) and PostgreSQL (Render/production)
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///kids_learning.db')

    # Render provides postgres:// but SQLAlchemy needs postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = database_url

    # Email / SMTP settings for parent report emailing
    SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USER = os.environ.get('SMTP_USER', '')
    SMTP_PASS = os.environ.get('SMTP_PASS', '')
    FROM_EMAIL = os.environ.get('FROM_EMAIL', '')
