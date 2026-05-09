import sys, os
os.chdir(r'C:\Users\fnyon\Videos\Learn_tip\kids_learning_app')
sys.path.insert(0, '.')

from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from models import db
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    from sqlalchemy import inspect, text
    inspector = inspect(db.engine)

    # Grade table should exist
    tables = inspector.get_table_names()
    new_tables = [t for t in tables if t in ('grades', 'topics', 'lessons', 'user_lesson_progress')]
    print(f'New tables after create_all: {new_tables}')

    # Subjects columns
    cols = {c['name'] for c in inspector.get_columns('subjects')}
    print(f'Subjects columns: {cols}')

    # Drop category to simulate old DB
    try:
        db.session.execute(text('ALTER TABLE subjects DROP COLUMN category'))
        db.session.commit()
        print('Dropped category column')
    except Exception as e:
        print(f'Could not drop category: {e}')

    inspector = inspect(db.engine)
    cols = {c['name'] for c in inspector.get_columns('subjects')}
    print(f'Subjects columns after drop: {cols}')

    print('--- Simulating Render startup ---')

del app

from app import create_app
app2 = create_app()
client = app2.test_client()

with app2.app_context():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    cols = {c['name'] for c in inspector.get_columns('subjects')}
    print(f'After migration - Subjects: {cols}')
    tables = inspector.get_table_names()
    new_tables = [t for t in tables if t in ('grades', 'topics', 'lessons', 'user_lesson_progress')]
    print(f'After migration - New tables: {new_tables}')

    # Check subject categories
    from models import Subject
    for s in Subject.query.all():
        print(f'  Subject: {s.name} -> category={getattr(s, "category", "MISSING")}')

resp = client.get('/')
print(f'Homepage: {resp.status_code}')
if resp.status_code == 200:
    print('OK - Homepage renders')
else:
    print(f'ERROR {resp.status_code}')
    print(resp.data.decode('utf-8', errors='replace')[:1000])
