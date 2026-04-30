# WSGI entry point for production
import os
import sys

# Ensure app directory is in path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

application = create_app()
