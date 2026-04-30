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
