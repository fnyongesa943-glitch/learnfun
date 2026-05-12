"""
Kids Learning App - Main Application Entry Point
Updated with new subjects, shop, stories, and enhanced features.
"""
import os
from flask import Flask, session
from seed_cbc import seed_cbc_content
from models import db, User, Subject, Quiz, Question, Score, UserBadge, ShopItem, UserOwnedItem, Story, UserStoryRead, Grade, Topic, Lesson, UserLessonProgress
from config import Config


def create_app():
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()
            run_migrations()
            seed_data()
            seed_cbc_data()
        except Exception as e:
            print(f"⚠️ Startup error (non-fatal): {e}")
            import traceback
            traceback.print_exc()

    from blueprints.main import main_bp
    from blueprints.auth import auth_bp
    from blueprints.quiz import quiz_bp
    from blueprints.progress import progress_bp
    from blueprints.parent import parent_bp
    from blueprints.stories import stories_bp
    from blueprints.lessons import lessons_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    app.register_blueprint(progress_bp, url_prefix='/progress')
    app.register_blueprint(parent_bp, url_prefix='/parent')
    app.register_blueprint(stories_bp, url_prefix='/stories')
    app.register_blueprint(lessons_bp, url_prefix='/lessons')

    @app.context_processor
    def inject_user():
        user = None
        if 'user_id' in session:
            try:
                user = User.query.get(session['user_id'])
            except Exception:
                session.pop('user_id', None)
        return {'current_user': user}

    return app


def run_migrations():
    """Add missing columns to existing database tables safely."""
    from sqlalchemy import inspect, text
    try:
        inspector = inspect(db.engine)
    except Exception:
        return  # Can't inspect, skip migrations

    migrations = []

    # Check subjects table for category column
    try:
        if 'subjects' in inspector.get_table_names():
            cols = {c['name']: c for c in inspector.get_columns('subjects')}
            if 'category' not in cols:
                migrations.append("ALTER TABLE subjects ADD COLUMN category VARCHAR(30) DEFAULT 'Core'")
    except Exception:
        pass

    # Check questions table for hint column
    try:
        if 'questions' in inspector.get_table_names():
            cols = {c['name']: c for c in inspector.get_columns('questions')}
            if 'hint' not in cols:
                migrations.append("ALTER TABLE questions ADD COLUMN hint VARCHAR(200) DEFAULT ''")
    except Exception:
        pass

    # Check quizzes table for new columns
    try:
        if 'quizzes' in inspector.get_table_names():
            cols = {c['name']: c for c in inspector.get_columns('quizzes')}
            if 'lesson_id' not in cols:
                migrations.append("ALTER TABLE quizzes ADD COLUMN lesson_id INTEGER")
            if 'grade_id' not in cols:
                migrations.append("ALTER TABLE quizzes ADD COLUMN grade_id INTEGER")
            if 'topic_id' not in cols:
                migrations.append("ALTER TABLE quizzes ADD COLUMN topic_id INTEGER")
    except Exception:
        pass

    # Check users table for parent_email column
    try:
        if 'users' in inspector.get_table_names():
            cols = {c['name']: c for c in inspector.get_columns('users')}
            if 'parent_email' not in cols:
                migrations.append("ALTER TABLE users ADD COLUMN parent_email VARCHAR(120) DEFAULT ''")
    except Exception:
        pass

    # Check stories for language column
    try:
        if 'stories' in inspector.get_table_names():
            cols = {c['name']: c for c in inspector.get_columns('stories')}
            if 'language' not in cols:
                migrations.append("ALTER TABLE stories ADD COLUMN language VARCHAR(10) DEFAULT 'en'")
    except Exception:
        pass

    # Execute migrations
    for migration in migrations:
        try:
            db.session.execute(text(migration))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"  Migration warning ({migration[:60]}): {e}")

    # Fix old phonics quiz sounds (e.g. "ah" → "a", "buh" → "b")
    try:
        from models import Question
        sound_fixes = {
            'ah': 'a', 'buh': 'b', 'kuh': 'k', 'duh': 'd',
            'eh': 'e', 'fff': 'f', 'guh': 'g',
            'hhh': 'h', 'ih': 'i', 'jjj': 'j',
            'lll': 'l', 'mmm': 'm', 'nnn': 'n',
            'oh': 'o', 'puh': 'p',
            'rrr': 'r', 'sss': 's', 'tuh': 't',
            'uh': 'u', 'vvv': 'v', 'www': 'w',
            'yyy': 'y', 'zzz': 'z',
        }
        for old, new in sound_fixes.items():
            for col in ['option_a', 'option_b', 'option_c', 'option_d']:
                kwargs = {col: old}
                count = Question.query.filter_by(**kwargs).count()
                if count > 0:
                    kwargs_update = {col: new}
                    db.session.query(Question).filter_by(**{col: old}).update(
                        kwargs_update, synchronize_session=False
                    )
        db.session.commit()
    except Exception:
        db.session.rollback()

    # Ensure new tables exist
    try:
        db.create_all()
    except Exception:
        pass


def seed_data():
    """Seed database with subjects, quizzes, shop items, stories, and questions."""
    from models import ShopItem, Story

    # Add shop items if not seeded
    if not ShopItem.query.first():
        shop_items = [
            ShopItem(name='Star Frame', icon='⭐', item_type='frame', price=50, description='A shiny star border!'),
            ShopItem(name='Rainbow Frame', icon='🌈', item_type='frame', price=100, description='Colorful rainbow frame!'),
            ShopItem(name='Gold Trophy', icon='🏆', item_type='badge', price=150, description='Show off your gold trophy!'),
            ShopItem(name='Wizard Hat', icon='🧙', item_type='hat', price=200, description='Become a learning wizard!'),
            ShopItem(name='Crown', icon='👑', item_type='hat', price=300, description='Fit for a king or queen!'),
            ShopItem(name='Rocket', icon='🚀', item_type='badge', price=250, description='Ready for liftoff!'),
            ShopItem(name='Diamond Badge', icon='💎', item_type='badge', price=500, description='Rare and sparkling!'),
            ShopItem(name='Unicorn', icon='🦄', item_type='avatar', price=400, description='Magical and majestic!'),
            ShopItem(name='Dino', icon='🦖', item_type='avatar', price=400, description='Rawr!'),
            ShopItem(name='Astronaut', icon='🧑‍🚀', item_type='avatar', price=600, description='To the moon!'),
        ]
        db.session.add_all(shop_items)
        db.session.commit()

    # Always check for missing subjects
    existing_names = {s.name for s in Subject.query.all()}
    subjects = [
        Subject(name='Math', icon='🔢', color='#4F46E5', description='Addition, subtraction, multiplication!'),
        Subject(name='Reading', icon='📚', color='#7C3AED', description='Word puzzles and stories!'),
        Subject(name='Science', icon='🔬', color='#059669', description='Animals, weather, and space!'),
        Subject(name='Geography', icon='🌍', color='#D97706', description='Countries, maps, and landmarks!'),
        Subject(name='Art', icon='🎨', color='#EC4899', description='Colors, shapes, and famous artists!'),
        Subject(name='Coding', icon='💻', color='#3B82F6', description='Logic puzzles and algorithms!'),
        Subject(name='Music', icon='🎵', color='#8B5CF6', description='Instruments and rhythms!'),
        Subject(name='ABC', icon='🔤', color='#EC4899', description='Learn the alphabet A-Z!'),
        Subject(name='123', icon='🔢', color='#14B8A6', description='Count from 1 to 100!'),
    ]

    new_subjects = [s for s in subjects if s.name not in existing_names]
    if new_subjects:
        db.session.add_all(new_subjects)
        db.session.commit()
        existing_names = {s.name for s in Subject.query.all()}

    # Build subject lookup
    subject_map = {s.name: s for s in Subject.query.all()}

    # Helper to add quizzes if they don't exist
    def add_quiz_if_missing(title, sub_name, difficulty, description):
        sub = subject_map.get(sub_name)
        if not sub:
            return None
        existing = Quiz.query.filter_by(title=title).first()
        if existing:
            return existing
        q = Quiz(title=title, subject_id=sub.id, difficulty=difficulty, description=description)
        db.session.add(q)
        db.session.commit()
        return q

    # Helper to add questions if quiz has none
    def add_questions_if_missing(quiz, qs):
        if not quiz or Question.query.filter_by(quiz_id=quiz.id).first():
            return
        db.session.add_all(qs)
        db.session.commit()

    # --- ABC QUIZZES ---
    abc1 = add_quiz_if_missing('Letters A-F', 'ABC', 'easy', 'First letters!')
    if abc1:
        add_questions_if_missing(abc1, [
            Question(quiz_id=abc1.id, text='What letter comes after A?', option_a='C', option_b='B', option_c='D', option_d='E', correct_answer='B', explanation='A, B! B comes after A!', hint='A then what?', points=5),
            Question(quiz_id=abc1.id, text='What letter comes before D?', option_a='C', option_b='E', option_c='B', option_d='A', correct_answer='A', explanation='C comes before D! A, B, C, D.', hint='A, B, ?, D.', points=5),
            Question(quiz_id=abc1.id, text='What letter is "Apple" for?', option_a='A', option_b='B', option_c='C', option_d='D', correct_answer='A', explanation='Apple starts with A!', hint='🍎 Apple.', points=5),
            Question(quiz_id=abc1.id, text='What letter comes after F?', option_a='E', option_b='D', option_c='G', option_d='H', correct_answer='C', explanation='G comes after F!', hint='After F comes?', points=5),
            Question(quiz_id=abc1.id, text='Which is a letter?', option_a='1', option_b='B', option_c='+', option_d='%', correct_answer='B', explanation='B is a letter!', hint='Look for ABC.', points=5),
        ])

    abc2 = add_quiz_if_missing('Letters G-L', 'ABC', 'easy', 'Next letters!')
    if abc2:
        add_questions_if_missing(abc2, [
            Question(quiz_id=abc2.id, text='What letter comes after L?', option_a='K', option_b='J', option_c='M', option_d='N', correct_answer='C', explanation='M comes after L!', hint='J, K, L, ?', points=5),
            Question(quiz_id=abc2.id, text='What letter comes before I?', option_a='J', option_b='H', option_c='G', option_d='K', correct_answer='B', explanation='H comes before I!', hint='G, ?, I.', points=5),
            Question(quiz_id=abc2.id, text='J is for?', option_a='Jump', option_b='Dog', option_c='Cat', option_d='Fish', correct_answer='A', explanation='Jump starts with J!', hint='Up and down!', points=5),
            Question(quiz_id=abc2.id, text='What letter is "Kite" for?', option_a='J', option_b='L', option_c='K', option_d='M', correct_answer='C', explanation='Kite starts with K!', hint='🪁 Kite.', points=5),
            Question(quiz_id=abc2.id, text='Letter after G?', option_a='F', option_b='H', option_c='I', option_d='J', correct_answer='B', explanation='H comes after G!', hint='F, G, ?', points=5),
        ])

    abc3 = add_quiz_if_missing('Letters M-Z', 'ABC', 'easy', 'Last letters!')
    if abc3:
        add_questions_if_missing(abc3, [
            Question(quiz_id=abc3.id, text='What letter is "Zebra" for?', option_a='X', option_b='Y', option_c='Z', option_d='W', correct_answer='C', explanation='Zebra starts with Z!', hint='🦓 Last letter.', points=5),
            Question(quiz_id=abc3.id, text='What letter comes before Y?', option_a='Z', option_b='X', option_c='W', option_d='V', correct_answer='B', explanation='X comes before Y!', hint='W, ?, Y, Z.', points=5),
            Question(quiz_id=abc3.id, text='What letter is "Monkey" for?', option_a='M', option_b='N', option_c='O', option_d='L', correct_answer='A', explanation='Monkey starts with M!', hint='🐒 Mmm!', points=5),
            Question(quiz_id=abc3.id, text='What letter is after T?', option_a='S', option_b='R', option_c='U', option_d='V', correct_answer='C', explanation='U comes after T!', hint='R, S, T, ?', points=5),
            Question(quiz_id=abc3.id, text='Last letter of alphabet?', option_a='X', option_b='Y', option_c='Z', option_d='A', correct_answer='C', explanation='Z is the last letter!', hint='🦓 Zebra.', points=5),
        ])

    # --- PHONICS QUIZZES ---
    ph1 = add_quiz_if_missing('Phonics A-G', 'ABC', 'easy', 'Letter sounds!')
    if ph1:
        add_questions_if_missing(ph1, [
            Question(quiz_id=ph1.id, text='What sound does A make?', option_a='a', option_b='b', option_c='k', option_d='d', correct_answer='A', explanation='A says "a" like Apple!', hint='🍎 a-pple.', points=5),
            Question(quiz_id=ph1.id, text='What sound does B make?', option_a='s', option_b='b', option_c='m', option_d='t', correct_answer='B', explanation='B says "b" like Ball!', hint='⚽ b-all.', points=5),
            Question(quiz_id=ph1.id, text='What sound does C make?', option_a='k', option_b='f', option_c='r', option_d='w', correct_answer='A', explanation='C says "k" like Cat!', hint='🐱 k-at.', points=5),
            Question(quiz_id=ph1.id, text='What sound does D make?', option_a='b', option_b='d', option_c='p', option_d='g', correct_answer='B', explanation='D says "d" like Dog!', hint='🐶 d-og.', points=5),
            Question(quiz_id=ph1.id, text='What sound does E make?', option_a='e', option_b='a', option_c='o', option_d='i', correct_answer='A', explanation='E says "e" like Elephant!', hint='🐘 e-lephant.', points=5),
            Question(quiz_id=ph1.id, text='What sound does F make?', option_a='f', option_b='v', option_c='th', option_d='h', correct_answer='A', explanation='F says "f" like Fish!', hint='🐟 f-ish.', points=5),
            Question(quiz_id=ph1.id, text='What sound does G make?', option_a='d', option_b='k', option_c='g', option_d='b', correct_answer='C', explanation='G says "g" like Guitar!', hint='🎸 g-uitar.', points=5),
        ])

    ph2 = add_quiz_if_missing('Phonics H-N', 'ABC', 'easy', 'More letter sounds!')
    if ph2:
        add_questions_if_missing(ph2, [
            Question(quiz_id=ph2.id, text='What sound does H make?', option_a='h', option_b='j', option_c='k', option_d='l', correct_answer='A', explanation='H says "h" like Hat!', hint='🎩 h-at.', points=5),
            Question(quiz_id=ph2.id, text='What sound does I make?', option_a='e', option_b='i', option_c='a', option_d='o', correct_answer='B', explanation='I says "i" like Igloo!', hint='🏔️ i-gloo.', points=5),
            Question(quiz_id=ph2.id, text='What sound does J make?', option_a='s', option_b='j', option_c='z', option_d='v', correct_answer='B', explanation='J says "j" like Juice!', hint='🧃 j-uice.', points=5),
            Question(quiz_id=ph2.id, text='What sound does K make?', option_a='k', option_b='p', option_c='t', option_d='b', correct_answer='A', explanation='K says "k" like Kite!', hint='🪁 k-ite.', points=5),
            Question(quiz_id=ph2.id, text='What sound does L make?', option_a='m', option_b='n', option_c='l', option_d='r', correct_answer='C', explanation='L says "l" like Lion!', hint='🦁 l-ion.', points=5),
            Question(quiz_id=ph2.id, text='What sound does M make?', option_a='n', option_b='m', option_c='b', option_d='p', correct_answer='B', explanation='M says "m" like Moon!', hint='🌙 m-oon.', points=5),
            Question(quiz_id=ph2.id, text='What sound does N make?', option_a='m', option_b='n', option_c='t', option_d='k', correct_answer='B', explanation='N says "n" like Nest!', hint='🐦 n-est.', points=5),
        ])

    ph3 = add_quiz_if_missing('Phonics O-T', 'ABC', 'easy', 'Keep going!')
    if ph3:
        add_questions_if_missing(ph3, [
            Question(quiz_id=ph3.id, text='What sound does O make?', option_a='a', option_b='e', option_c='o', option_d='u', correct_answer='C', explanation='O says "o" like Octopus!', hint='🐙 o-ctopus.', points=5),
            Question(quiz_id=ph3.id, text='What sound does P make?', option_a='b', option_b='p', option_c='d', option_d='g', correct_answer='B', explanation='P says "p" like Pig!', hint='🐷 p-ig.', points=5),
            Question(quiz_id=ph3.id, text='What sound does Q make?', option_a='kw', option_b='w', option_c='t', option_d='z', correct_answer='A', explanation='Q says "kw" like Queen!', hint='👸 kw-ueen.', points=5),
            Question(quiz_id=ph3.id, text='What sound does R make?', option_a='l', option_b='r', option_c='w', option_d='y', correct_answer='B', explanation='R says "r" like Rain!', hint='🌧️ r-ain.', points=5),
            Question(quiz_id=ph3.id, text='What sound does S make?', option_a='z', option_b='s', option_c='f', option_d='th', correct_answer='B', explanation='S says "s" like Sun!', hint='☀️ s-un.', points=5),
            Question(quiz_id=ph3.id, text='What sound does T make?', option_a='d', option_b='p', option_c='t', option_d='k', correct_answer='C', explanation='T says "t" like Tree!', hint='🌳 t-ree.', points=5),
        ])

    ph4 = add_quiz_if_missing('Phonics U-Z', 'ABC', 'easy', 'Last sounds!')
    if ph4:
        add_questions_if_missing(ph4, [
            Question(quiz_id=ph4.id, text='What sound does U make?', option_a='a', option_b='u', option_c='e', option_d='i', correct_answer='B', explanation='U says "u" like Umbrella!', hint='☂️ u-mbrella.', points=5),
            Question(quiz_id=ph4.id, text='What sound does V make?', option_a='f', option_b='w', option_c='v', option_d='z', correct_answer='C', explanation='V says "v" like Violin!', hint='🎻 v-iolin.', points=5),
            Question(quiz_id=ph4.id, text='What sound does W make?', option_a='w', option_b='v', option_c='y', option_d='r', correct_answer='A', explanation='W says "w" like Water!', hint='💧 w-ater.', points=5),
            Question(quiz_id=ph4.id, text='What sound does X make?', option_a='ks', option_b='s', option_c='t', option_d='g', correct_answer='A', explanation='X says "ks" like Box!', hint='📦 bo-ks.', points=5),
            Question(quiz_id=ph4.id, text='What sound does Y make?', option_a='e', option_b='y', option_c='i', option_d='a', correct_answer='B', explanation='Y says "y" like Yellow!', hint='💛 y-ellow.', points=5),
            Question(quiz_id=ph4.id, text='What sound does Z make?', option_a='s', option_b='v', option_c='z', option_d='f', correct_answer='C', explanation='Z says "z" like Zebra!', hint='🦓 z-ebra.', points=5),
        ])

    # --- 123 QUIZZES ---
    num1 = add_quiz_if_missing('Count 1-10', '123', 'easy', 'First numbers!')
    if num1:
        add_questions_if_missing(num1, [
            Question(quiz_id=num1.id, text='What number comes after 1?', option_a='3', option_b='2', option_c='4', option_d='5', correct_answer='B', explanation='1, 2!', hint='One, then?', points=5),
            Question(quiz_id=num1.id, text='How many fingers on one hand?', option_a='3', option_b='4', option_c='5', option_d='6', correct_answer='C', explanation='5 fingers!', hint='Count your hand.', points=5),
            Question(quiz_id=num1.id, text='What number is 1 + 1?', option_a='1', option_b='3', option_c='2', option_d='4', correct_answer='C', explanation='1 + 1 = 2!', hint='One and one more.', points=5),
            Question(quiz_id=num1.id, text='What comes after 4?', option_a='3', option_b='5', option_c='6', option_d='7', correct_answer='B', explanation='5 comes after 4!', hint='1, 2, 3, 4, ?', points=5),
            Question(quiz_id=num1.id, text='Biggest number?', option_a='3', option_b='7', option_c='2', option_d='5', correct_answer='B', explanation='7 is biggest!', hint='Count highest.', points=5),
        ])

    num2 = add_quiz_if_missing('Count 11-20', '123', 'easy', 'Teen numbers!')
    if num2:
        add_questions_if_missing(num2, [
            Question(quiz_id=num2.id, text='What comes after 10?', option_a='12', option_b='11', option_c='9', option_d='13', correct_answer='B', explanation='11 comes after 10!', hint='Ten then?', points=5),
            Question(quiz_id=num2.id, text='What is 10 + 5?', option_a='14', option_b='16', option_c='15', option_d='13', correct_answer='C', explanation='10 + 5 = 15!', hint='Count from 10 up 5.', points=5),
            Question(quiz_id=num2.id, text='What comes before 20?', option_a='18', option_b='21', option_c='19', option_d='17', correct_answer='C', explanation='19 comes before 20!', hint='? then 20.', points=5),
            Question(quiz_id=num2.id, text='What number is "fifteen"?', option_a='14', option_b='16', option_c='15', option_d='13', correct_answer='C', explanation='Fifteen is 15!', hint='One and five.', points=5),
            Question(quiz_id=num2.id, text='Count: 13, 14, __?', option_a='16', option_b='15', option_c='12', option_d='17', correct_answer='B', explanation='15!', hint='After fourteen?', points=5),
        ])

    num3 = add_quiz_if_missing('Count 21-50', '123', 'easy', 'Big counting!')
    if num3:
        add_questions_if_missing(num3, [
            Question(quiz_id=num3.id, text='What comes after 20?', option_a='22', option_b='19', option_c='21', option_d='23', correct_answer='C', explanation='21 comes after 20!', hint='Twenty then?', points=5),
            Question(quiz_id=num3.id, text='What is 25 + 5?', option_a='28', option_b='30', option_c='31', option_d='29', correct_answer='B', explanation='25 + 5 = 30!', hint='Twenty-five plus five.', points=5),
            Question(quiz_id=num3.id, text='What comes before 30?', option_a='28', option_b='29', option_c='31', option_d='27', correct_answer='B', explanation='29 comes before 30!', hint='Twenty-?', points=5),
            Question(quiz_id=num3.id, text='What is 40 - 10?', option_a='25', option_b='35', option_c='30', option_d='20', correct_answer='C', explanation='40 - 10 = 30!', hint='Count back from 40.', points=5),
            Question(quiz_id=num3.id, text='Count: 45, 46, __?', option_a='48', option_b='47', option_c='44', option_d='49', correct_answer='B', explanation='47!', hint='After forty-six.', points=5),
        ])

    num4 = add_quiz_if_missing('Count 51-100', '123', 'medium', 'All the way!')
    if num4:
        add_questions_if_missing(num4, [
            Question(quiz_id=num4.id, text='What comes after 50?', option_a='52', option_b='49', option_c='51', option_d='53', correct_answer='C', explanation='51 comes after 50!', hint='Fifty then?', points=5),
            Question(quiz_id=num4.id, text='What is 75 + 25?', option_a='90', option_b='100', option_c='95', option_d='85', correct_answer='B', explanation='75 + 25 = 100!', hint='Three quarters plus one.', points=5),
            Question(quiz_id=num4.id, text='What comes before 100?', option_a='98', option_b='99', option_c='97', option_d='101', correct_answer='B', explanation='99 comes before 100!', hint='Ninety-?', points=5),
            Question(quiz_id=num4.id, text='What is 90 - 30?', option_a='50', option_b='70', option_c='60', option_d='55', correct_answer='C', explanation='90 - 30 = 60!', hint='Count back from 90.', points=5),
            Question(quiz_id=num4.id, text='Count: 88, 89, __?', option_a='91', option_b='87', option_c='90', option_d='92', correct_answer='C', explanation='90!', hint='After eighty-nine.', points=5),
        ])

    # --- MATH QUIZZES ---
    m1 = Quiz(title='Addition Fun', subject_id=1, difficulty='easy', description='Practice adding numbers!')
    m2 = Quiz(title='Subtraction Pro', subject_id=1, difficulty='easy', description='Subtract with ease!')
    m3 = Quiz(title='Multiplication Magic', subject_id=1, difficulty='medium', description='Multiply and conquer!')
    m4 = Quiz(title='Division Debut', subject_id=1, difficulty='medium', description='Learn to divide!')
    m5 = Quiz(title='Fraction Fun', subject_id=1, difficulty='medium', description='Understand fractions!')
    m6 = Quiz(title='Mixed Operations', subject_id=1, difficulty='hard', description='Mix math operations!')
    m7 = Quiz(title='Multiplication Master', subject_id=1, difficulty='hard', description='Advanced multiplication!')
    m8 = Quiz(title='Division Challenge', subject_id=1, difficulty='hard', description='Tougher division problems!')
    db.session.add_all([m1, m2, m3, m4, m5, m6, m7, m8])
    db.session.commit()

    q1 = [
        Question(quiz_id=m1.id, text='2 + 3 = ?', option_a='4', option_b='5', option_c='6', option_d='7', correct_answer='B', explanation='Imagine you have 2 yummy apples, and your friend gives you 3 more! Count them: 1, 2, 3, 4, 5! You now have 5 delicious apples!', hint='Start at 2, then count 3 more: 3, 4, 5!', points=10),
        Question(quiz_id=m1.id, text='7 + 4 = ?', option_a='10', option_b='11', option_c='12', option_d='9', correct_answer='B', explanation='Picture 7 colorful balloons floating in the air. Add 4 more balloons. Now count them all: 8, 9, 10, 11! You have 11 balloons dancing in the breeze!', hint='Start at 7 and count up 4 more friends!', points=10),
        Question(quiz_id=m1.id, text='6 + 6 = ?', option_a='10', option_b='11', option_c='12', option_d='14', correct_answer='C', explanation='Did you know that 6 + 6 is called a "double 6"? Just like having two hands with 6 fingers each - that makes 12 fingers total!', hint='Think of two groups of 6 - double 6 makes 12!', points=10),
        Question(quiz_id=m1.id, text='9 + 5 = ?', option_a='13', option_b='14', option_c='15', option_d='12', correct_answer='B', explanation='Here\'s a clever trick: Take 1 from 5 to make 10 (9+1=10), then add the remaining 4: 10+4=14! Math magic!', hint='Make a friendly 10 first: 9 needs 1 to become 10, then add 4 more!', points=10),
        Question(quiz_id=m1.id, text='8 + 7 = ?', option_a='14', option_b='15', option_c='16', option_d='13', correct_answer='B', explanation='Start at 8 and imagine climbing 7 steps up a magical staircase: 9, 10, 11, 12, 13, 14, 15! You reached the top at 15!', hint='Start at 8 and count up 7 magical steps!', points=10),
    ]
    db.session.add_all(q1)
    db.session.commit()

    q2 = [
        Question(quiz_id=m2.id, text='8 - 3 = ?', option_a='4', option_b='5', option_c='6', option_d='3', correct_answer='B', explanation='Imagine you have 8 colorful candies in your hand. You eat 3 yummy candies - yum! How many are left? Count: 8, 7, 6, 5! You have 5 sweet candies left!', hint='Start at 8, then count backwards: 7, 6, 5!', points=10),
        Question(quiz_id=m2.id, text='10 - 6 = ?', option_a='3', option_b='5', option_c='4', option_d='6', correct_answer='C', explanation='Picture 10 fluffy clouds in the sky. Suddenly, 6 clouds float away behind a mountain. Count the remaining clouds: 10, 9, 8, 7, 4! Only 4 clouds left in the sky!', hint='Count backwards from 10: 9, 8, 7, 6, 5, 4!', points=10),
        Question(quiz_id=m2.id, text='15 - 7 = ?', option_a='7', option_b='8', option_c='9', option_d='6', correct_answer='B', explanation='Here\'s a math secret: 7 + 8 = 15, so if you take away 7 from 15, you get 8! It\'s like a math puzzle that fits together perfectly!', hint='Think: 7 plus what equals 15? That\'s your answer!', points=10),
        Question(quiz_id=m2.id, text='12 - 5 = ?', option_a='6', option_b='8', option_c='7', option_d='5', correct_answer='C', explanation='Imagine you have 12 sparkly stars twinkling at night. 5 stars decide to hide behind a cloud. Count the stars still shining: 12, 11, 10, 9, 8, 7, 6, 5! You see 7 bright stars!', hint='Start at 12 and count back 5 steps!', points=10),
        Question(quiz_id=m2.id, text='20 - 9 = ?', option_a='10', option_b='12', option_c='11', option_d='9', correct_answer='C', explanation='Here\'s a clever trick: 20 - 10 = 10, but you\'re only taking away 9 (which is 1 less than 10), so the answer is 10 + 1 = 11! Math magic!', hint='20 minus 10 is 10, but you have 1 extra, so add 1!', points=10),
    ]
    db.session.add_all(q2)
    db.session.commit()

    q3 = [
        Question(quiz_id=m3.id, text='3 x 4 = ?', option_a='10', option_b='11', option_c='12', option_d='14', correct_answer='C', explanation='3 x 4 = 12!', hint='3 groups of 4.', points=15),
        Question(quiz_id=m3.id, text='5 x 2 = ?', option_a='8', option_b='10', option_c='12', option_d='7', correct_answer='B', explanation='5 x 2 = 10!', hint='Two groups of 5.', points=15),
        Question(quiz_id=m3.id, text='6 x 3 = ?', option_a='16', option_b='18', option_c='20', option_d='15', correct_answer='B', explanation='6 x 3 = 18!', hint='6 + 6 + 6 = ?', points=15),
        Question(quiz_id=m3.id, text='4 x 4 = ?', option_a='14', option_b='16', option_c='18', option_d='12', correct_answer='B', explanation='4 x 4 = 16!', hint='Four groups of 4.', points=15),
        Question(quiz_id=m3.id, text='7 x 2 = ?', option_a='12', option_b='16', option_c='14', option_d='15', correct_answer='C', explanation='7 x 2 = 14!', hint='7 + 7 = ?', points=15),
    ]
    db.session.add_all(q3)
    db.session.commit()

    q4 = [
        Question(quiz_id=m4.id, text='10 ÷ 2 = ?', option_a='4', option_b='5', option_c='6', option_d='3', correct_answer='B', explanation='Imagine you have 10 delicious cookies, and you want to share them equally with your best friend! Split them into 2 equal groups: Group 1 gets 5 cookies, Group 2 gets 5 cookies. Each group has 5 yummy cookies! 10 ÷ 2 = 5!', hint='Close your eyes and imagine 10 cookies. Can you split them into 2 equal, yummy piles?', points=15),
        Question(quiz_id=m4.id, text='12 ÷ 3 = ?', option_a='3', option_b='4', option_c='5', option_d='6', correct_answer='B', explanation='Picture 12 bright balloons floating in the sky. You want to tie them into 3 equal bunches. Bunch 1: 4 balloons, Bunch 2: 4 balloons, Bunch 3: 4 balloons. Each bunch has 4 balloons dancing in the wind! 12 ÷ 3 = 4!', hint='Imagine 3 friends each holding the same number of balloons. 3 groups of 4 = 12!', points=15),
        Question(quiz_id=m4.id, text='8 ÷ 4 = ?', option_a='1', option_b='3', option_c='2', option_d='4', correct_answer='C', explanation='Imagine you have 8 colorful marbles, and you want to put them into 4 small bags. Bag 1: 2 marbles, Bag 2: 2 marbles, Bag 3: 2 marbles, Bag 4: 2 marbles. Each bag has exactly 2 shiny marbles! 8 ÷ 4 = 2!', hint='Picture 4 small treasure chests. Each chest gets the same number of gold coins. 4 groups of 2 = 8!', points=15),
        Question(quiz_id=m4.id, text='15 ÷ 5 = ?', option_a='2', option_b='4', option_c='3', option_d='5', correct_answer='C', explanation='Picture 15 sparkly stars twinkling at night. You want to group them into 5 constellations. Constellation 1: 3 stars, Constellation 2: 3 stars, Constellation 3: 3 stars, Constellation 4: 3 stars, Constellation 5: 3 stars. Each constellation has 3 bright stars! 15 ÷ 5 = 3!', hint='Imagine 5 friends each getting the same number of stickers. 5 groups of 3 = 15!', points=15),
        Question(quiz_id=m4.id, text='20 ÷ 4 = ?', option_a='4', option_b='6', option_c='5', option_d='7', correct_answer='C', explanation='Imagine you have 20 rainbow-colored shells from the beach. You want to put them into 4 beautiful jars. Jar 1: 5 shells, Jar 2: 5 shells, Jar 3: 5 shells, Jar 4: 5 shells. Each jar has exactly 5 gorgeous shells! 20 ÷ 4 = 5!', hint='Picture 4 treasure chests. Each chest contains the same number of pearls. 4 groups of 5 = 20!', points=15),
    ]
    db.session.add_all(q4)
    db.session.commit()

    q5 = [
        Question(quiz_id=m5.id, text='Half of 10 is?', option_a='3', option_b='5', option_c='7', option_d='4', correct_answer='B', explanation='Imagine a yummy pizza cut into 2 equal halves. Each half has 5 slices! 1/2 of 10 = 5. It\'s like sharing your pizza equally with a friend!', hint='Close your eyes and imagine 10 cookies. Now split them into 2 equal, yummy groups!', points=15),
        Question(quiz_id=m5.id, text='1/4 of 12 = ?', option_a='2', option_b='4', option_c='3', option_d='6', correct_answer='C', explanation='Picture a chocolate bar with 12 squares arranged in a grid. If you break off 1/4 (one quarter) of the bar, you get exactly 3 delicious squares! 1/4 of 12 = 3.', hint='Imagine splitting 12 gummy bears into 4 equal groups. How many in each group?', points=15),
        Question(quiz_id=m5.id, text='Which is bigger: 1/2 or 1/4?', option_a='1/2', option_b='1/4', option_c='Same', option_d='Unknown', correct_answer='A', explanation='Think of two pizzas: Pizza A is cut into 2 big slices (1/2 each), Pizza B is cut into 4 small slices (1/4 each). Which slice gives you more? The 1/2 slice is MUCH bigger!', hint='Would you rather have half a pizza or just a quarter? Half is bigger!', points=15),
        Question(quiz_id=m5.id, text='1/3 of 9 = ?', option_a='2', option_b='4', option_c='3', option_d='6', correct_answer='C', explanation='Imagine 9 colorful balloons floating in the sky. You want to tie them into 3 equal bunches. Bunch 1: 3 balloons, Bunch 2: 3 balloons, Bunch 3: 3 balloons. Each bunch has 3 balloons! 1/3 of 9 = 3.', hint='Split 9 sparkly stars into 3 equal constellations. How many stars in each?', points=15),
        Question(quiz_id=m5.id, text='2/4 is the same as?', option_a='1/4', option_b='3/4', option_c='1/2', option_d='1/3', correct_answer='C', explanation='Here\'s a fraction secret: 2/4 is like having 2 out of 4 quarters of a pizza. That\'s the same as 1/2 (half the pizza)! You can simplify fractions by dividing both numbers by 2.', hint='Imagine a pizza cut into 4 slices. If you eat 2 slices, how much is left? You ate half!', points=15),
    ]
    db.session.add_all(q5)
    db.session.commit()

    q6 = [
        Question(quiz_id=m6.id, text='3 + 4 x 2 = ?', option_a='14', option_b='11', option_c='10', option_d='7', correct_answer='B', explanation='3 + (4 x 2) = 3 + 8 = 11!', hint='Multiply first, then add.', points=20),
        Question(quiz_id=m6.id, text='10 - 2 x 3 = ?', option_a='4', option_b='24', option_c='6', option_d='8', correct_answer='A', explanation='10 - (2 x 3) = 10 - 6 = 4!', hint='Multiply first, then subtract.', points=20),
        Question(quiz_id=m6.id, text='5 x 2 + 3 = ?', option_a='13', option_b='25', option_c='16', option_d='10', correct_answer='A', explanation='(5 x 2) + 3 = 10 + 3 = 13!', hint='Multiply first, then add.', points=20),
        Question(quiz_id=m6.id, text='12 ÷ 3 + 2 = ?', option_a='6', option_b='4', option_c='8', option_d='3', correct_answer='A', explanation='(12 ÷ 3) + 2 = 4 + 2 = 6!', hint='Divide first, then add.', points=20),
        Question(quiz_id=m6.id, text='4 + 6 ÷ 2 = ?', option_a='7', option_b='5', option_c='8', option_d='9', correct_answer='A', explanation='4 + (6 ÷ 2) = 4 + 3 = 7!', hint='Divide first, then add.', points=20),
    ]
    db.session.add_all(q6)
    db.session.commit()

    q7 = [
        Question(quiz_id=m7.id, text='8 x 7 = ?', option_a='54', option_b='56', option_c='64', option_d='48', correct_answer='B', explanation='8 x 7 = 56!', hint='8 groups of 7.', points=20),
        Question(quiz_id=m7.id, text='9 x 6 = ?', option_a='54', option_b='56', option_c='45', option_d='63', correct_answer='A', explanation='9 x 6 = 54!', hint='9 groups of 6.', points=20),
        Question(quiz_id=m7.id, text='12 x 5 = ?', option_a='60', option_b='50', option_c='70', option_d='55', correct_answer='A', explanation='12 x 5 = 60!', hint='10 x 5 = 50, plus 2 x 5 = 10.', points=20),
        Question(quiz_id=m7.id, text='11 x 8 = ?', option_a='88', option_b='80', option_c='96', option_d='72', correct_answer='A', explanation='11 x 8 = 88!', hint='10 x 8 = 80, plus 1 x 8 = 8.', points=20),
        Question(quiz_id=m7.id, text='15 x 4 = ?', option_a='50', option_b='60', option_c='55', option_d='65', correct_answer='B', explanation='15 x 4 = 60!', hint='10 x 4 = 40, plus 5 x 4 = 20.', points=20),
    ]
    db.session.add_all(q7)
    db.session.commit()

    q8 = [
        Question(quiz_id=m8.id, text='36 ÷ 6 = ?', option_a='5', option_b='6', option_c='7', option_d='8', correct_answer='B', explanation='36 ÷ 6 = 6!', hint='6 groups of 6 = 36.', points=20),
        Question(quiz_id=m8.id, text='45 ÷ 9 = ?', option_a='4', option_b='6', option_c='5', option_d='7', correct_answer='C', explanation='45 ÷ 9 = 5!', hint='9 groups of 5 = 45.', points=20),
        Question(quiz_id=m8.id, text='64 ÷ 8 = ?', option_a='7', option_b='9', option_c='8', option_d='6', correct_answer='C', explanation='64 ÷ 8 = 8!', hint='8 groups of 8 = 64.', points=20),
        Question(quiz_id=m8.id, text='72 ÷ 9 = ?', option_a='7', option_b='9', option_c='8', option_d='6', correct_answer='C', explanation='72 ÷ 9 = 8!', hint='9 groups of 8 = 72.', points=20),
        Question(quiz_id=m8.id, text='100 ÷ 10 = ?', option_a='100', option_b='1000', option_c='10', option_d='5', correct_answer='C', explanation='100 ÷ 10 = 10!', hint='10 groups of 10 = 100.', points=20),
    ]
    db.session.add_all(q8)
    db.session.commit()

    # --- READING QUIZZES ---
    r1 = Quiz(title='Word Puzzles', subject_id=2, difficulty='easy', description='Find the right word!')
    r2 = Quiz(title='Story Time', subject_id=2, difficulty='medium', description='Read and answer!')
    r3 = Quiz(title='Vocabulary', subject_id=2, difficulty='medium', description='New words!')
    db.session.add_all([r1, r2, r3])
    db.session.commit()

    qr1 = [
        Question(quiz_id=r1.id, text='Which rhymes with "cat"?', option_a='dog', option_b='hat', option_c='sun', option_d='pen', correct_answer='B', explanation='Hat and cat sound alike!', hint='Look for "at".', points=10),
        Question(quiz_id=r1.id, text='Opposite of "hot"?', option_a='warm', option_b='big', option_c='cold', option_d='fast', correct_answer='C', explanation='Cold is opposite of hot.', hint='Winter is cold.', points=10),
        Question(quiz_id=r1.id, text='Starts with "S"?', option_a='apple', option_b='ball', option_c='snake', option_d='dog', correct_answer='C', explanation='Snake starts with S.', hint='Sssnake.', points=10),
        Question(quiz_id=r1.id, text='The sun is ____.', option_a='blue', option_b='bright', option_c='cold', option_d='soft', correct_answer='B', explanation='The sun is bright!', hint='It gives light.', points=10),
        Question(quiz_id=r1.id, text='3 letters?', option_a='apple', option_b='sun', option_c='flower', option_d='fly', correct_answer='B', explanation='Sun has 3 letters.', hint='S-U-N.', points=10),
    ]
    db.session.add_all(qr1)
    db.session.commit()

    qr2 = [
        Question(quiz_id=r2.id, text='Tom has a red ball. Color?', option_a='blue', option_b='green', option_c='red', option_d='yellow', correct_answer='C', explanation='It says "red ball"!', hint='Check the story.', points=10),
        Question(quiz_id=r2.id, text='Sara goes to park. Where?', option_a='school', option_b='park', option_c='home', option_d='store', correct_answer='B', explanation='Park!', hint='Look at the text.', points=10),
        Question(quiz_id=r2.id, text='Bird in tree. What does it do?', option_a='flies', option_b='eats', option_c='sings', option_d='sleeps', correct_answer='C', explanation='Sings!', hint='Happy song.', points=10),
        Question(quiz_id=r2.id, text='Max has 2 dogs, 1 cat. Pets?', option_a='1', option_b='2', option_c='3', option_d='4', correct_answer='C', explanation='2+1=3 pets.', hint='Add them up.', points=10),
        Question(quiz_id=r2.id, text='Raining. Lily opens ___', option_a='book', option_b='umbrella', option_c='toy', option_d='shoes', correct_answer='B', explanation='Umbrella!', hint='Keeps dry.', points=10),
    ]
    db.session.add_all(qr2)
    db.session.commit()

    qr3 = [
        Question(quiz_id=r3.id, text='"Enormous" means?', option_a='small', option_b='big', option_c='fast', option_d='slow', correct_answer='B', explanation='Huge!', hint='Like an elephant.', points=10),
        Question(quiz_id=r3.id, text='"Whisper" means?', option_a='shout', option_b='sing', option_c='speak soft', option_d='laugh', correct_answer='C', explanation='Speak very softly.', hint='Like a secret.', points=10),
        Question(quiz_id=r3.id, text='Same as "happy"?', option_a='sad', option_b='angry', option_c='joyful', option_d='tired', correct_answer='C', explanation='Joyful!', hint='Smiling.', points=10),
        Question(quiz_id=r3.id, text='"Habitat" is?', option_a='food', option_b='home', option_c='school', option_d='game', correct_answer='B', explanation='Where animals live.', hint='Bear lives in forest.', points=10),
        Question(quiz_id=r3.id, text='"Predict" means?', option_a='look back', option_b='guess future', option_c='remember', option_d='write', correct_answer='B', explanation='Guess what will happen.', hint='Before it happens.', points=10),
    ]
    db.session.add_all(qr3)
    db.session.commit()

    # --- SCIENCE QUIZZES ---
    s1 = Quiz(title='Animal Kingdom', subject_id=3, difficulty='easy', description='Amazing animals!')
    s2 = Quiz(title='Weather', subject_id=3, difficulty='easy', description='How weather works!')
    s3 = Quiz(title='Space', subject_id=3, difficulty='medium', description='To the stars!')
    db.session.add_all([s1, s2, s3])
    db.session.commit()

    qs1 = [
        Question(quiz_id=s1.id, text='King of Jungle?', option_a='tiger', option_b='elephant', option_c='lion', option_d='bear', correct_answer='C', explanation='Lion!', hint='Big cat, loud roar.', points=10),
        Question(quiz_id=s1.id, text='Spider legs?', option_a='6', option_b='8', option_c='10', option_d='4', correct_answer='B', explanation='8 legs!', hint='More than insects.', points=10),
        Question(quiz_id=s1.id, text='Which flies?', option_a='dog', option_b='fish', option_c='bird', option_d='cat', correct_answer='C', explanation='Bird!', hint='Has wings.', points=10),
        Question(quiz_id=s1.id, text='Fish live in?', option_a='trees', option_b='water', option_c='sky', option_d='sand', correct_answer='B', explanation='Water!', hint='Swim!', points=10),
        Question(quiz_id=s1.id, text='Gives milk?', option_a='chicken', option_b='cow', option_c='dog', option_d='frog', correct_answer='B', explanation='Cow!', hint='Moo!', points=10),
    ]
    db.session.add_all(qs1)
    db.session.commit()

    qs2 = [
        Question(quiz_id=s2.id, text='Cold sky falls as?', option_a='rain', option_b='sun', option_c='snow', option_d='wind', correct_answer='C', explanation='Snow!', hint='Winter flakes.', points=10),
        Question(quiz_id=s2.id, text='After rain you see?', option_a='moon', option_b='stars', option_c='rainbow', option_d='clouds', correct_answer='C', explanation='Rainbow!', hint='Colorful arc.', points=10),
        Question(quiz_id=s2.id, text='Hottest season?', option_a='winter', option_b='spring', option_c='summer', option_d='fall', correct_answer='C', explanation='Summer!', hint='Swimming time.', points=10),
        Question(quiz_id=s2.id, text='Day light from?', option_a='moon', option_b='stars', option_c='sun', option_d='lamp', correct_answer='C', explanation='Sun!', hint='Shines bright.', points=10),
        Question(quiz_id=s2.id, text='Wind is?', option_a='trees', option_b='moving air', option_c='clouds', option_d='birds', correct_answer='B', explanation='Moving air!', hint='Invisible push.', points=10),
    ]
    db.session.add_all(qs2)
    db.session.commit()

    qs3 = [
        Question(quiz_id=s3.id, text='Closest star?', option_a='Moon', option_b='Mars', option_c='Sun', option_d='Venus', correct_answer='C', explanation='Sun!', hint='In the sky.', points=15),
        Question(quiz_id=s3.id, text='Planets in solar system?', option_a='6', option_b='7', option_c='8', option_d='9', correct_answer='C', explanation='8!', hint='Mercury to Neptune.', points=15),
        Question(quiz_id=s3.id, text='We live on?', option_a='Mars', option_b='Earth', option_c='Jupiter', option_d='Saturn', correct_answer='B', explanation='Earth!', hint='Home.', points=15),
        Question(quiz_id=s3.id, text='Goes around Earth?', option_a='Sun', option_b='Mars', option_c='Moon', option_d='Stars', correct_answer='C', explanation='Moon!', hint='Night light.', points=15),
        Question(quiz_id=s3.id, text='Red Planet?', option_a='Venus', option_b='Mars', option_c='Jupiter', option_d='Saturn', correct_answer='B', explanation='Mars!', hint='Looks red.', points=15),
    ]
    db.session.add_all(qs3)
    db.session.commit()

    # --- GEOGRAPHY QUIZZES ---
    g1 = Quiz(title='Continents', subject_id=4, difficulty='easy', description='Big lands!')
    g2 = Quiz(title='Oceans & Rivers', subject_id=4, difficulty='easy', description='Water world!')
    g3 = Quiz(title='Famous Places', subject_id=4, difficulty='medium', description='World landmarks!')
    db.session.add_all([g1, g2, g3])
    db.session.commit()

    qg1 = [
        Question(quiz_id=g1.id, text='Largest continent?', option_a='Africa', option_b='Asia', option_c='Europe', option_d='America', correct_answer='B', explanation='Asia is biggest!', hint='China is here.', points=10),
        Question(quiz_id=g1.id, text='Coldest continent?', option_a='Antarctica', option_b='Europe', option_c='Australia', option_d='Africa', correct_answer='A', explanation='Antarctica!', hint='Penguins live here.', points=10),
        Question(quiz_id=g1.id, text='USA is in?', option_a='North America', option_b='South America', option_c='Europe', option_d='Asia', correct_answer='A', explanation='North America!', hint='Above South America.', points=10),
        Question(quiz_id=g1.id, text='Africa has the?', option_a='Sahara', option_b='Amazon', option_c='Alps', option_d='Everest', correct_answer='A', explanation='Sahara Desert!', hint='Very sandy.', points=10),
        Question(quiz_id=g1.id, text='Smallest continent?', option_a='Australia', option_b='Europe', option_c='Antarctica', option_d='Asia', correct_answer='A', explanation='Australia!', hint='Kangaroos.', points=10),
    ]
    db.session.add_all(qg1)
    db.session.commit()

    qg2 = [
        Question(quiz_id=g2.id, text='Largest ocean?', option_a='Atlantic', option_b='Pacific', option_c='Indian', option_d='Arctic', correct_answer='B', explanation='Pacific!', hint='Peaceful.', points=10),
        Question(quiz_id=g2.id, text='Longest river?', option_a='Amazon', option_b='Nile', option_c='Mississippi', option_d='Yangtze', correct_answer='B', explanation='Nile!', hint='In Africa.', points=10),
        Question(quiz_id=g2.id, text='How many oceans?', option_a='3', option_b='4', option_c='5', option_d='6', correct_answer='C', explanation='5!', hint='Atlantic, Pacific, Indian, Arctic, Southern.', points=10),
        Question(quiz_id=g2.id, text='Salt water or fresh?', option_a='Salt', option_b='Fresh', option_c='Sweet', option_d='Sour', correct_answer='A', explanation='Salt!', hint='Sea.', points=10),
        Question(quiz_id=g2.id, text='Where rivers end?', option_a='Mountain', option_b='Sea', option_c='Sky', option_d='Forest', correct_answer='B', explanation='Sea!', hint='Ocean.', points=10),
    ]
    db.session.add_all(qg2)
    db.session.commit()

    qg3 = [
        Question(quiz_id=g3.id, text='Great Wall is in?', option_a='India', option_b='China', option_c='Japan', option_d='Russia', correct_answer='B', explanation='China!', hint='Long wall.', points=15),
        Question(quiz_id=g3.id, text='Pyramids are in?', option_a='Mexico', option_b='Egypt', option_c='Peru', option_d='Greece', correct_answer='B', explanation='Egypt!', hint='Pharaohs.', points=15),
        Question(quiz_id=g3.id, text='Eiffel Tower city?', option_a='London', option_b='Paris', option_c='Rome', option_d='Berlin', correct_answer='B', explanation='Paris!', hint='France.', points=15),
        Question(quiz_id=g3.id, text='Taj Mahal is?', option_a='Palace', option_b='Tomb', option_c='School', option_d='Mall', correct_answer='B', explanation='A tomb!', hint='In India.', points=15),
        Question(quiz_id=g3.id, text='Statue of Liberty is?', option_a='USA', option_b='UK', option_c='France', option_d='Italy', correct_answer='A', explanation='USA!', hint='New York.', points=15),
    ]
    db.session.add_all(qg3)
    db.session.commit()

    # --- ART QUIZZES ---
    a1 = Quiz(title='Colors', subject_id=5, difficulty='easy', description='Mix and match!')
    a2 = Quiz(title='Famous Art', subject_id=5, difficulty='easy', description='Masterpieces!')
    a3 = Quiz(title='Instruments', subject_id=5, difficulty='medium', description='Make music!')
    db.session.add_all([a1, a2, a3])
    db.session.commit()

    qa1 = [
        Question(quiz_id=a1.id, text='Red + Blue = ?', option_a='Green', option_b='Purple', option_c='Orange', option_d='Yellow', correct_answer='B', explanation='Purple!', hint='Eggplant color.', points=10),
        Question(quiz_id=a1.id, text='Primary colors?', option_a='RBY', option_b='RGB', option_c='RYB', option_d='GBO', correct_answer='C', explanation='Red, Yellow, Blue!', hint='Mix to make others.', points=10),
        Question(quiz_id=a1.id, text='Opposite of Red?', option_a='Blue', option_b='Green', option_c='Orange', option_d='Yellow', correct_answer='B', explanation='Green!', hint='Color wheel.', points=10),
        Question(quiz_id=a1.id, text='Sky is usually?', option_a='Red', option_b='Yellow', option_c='Blue', option_d='Purple', correct_answer='C', explanation='Blue!', hint='Look up.', points=10),
        Question(quiz_id=a1.id, text='Grass is?', option_a='Red', option_b='Green', option_c='Blue', option_d='Orange', correct_answer='B', explanation='Green!', hint='Trees too.', points=10),
    ]
    db.session.add_all(qa1)
    db.session.commit()

    qa2 = [
        Question(quiz_id=a2.id, text='Mona Lisa painter?', option_a='Van Gogh', option_b='Da Vinci', option_c='Picasso', option_d='Monet', correct_answer='B', explanation='Leonardo da Vinci!', hint='Also inventor.', points=15),
        Question(quiz_id=a2.id, text='Sunflowers painter?', option_a='Van Gogh', option_b='Da Vinci', option_c='Picasso', option_d='Monet', correct_answer='A', explanation='Van Gogh!', hint='Yellow flowers.', points=15),
        Question(quiz_id=a2.id, text='Starry Night is?', option_a='Painting', option_b='Song', option_c='Book', option_d='Movie', correct_answer='A', explanation='Painting!', hint='Night sky swirls.', points=15),
        Question(quiz_id=a2.id, text='Sculpture is?', option_a='Drawing', option_b='Carving', option_c='Photo', option_d='Music', correct_answer='B', explanation='Carving!', hint='3D art.', points=15),
        Question(quiz_id=a2.id, text='Canvas is for?', option_a='Painting', option_b='Singing', option_c='Dancing', option_d='Running', correct_answer='A', explanation='Painting!', hint='Holds paint.', points=15),
    ]
    db.session.add_all(qa2)
    db.session.commit()

    qa3 = [
        Question(quiz_id=a3.id, text='String instrument?', option_a='Drum', option_b='Violin', option_c='Flute', option_d='Trumpet', correct_answer='B', explanation='Violin!', hint='4 strings, bow.', points=15),
        Question(quiz_id=a3.id, text='Piano has?', option_a='Keys', option_b='Strings', option_c='Sticks', option_d='Horns', correct_answer='A', explanation='Keys!', hint='Black and white.', points=15),
        Question(quiz_id=a3.id, text='Trumpet family?', option_a='Woodwind', option_b='Brass', option_c='String', option_d='Percussion', correct_answer='B', explanation='Brass!', hint='Shiny metal.', points=15),
        Question(quiz_id=a3.id, text='Drums are?', option_a='String', option_b='Wind', option_c='Percussion', option_d='Brass', correct_answer='C', explanation='Percussion!', hint='Hit them.', points=15),
        Question(quiz_id=a3.id, text='Flute is?', option_a='Woodwind', option_b='Brass', option_c='String', option_d='Percussion', correct_answer='A', explanation='Woodwind!', hint='Blow across.', points=15),
    ]
    db.session.add_all(qa3)
    db.session.commit()

    # --- CODING QUIZZES ---
    c1 = Quiz(title='Logic Puzzles', subject_id=6, difficulty='easy', description='Think like a computer!')
    c2 = Quiz(title='Algorithms', subject_id=6, difficulty='medium', description='Step by step!')
    c3 = Quiz(title='Binary', subject_id=6, difficulty='medium', description='0s and 1s!')
    db.session.add_all([c1, c2, c3])
    db.session.commit()

    qc1 = [
        Question(quiz_id=c1.id, text='Computer language?', option_a='English', option_b='Code', option_c='Spanish', option_d='Latin', correct_answer='B', explanation='Code!', hint='Instructions.', points=10),
        Question(quiz_id=c1.id, text='What is a bug?', option_a='Insect', option_b='Error', option_c='Feature', option_d='Game', correct_answer='B', explanation='Error!', hint='Fix it.', points=10),
        Question(quiz_id=c1.id, text='Repeat action is?', option_a='Loop', option_b='Jump', option_c='Stop', option_d='Run', correct_answer='A', explanation='Loop!', hint='Again and again.', points=10),
        Question(quiz_id=c1.id, text='Input device?', option_a='Screen', option_b='Keyboard', option_c='Speaker', option_d='Printer', correct_answer='B', explanation='Keyboard!', hint='Type on it.', points=10),
        Question(quiz_id=c1.id, text='Output device?', option_a='Mouse', option_b='Keyboard', option_c='Screen', option_d='Webcam', correct_answer='C', explanation='Screen!', hint='Shows results.', points=10),
    ]
    db.session.add_all(qc1)
    db.session.commit()

    qc2 = [
        Question(quiz_id=c2.id, text='Algorithm is?', option_a='Steps', option_b='Food', option_c='Game', option_d='Song', correct_answer='A', explanation='Steps!', hint='Recipe for code.', points=15),
        Question(quiz_id=c2.id, text='IF statement?', option_a='Choice', option_b='Loop', option_c='Number', option_d='Word', correct_answer='A', explanation='Choice!', hint='If this, then that.', points=15),
        Question(quiz_id=c2.id, text='Variable stores?', option_a='Power', option_b='Data', option_c='Music', option_d='Air', correct_answer='B', explanation='Data!', hint='Like a box.', points=15),
        Question(quiz_id=c2.id, text='Debug means?', option_a='Create', option_b='Delete', option_c='Fix', option_d='Run', correct_answer='C', explanation='Fix!', hint='Remove bugs.', points=15),
        Question(quiz_id=c2.id, text='Start of program?', option_a='End', option_b='Start', option_c='Middle', option_d='Loop', correct_answer='B', explanation='Start!', hint='Beginning.', points=15),
    ]
    db.session.add_all(qc2)
    db.session.commit()

    qc3 = [
        Question(quiz_id=c3.id, text='Binary uses?', option_a='1-10', option_b='A-Z', option_c='0-1', option_d='!@#', correct_answer='C', explanation='0 and 1!', hint='Yes/No.', points=15),
        Question(quiz_id=c3.id, text='10 in binary?', option_a='10', option_b='1010', option_c='11', option_d='111', correct_answer='B', explanation='1010!', hint='8+2.', points=15),
        Question(quiz_id=c3.id, text='Bit means?', option_a='Binary Digit', option_b='Big Byte', option_c='Base Item', option_d='Byte', correct_answer='A', explanation='Binary Digit!', hint='Smallest unit.', points=15),
        Question(quiz_id=c3.id, text='Byte has bits?', option_a='4', option_b='8', option_c='16', option_d='32', correct_answer='B', explanation='8 bits!', hint='Half dozen + 2.', points=15),
        Question(quiz_id=c3.id, text='1111 in decimal?', option_a='10', option_b='12', option_c='15', option_d='14', correct_answer='C', explanation='15!', hint='8+4+2+1.', points=15),
    ]
    db.session.add_all(qc3)
    db.session.commit()

    # --- MUSIC QUIZZES ---
    u1 = Quiz(title='Basics', subject_id=7, difficulty='easy', description='Notes and rhythm!')
    u2 = Quiz(title='Instruments 2', subject_id=7, difficulty='easy', description='Sound makers!')
    u3 = Quiz(title='Famous Songs', subject_id=7, difficulty='medium', description='Tunes you know!')
    db.session.add_all([u1, u2, u3])
    db.session.commit()

    qu1 = [
        Question(quiz_id=u1.id, text='Music symbols?', option_a='Notes', option_b='Letters', option_c='Numbers', option_d='Shapes', correct_answer='A', explanation='Notes!', hint='♩', points=10),
        Question(quiz_id=u1.id, text='High sound is?', option_a='Low', option_b='Treble', option_c='Bass', option_d='Loud', correct_answer='B', explanation='Treble!', hint='High pitch.', points=10),
        Question(quiz_id=u1.id, text='Low sound is?', option_a='Treble', option_b='Bass', option_c='Soft', option_d='Fast', correct_answer='B', explanation='Bass!', hint='Deep.', points=10),
        Question(quiz_id=u1.id, text='Fast music is?', option_a='Adagio', option_b='Allegro', option_c='Largo', option_d='Slow', correct_answer='B', explanation='Allegro!', hint='Quickly.', points=10),
        Question(quiz_id=u1.id, text='Slow music is?', option_a='Allegro', option_b='Presto', option_c='Largo', option_d='Fast', correct_answer='C', explanation='Largo!', hint='Slowly.', points=10),
    ]
    db.session.add_all(qu1)
    db.session.commit()

    qu2 = [
        Question(quiz_id=u2.id, text='Guitar strings?', option_a='4', option_b='5', option_c='6', option_d='7', correct_answer='C', explanation='6!', hint='Standard guitar.', points=10),
        Question(quiz_id=u2.id, text='Violin played with?', option_a='Hands', option_b='Bow', option_c='Stick', option_d='Blow', correct_answer='B', explanation='Bow!', hint='Hair and wood.', points=10),
        Question(quiz_id=u2.id, text='Piano keys?', option_a='66', option_b='88', option_c='100', option_d='50', correct_answer='B', explanation='88!', hint='Black and white.', points=10),
        Question(quiz_id=u2.id, text='Saxophone is?', option_a='Woodwind', option_b='Brass', option_c='String', option_d='Percussion', correct_answer='A', explanation='Woodwind!', hint='Uses reed.', points=10),
        Question(quiz_id=u2.id, text='Cymbals family?', option_a='String', option_b='Percussion', option_c='Brass', option_d='Woodwind', correct_answer='B', explanation='Percussion!', hint='Clash them.', points=10),
    ]
    db.session.add_all(qu2)
    db.session.commit()

    qu3 = [
        Question(quiz_id=u3.id, text='Beethoven was?', option_a='Singer', option_b='Composer', option_c='Dancer', option_d='Painter', correct_answer='B', explanation='Composer!', hint='Classical music.', points=15),
        Question(quiz_id=u3.id, text='Twinkle Twinkle is?', option_a='Lullaby', option_b='Rock', option_c='Rap', option_d='Jazz', correct_answer='A', explanation='Lullaby!', hint='For sleeping.', points=15),
        Question(quiz_id=u3.id, text='Mozart wrote?', option_a='Songs', option_b='Symphonies', option_c='Poems', option_d='Stories', correct_answer='B', explanation='Symphonies!', hint='Orchestras.', points=15),
        Question(quiz_id=u3.id, text='National Anthem?', option_a='Lullaby', option_b='Patriotic', option_c='Dance', option_d='Pop', correct_answer='B', explanation='Patriotic!', hint='Country song.', points=15),
        Question(quiz_id=u3.id, text='Happy Birthday is?', option_a='Rock', option_b='Celebration', option_c='Sad', option_d='Fast', correct_answer='B', explanation='Celebration!', hint='Cakes.', points=15),
    ]
    db.session.add_all(qu3)
    db.session.commit()

    # --- STORIES ---
    seed_stories()

    # --- ADDITIONAL QUESTIONS (20-100 per subject) ---
    from seed_more_questions import seed_more_questions as seed_extra_qs
    seed_extra_qs()

    print("Database seeded successfully!")


def seed_stories():
    """Seed database with children's stories across various genres."""
    from models import Story

    # Check if Swahili stories already exist
    if Story.query.filter_by(language='sw').first():
        return

    stories = []
    # Only add English stories if none exist yet
    if not Story.query.first():
        stories = [
        # FOLKTALES
        Story(
            title="The Tortoise and the Hare",
            content="Once upon a time, in a lush green forest filled with tall trees and colorful flowers, there lived a very fast Hare who could run like the wind. He was so proud of his speed that he would laugh at anyone slower than him.\n\n'You are as slow as a sleepy snail!' he would tease the Tortoise, flicking his long ears back and forth with confidence.\n\nThe Tortoise, however, simply smiled calmly and said, 'My friend, speed is not everything. I may be slow, but I can beat you in a race any day.'\n\nThe Hare threw his head back and laughed until his sides hurt. 'A race? YOU want to race ME? This will be the easiest win of my life!'\n\nSoon, all the forest animals gathered - the squirrel, the deer, the fox, and even the wise old owl came to watch. The Fox marked the starting line near the oak tree and the finish line far across the sun-dappled meadow.\n\n'Ready, set, GO!' shouted the Fox.\n\nZOOM! The Hare dashed ahead like a lightning bolt, his legs blurring with speed. He was so far in front that he couldn't even see the Tortoise behind him. 'This is too easy,' he thought, slowing to a walk. 'I have plenty of time for a little nap under this shady tree.'\n\nSo the Hare curled up in the cool grass, listened to the birds singing, and fell into a deep, peaceful sleep. Meanwhile, the Tortoise kept plodding along, slow and steady, never stopping, never giving up, one careful step after another.\n\nWhen the Hare finally woke up with a start, the sun was high in the sky. He looked around in panic, his heart pounding. There, near the finish line, was the Tortoise, taking his final careful steps!\n\nThe Hare sprinted as fast as he could, his paws flying, but it was too late. The Tortoise crossed the finish line first, greeted by cheers from all the animals!\n\nThat day, the Hare learned an important lesson that he never forgot: slow and steady wins the race. And the Tortoise? He just smiled and kept walking.",
            story_type="folktale",
            age_range="6-10",
            reading_time=7,
            points_earned=15
        ),
        Story(
            title="Anansi and the Wisdom Pot",
            content="Long ago in West Africa, the sky god Nyame had a pot full of all the wisdom in the world. He kept it locked away because he didn't want anyone else to be wise.\n\nAnansi the Spider wanted that wisdom. He went to Nyame and said, 'Great Sky God, please give me the pot of wisdom.'\n\nNyame laughed. 'It is too heavy for you, little spider. But if you can capture these three creatures: the python, the leopard, and the hornet, I will give it to you.'\n\nAnansi was clever. First, he caught the leopard by digging a deep pit and covering it with sticks and leaves. The leopard fell in! Then Anansi offered to help him out - if the leopard promised to be his prisoner.\n\nNext, Anansi caught the python by convincing him to stretch out straight so they could see who was longer. Then he tied the python to a bamboo stick!\n\nFor the hornets, Anansi filled a calabash with water and poured it over the nest, shouting, 'It's raining! Get in this dry gourd!' The hornets flew inside to stay dry, and Anansi quickly covered it.\n\nNyame was impressed! He gave Anansi the wisdom pot. But as Anansi climbed the tall tree to take it home, he thought, 'Why should I share this wisdom? I want it all for myself!'\n\nHe tied the pot to his chest and climbed. But it kept bumping his belly, making it hard to climb. A little bird flying by said, 'Why don't you tie it to your back instead?'\n\nAnansi was so surprised that someone so small could give him advice that he dropped the pot. It shattered on the ground, and all the wisdom spilled out, soaking into the earth for everyone to share.\n\nAnd that's why today, wisdom belongs to everyone - not just one person.",
            story_type="folktale",
            age_range="8-12",
            reading_time=7,
            points_earned=20
        ),

        # MORAL STORIES
        Story(
            title="The Boy Who Cried Wolf",
            content="There was once a young shepherd boy who looked after a flock of sheep. He lived in a village near a forest and would take the sheep to graze on the hillside every day.\n\nOne day, the boy felt bored. He thought, 'I'll play a trick on the villagers. I'll shout that a wolf is coming!'\n\nSo he cupped his hands around his mouth and shouted, 'WOLF! WOLF! A wolf is attacking the sheep!'\n\nThe villagers heard his cries and rushed up the hill with sticks and tools to chase the wolf away. When they arrived, they found... no wolf. The sheep were peacefully grazing, and the boy was rolling on the ground laughing.\n\n'You tricked us!' the villagers said angrily. 'That was NOT funny!'\n\nThe boy just laughed. A few days later, he was bored again. 'WOLF! WOLF!' he shouted. 'A big wolf is eating the sheep!'\n\nAgain, the villagers dropped their work and ran up the hill. Again, there was no wolf. The boy laughed even harder this time.\n\n'That boy is a liar,' the villagers grumbled. 'We won't believe him anymore.'\n\nOne day, a REAL wolf came to the hillside. It snuck into the flock and grabbed a sheep! The boy screamed at the top of his lungs, 'WOLF! WOLF! HELP! A REAL WOLF!'\n\nBut the villagers heard him and said, 'He's tricking us again. Let him cry.'\n\nNobody came to help. The wolf ate several sheep before it ran away. The boy cried and cried, but it was too late.\n\nHe learned the hard way: nobody believes a liar, even when they tell the truth.",
            story_type="moral",
            age_range="6-10",
            reading_time=5,
            points_earned=15
        ),
        Story(
            title="The Giving Tree",
            content="Once there was a tree, and she loved a little boy. Every day the boy would come and gather her leaves to make crowns, climb her trunk, swing from her branches, and eat her apples.\n\nThe tree was happy. But as the boy grew older, he didn't come as often. One day he came and the tree said, 'Come play with me!' But the boy said, 'I'm too big to climb trees. I want money. Can you give me some money?'\n\n'I have no money,' said the tree. 'But take my apples, sell them in the city, and you'll have money.'\n\nThe boy took all the apples and left. The tree was happy. But the boy didn't come back for a long time. When he finally returned, he said, 'I'm a man now. I need a house. Can you give me a house?'\n\n'Cut down my branches and build a house,' said the tree. The boy cut off all her branches and carried them away. The tree was happy, but not really.\n\nYears later, the boy came back, now an old man. 'I'm tired,' he said. 'I need a boat to sail far away.'\n\n'Cut down my trunk and make a boat,' said the tree. So the boy cut down her trunk. Now the tree was just a stump, and she was sad.\n\nMany years passed. The old man returned one last time. 'I'm sorry,' he said. 'I have nothing left to give you.'\n\n'I don't need much,' said the old man. 'Just a quiet place to sit.'\n\n'Good!' said the tree, now just a stump. 'An old stump is a good place to sit.'\n\nAnd the old man sat down. And the tree was happy.",
            story_type="moral",
            age_range="8-12",
            reading_time=6,
            points_earned=20
        ),

        # FUNNY STORIES
        Story(
            title="The Day the Crayons Quit",
            content="One morning, Duncan went to his desk to color. But when he opened his crayon box, there was a stack of letters instead of crayons!\n\nThe Red Crayon wrote: 'Dear Duncan, You use me too much! I need a break. Your friend, Red (who is very tired)'\n\nThe Green Crayon wrote: 'Dear Duncan, My brother and I are happy. But stop coloring outside the lines! It makes us look messy. Green'\n\nThe Yellow Crayon wrote: 'Dear Duncan, Orange and I are in a fight. He says he's the color of the sun. I say I'M the color of the sun. Can you decide? Yellow'\n\nThe Blue Crayon wrote: 'Dear Duncan, Remember when you colored the whole ocean blue? My tip is worn down to nothing! I need a vacation. Blue'\n\nThe Pink Crayon wrote: 'Dear Duncan, You never use me! I sit here all day while you use Red and Purple. I want to color something pretty! Pink'\n\nThe Black Crayon wrote: 'Dear Duncan, I am NOT just for outlining! I want to color inside too! Black (feeling gloomy)'\n\nDuncan read all the letters and felt bad. So he got a big piece of paper and made a picture using ALL the crayons the way they wanted:\n- Red colored a fire truck and stop sign\n- Green colored inside the lines\n- Yellow and Orange both colored the sun together\n- Blue colored a small pond (not the whole ocean!)\n- Pink colored a beautiful butterfly\n- Black colored a big, dark night sky\n\nThe crayons were so happy! They all went back in the box, ready to color again. And Duncan learned to share his crayons equally.",
            story_type="funny",
            age_range="6-10",
            reading_time=5,
            points_earned=15
        ),
        Story(
            title="The Mixed-Up Animal Birthday",
            content="It was Benny's birthday, and all the animals were coming to his party. But Benny's mom mixed up the invitations!\n\nFirst, the Elephant arrived wearing swimming goggles. 'I heard it's a pool party!' he said.\n\n'No,' said Benny. 'It's a birthday party. But you can still come!'\n\nThen the Fish arrived wearing a winter coat and boots. 'Brrr! I heard it's a ski party!'\n\n'No,' laughed Benny. 'It's my birthday party!'\n\nNext came the Bird wearing a hard hat and carrying a hammer. 'I heard we're building a house!'\n\n'No!' said Benny, giggling. 'It's my BIRTHDAY party!'\n\nThen the Giraffe arrived wearing a scuba tank. 'Ready to dive!' he said.\n\nThe Monkey arrived with a tennis racket. The Penguin came with a sunscreen bottle. The Kangaroo came with ice skates!\n\nBenny's mom came out and saw all the confused animals. 'Oh my!' she said. 'I sent the wrong invitations!'\n\nEveryone laughed. They took off their silly outfits and put on birthday hats instead. They ate cake, played games, and had the mixed-up birthday party ever!\n\nAnd from that day on, Benny's mom double-checked her invitations.",
            story_type="funny",
            age_range="6-9",
            reading_time=4,
            points_earned=15
        ),

        # EDUCATIONAL STORIES
        Story(
            title="The Journey of a Little Seed",
            content="Once there was a tiny seed named Sam. Sam lived in a beautiful apple with his brothers and sisters. But one day, a bird ate the apple!\n\nSam felt himself going down, down, down into the bird's tummy. 'This is scary!' he thought. But soon, the bird flew far away and... plop! Sam came out in a new place with dirt all around.\n\n'Hello?' Sam called out. 'Where am I?'\n\nThe Earth said, 'You're in the soil, little seed. Drink the water, feel the sun, and you'll grow!'\n\nSam drank rainwater. He felt the warm sunshine. Something amazing happened - his shell cracked open!\n\nFirst came a tiny root, reaching down into the darkness. 'I'm looking for water!' the root said. Then came a green sprout, pushing up toward the light. 'I'm looking for the sun!'\n\nDays passed. The sprout became a stem. Leaves unfurled like little green flags. 'We catch sunlight!' the leaves said. 'We make food for the plant!'\n\nMonths passed. Sam was now a small tree. His leaves made food. His roots drank water. He grew taller and stronger.\n\nOne spring, something special happened. Pink blossoms appeared all over Sam! Bees came to visit, carrying pollen from flower to flower.\n\nAfter the flowers fell off, tiny green balls appeared. They grew bigger and bigger. They turned red. They became apples!\n\nAnd inside those apples? New little seeds, just like Sam. Ready to start their own journey someday.",
            story_type="educational",
            age_range="7-11",
            reading_time=6,
            points_earned=20,
            related_subject_id=3  # Science
        ),
        Story(
            title="The Number Adventure",
            content="Once upon a time, in the Land of Math, lived numbers 1, 2, 3, 4, and 5. They were best friends and loved to play together.\n\nOne day, 1 said, 'Let's make a bigger number!'\n\n'How?' asked 2.\n\n'Watch!' said 1. He stood next to 2. 'Now we are 12!'\n\nBut 3 shook his head. 'That's just putting numbers together. Let me show you real math!'\n\n3 found 2 more friends hiding behind a tree. '1, 2, come out!' he called. Two little 1s came out.\n\n'Now,' said 3, 'watch this magic: 3 plus 1 plus 1 equals... 5!'\n\nThe numbers cheered! 'Again, again!'\n\nThis time, 5 wanted to try. 'I have 5 apples,' he said. 'If I give 2 to 3, how many do I have left?'\n\n5 closed his eyes and thought: '5 take away 2... that leaves 3!'\n\n'Correct!' cheered the others.\n\nThen they tried multiplication. 2 brought his twin brother. Now there were two 2s.\n\n'Two groups of two,' said 2. 'That's 2 times 2. And the answer is... 4!'\n\nThe numbers danced with joy. They learned that day that math isn't just about numbers - it's about the amazing things numbers can do when they work together!\n\nAnd if you listen carefully in the Land of Math, you can still hear them singing: '1, 2, 3, 4, 5 - math is fun and math is alive!'",
            story_type="educational",
            age_range="6-10",
            reading_time=5,
            points_earned=20,
            related_subject_id=1  # Math
        ),

        # ADVENTURE STORIES
        Story(
            title="The Secret of the Hidden Cave",
            content="Maya and her dog Rocky were exploring the beach during their summer vacation. The tide was low, revealing rocks and pools they had never seen before.\n\n'Look, Rocky!' Maya pointed to a dark opening between two big rocks. 'It's a cave!'\n\nRocky wagged his tail and sniffed the entrance. Maya grabbed her flashlight and ducked inside. The cave was cool and smelled like salt and seaweed.\n\nThey walked deeper. Suddenly, Rocky started barking. 'What is it, boy?'\n\nThere, on the cave wall, was a message written in old, faded paint: 'X marks the spot where the treasure sits.'\n\nMaya's heart raced. She shined her light around. There was a big X painted on the ground! She and Rocky dug with their hands. Sand flew everywhere!\n\nClink! Rocky's paw hit something hard. They dug faster and pulled out... an old tin box!\n\nMaya opened it with shaking hands. Inside were shells - hundreds of beautiful seashells in every color! There were also drawings on the box lid showing the cave and the beach from long ago.\n\n'Someone left these shells for people to find,' Maya whispered. She took one beautiful purple shell for herself and left the rest for other explorers to find.\n\nAs they walked back to the beach, the tide was coming in. The cave entrance slowly disappeared under the waves.\n\nMaya smiled. It was their secret adventure, and she had a purple shell to prove it really happened!",
            story_type="adventure",
            age_range="7-12",
            reading_time=6,
            points_earned=20
        ),
        Story(
            title="The Mysterious Map in the Attic",
            content="Sam was helping his grandmother clean the attic when he found an old wooden chest covered in dust. Inside was a yellowed map with strange symbols and a big red X.\n\n'Grandma, what's this?' Sam asked.\n\nGrandma's eyes lit up. 'That's the map your grandfather made when he was your age! He always said there was a secret in the old oak tree in the backyard.'\n\nSam raced to the backyard with the map. The old oak tree was enormous, with branches that reached like arms into the sky. He studied the map - it showed a hollow in the third branch from the left.\n\nSam climbed carefully. The branch creaked but held strong. He reached into the hollow... and pulled out a rusty tin can!\n\nInside was a notebook filled with his grandfather's handwriting. 'Dear finder,' it began. 'If you're reading this, you're as curious as I was!'\n\nThe notebook was filled with drawings of birds, insects, and plants his grandfather had seen in the backyard. On the last page, it said: 'The real treasure is curiosity. Keep exploring!'\n\nSam smiled. He grabbed his own notebook and started drawing the birds he could see right now. His grandfather was right - curiosity was the greatest adventure of all.",
            story_type="adventure",
            age_range="8-12",
            reading_time=6,
            points_earned=20
        ),

        # IMAGINATION STORIES
        Story(
            title="The Cloud Castle",
            content="Lily was lying on the grass, watching the clouds float by, when she saw a very special one. It looked exactly like a castle with towers and a drawbridge!\n\n'Wait for me!' she called. She closed her eyes and imagined herself floating up, up, up into the sky.\n\nWhen she opened her eyes, she was standing on a fluffy white drawbridge. The Cloud Castle was even more beautiful up close. The walls were made of wispy clouds, and the towers touched the sun!\n\nA cloud dragon flew down to greet her. He was made entirely of white mist, and when he breathed, little cloud puffs came out. 'Welcome, Lily! I'm Misty. Come meet the Cloud People!'\n\nInside the castle, everything was soft and bouncy. The chairs were cloud cushions. The tables were flat clouds. And the Cloud People were the friendliest people Lily had ever met!\n\nThey showed her the Cloud Garden where cloud flowers grew - dandelions that floated, roses that rained petals, and sunflowers that followed you around!\n\nThen they went to the Rainbow Room. 'This is where rainbows are made,' said the Cloud Queen. She mixed colors in cloud bowls: red, orange, yellow, green, blue, indigo, violet - and threw them into the sky!\n\nA beautiful rainbow arched across the world below. Lily could see her house! It looked like a tiny dollhouse.\n\n'Time to go home,' said Misty the dragon. He gave Lily a ride on his back, soaring through the sunset colors.\n\nLily opened her eyes. She was back on the grass. But in her hand was a soft, wispy cloud petal that proved her adventure was real!",
            story_type="imagination",
            age_range="6-10",
            reading_time=6,
            points_earned=20
        ),
        Story(
            title="The Door to Nowhere",
            content="Timmy found an old door leaning against the wall in his basement. It had no frame, no hinges, no handle - just a plain wooden door with a sign that said: 'KNOCK THREE TIMES.'\n\nTimmy knocked: knock, knock, knock.\n\nThe door slowly creaked open... and behind it was nothing. Just a swirling purple mist.\n\nTimmy stepped through - and landed on a giant floating marshmallow! He was in a world where everything was made of candy and sweets.\n\nThe trees had chocolate bark and gummy leaves. The river flowed with strawberry milkshake. The grass was made of green cotton candy that tasted like mint!\n\nA unicorn made of spun sugar trotted over. 'Welcome to Sweet World! I'm Sprinkles. Come meet the Candy King!'\n\nThey walked to a castle made of gingerbread. The walls were decorated with colorful candy gems. The Candy King sat on a throne of lollipops.\n\n'We have a problem,' said the King. 'The Sour Troll has been turning our sweet rivers into sour lemon juice!'\n\nTimmy wanted to help. He remembered his grandma's secret - honey makes everything sweet again! He had a jar of honey in his pocket (he always carried snacks).\n\nTimmy poured honey into the river. Slowly, the sour juice turned back into sweet strawberry milkshake!\n\nThe Candy King cheered. 'You saved us! Here's a gift.' He gave Timmy a seed that grew candy canes when you planted it.\n\nTimmy stepped back through the door and found himself in his basement. In his hand was a candy cane growing from a tiny seed. The door had disappeared.\n\nBut every time Timmy eats a candy cane now, he remembers his sweet adventure!",
            story_type="imagination",
            age_range="6-11",
            reading_time=7,
            points_earned=20
        ),
    ]

    swahili_stories = [
        # HADITHI ZA KIENYEJI (Folktales)
        Story(
            title="Sungura na Kobe",
            content="Hapo zamani za kale, katika msitu mnene wenye miti mirefu na maua ya rangi mbalimbali, aliishi Sungura aliyejivunia kukimbia kwa kasi. Alikuwa na fahari kubwa na mara nyingi aliwacheka wanyama wengine wenye mwendo wa polepole.\n\n'Wewe ni mwoga kama konokono!' alimtania Kobe, akitikisa masikio yake marefu.\n\nKobe alitabasamu kwa utulivu na kusema: 'Rafiki yangu, si kila kitu ni kasi. Ninaweza kukushinda mbio siku yoyote.'\n\nSungura alicheka kwa sauti: 'WEWE? Wewe unataka kukimbiana na MIMI? Hii itakuwa rahisi kwangu!'\n\nWanyama wote wakakutana - kundi, swala, mbweha, na hata bundi mwenye busara. Mbweha aliweka alama mwanzo na mwisho wa mbio shambani.\n\n'Tayari, weka, ENDA!' Mbweha akaamuru.\n\nNYOOSH! Sungura aliruka mbele kama mwale wa umeme. Alipokuwa mbele sana hakumwona Kobe nyuma yake. 'Hii ni rahisi sana,' aliwaza. 'Nina muda wa kupumzika kidogo chini ya mti huu.'\n\nBasi Sungura alijikunyata kwenye nyasi laini, akasikiliza ndege wakiimba, na usingizi ukamzibua.\n\nWakati huo huo, Kobe aliendelea kutembea polepole, hatua kwa hatua, bila kusimama, bila kukata tamaa.\n\nSungura alipoamka, jua lilikuwa juu angani! Alitazama kwa hofu - na kumwona Kobe akikaribia mstari wa mwisho!\n\nSungura alikimbia kwa mwendo wa umeme, lakini ilikuwa kuchelewa. Kobe alivuka mstari wa mwisho kwanza, huku wanyama wote wakishangilia!\n\nSiku hiyo, Sungura alijifunza somo muhimu: mwendo wa polepole huvunja gogo.",
            story_type="folktale",
            age_range="6-10",
            reading_time=6,
            language="sw",
            points_earned=15
        ),
        Story(
            title="Anansi na Chungu cha Hekima",
            content="Hapo zamani za mbali katika Afrika Magharibi, mungu wa anga aliitwa Nyame alikuwa na chungu kilichojaa hekima yote duniani. Alikificha kwa sababu hakutaka mtu mwingine awe na hekima.\n\nAnansi buibui alitaka hekima hiyo. Alimwendea Nyame na kusema: 'Mungu mkuu, naomba unipe chungu cha hekima.'\n\nNyame alicheka. 'Ni kizito kwako, buibui mdogo. Lakini ukinikamata chatu, chui, na nyigu, nitakupa.'\n\nAnansi alikuwa mjanja. Kwanza, alimkamata chui kwa kuchimba shimo refu na kulifunika kwa majani na vijiti. Chui akaanguka ndani! Kisha Anansi akamtoa - kwa sharti la kuwa mteswa wake.\n\nPili, Anansi alimkamata chatu kwa kumshawishi anyooshe mwili wake wote ili waone nani mrefu zaidi. Kisha akamfunga chatu kwenye fimbo!\n\nKwa nyigu, Anansi alijaza kibuyu kwa maji na kumwaga juu ya kiota wakiwa wamelala, akipiga kelele: 'Kunanyesha! Ingilieni kwenye kibuyu hiki kikavu!' Nyigu wakaruka ndani ili kukaa mahali pakavu, na Anansi akafunga mdomo wa kibuyu.\n\nNyame alishangazwa! Akampa Anansi chungu cha hekima. Lakini Anansi alipokuwa akipanda mti mrefu kuchukua chungu nyumbani, aliwaza: 'Kwa nini nishiriki hekima hii? Nataka yote mwenyewe!'\n\nAlifunga chungu mbele ya kifua chake na kupanda. Lakini chungu kiligonga tumbo lake na kufanya iwe vigumu kupanda. Ndege mdogo aliyekuwa akipita akasema: 'Kwa nini usifunge nyuma yako?'\n\nAnansi alishangaa sana kwamba mdogo kama ndege anaweza kumpa ushauri hata akalishusha chungu. Kilivunjika vipande vipande, na hekima yote ikamwagika, ikiingia ardhini kwa kila mtu.\n\nNdiyo maana leo, hekima ni ya kila mtu - si ya mtu mmoja tu.",
            story_type="folktale",
            age_range="8-12",
            reading_time=7,
            language="sw",
            points_earned=20
        ),

        # HADITHI ZA MAADILI (Moral Stories)
        Story(
            title="Mvulana Aliyeita Mbwa Mwitu",
            content="Hapo zamani, alikuwa na mvulana mchungaji aliyechunga kondoo. Aliishi katika kijiji karibu na msitu na kila siku aliwapeleka kondoo malishoni.\n\nSiku moja, mvulana alichoka. 'Nitawachezea watu wa kijijini,' aliwaza. 'Nitapiga kelele kwamba mbwa mwitu anakuja!'\n\nBasi akaweka mikono midomoni na kupiga kelele: 'MBWA MWITU! MBWA MWITU! Kondoo wanaliwa!'\n\nWatu wa kijijini walimsikia na wakakimbilia mlimani na fimbo na mundu kumfukuza mbwa mwitu. Walipofika... hakukuwa na mbwa mwitu. Kondoo walikuwa wanakula amani, na mvulana alikuwa anaviringika chini akicheka.\n\n'Umekwisha tudanganya!' watu walisema kwa hasira. 'Hilo si jambo la kuchekesha!'\n\nMvulana aliendelea kucheka. Baada ya siku kadhaa, alichoka tena. 'MBWA MWITU! MBWA MWITU!' 'Kuna mbwa mwitu mkubwa anawala kondoo!'\n\nTena, watu waliacha shughuli zao na kukimbilia mlimani. Tena, hapakuwa na mbwa mwitu. Mvulana alicheka zaidi.\n\n'Mvulana huyo ni mwongo,' watu walinung'unika. 'Hatutamwamini tena.'\n\nSiku moja, mbwa mwitu wa kweli alikuja. Alijinyatia kwenye kundi na kumnyakua kondoo! Mvulana alipiga kelele kwa nguvu zake zote: 'MBWA MWITU! MBWA MWITU! MSAIDIE! MBWA MWITU WA KWELI!'\n\nLakini watu walimsikia na kusema: 'Anatudanganya tena. Tumwache.'\n\nHakuna aliyekuja kusaidia. Mbwa mwitu alikula kondoo wengi kabla ya kukimbia. Mvulana alilia sana, lakini ilikuwa kuchelewa.\n\nAlijifunza kwa uchungu: mwongo haaminiwi, hata anaposema ukweli.",
            story_type="moral",
            age_range="6-10",
            reading_time=5,
            language="sw",
            points_earned=15
        ),
        Story(
            title="Mti wa Ukarimu",
            content="Hapo zamani, kulikuwa na mti ambao ulimpenda mvulana mdogo. Kila siku mvulana alikuja kukusanya majani yake kutengeneza taji, kupanda shina lake, kuyumbayumba kwenye matawi yake, na kula matunda yake.\n\nMti ulifurahi. Lakini mvulana alipokua, hakuja mara nyingi. Siku moja alikuja na mti ukasema: 'Njoo ucheze nami!' Lakini mvulana akasema: 'Mimi si mdogo tena. Nataka pesa. Unaweza kunipa pesa?'\n\n'Pesa sina,' mti ukasema. 'Lakini chukua matunda yangu, uyauze sokoni, na utapata pesa.'\n\nMvulana alichukua matunda yote na kuondoka. Mti ulifurahi. Lakini mvulana hakurudi kwa muda mrefu. Aliporudi, alisema: 'Mimi ni mtu mzima sasa. Nahitaji nyumba. Unaweza kunipa nyumba?'\n\n'Kata matawi yangu ujenge nyumba,' mti ukasema. Mvulana akakata matawi yote na kuyachukua. Mti ulifurahi, lakini sio kweli.\n\nMiaka ikapita, mvulana alirudi, sasa ni mzee. 'Nimechoka,' alisema. 'Nahitaji mashua kusafiri.'\n\n'Kata shina langu ufanye mashua,' mti ukasema. Mvulana akakata shina. Sasa mti ulikuwa kigogo tu, na ulihuzunika.\n\nMiaka mingi ilipita. Mzee alirudi mara ya mwisho. 'Samahani,' alisema. 'Sina chochote cha kukupa tena.'\n\n'Sihitaji mengi,' mzee alisema. 'Nafasi tu ya kukaa.'\n\n'Nzuri!' mti ulisema, sasa ni kigogo tu. 'Kigogo ni mahali pazuri pa kukaa.'\n\nNa mzee aliketi. Na mti ulifurahi.",
            story_type="moral",
            age_range="8-12",
            reading_time=6,
            language="sw",
            points_earned=20
        ),

        # HADITHI ZA ELIMU (Educational Stories)
        Story(
            title="Safari ya Mbegu Ndogo",
            content="Hapo zamani, kulikuwa na mbegu ndogo iitwayo Sam. Sam aliishi katika tunda zuri la embe pamoja na ndugu zake. Lakini siku moja, ndege alikula embe hilo!\n\nSam alijisikia akienda chini, chini, chini ndani ya tumba la ndege. 'Hii inatisha!' aliwaza. Lakini hivi karibuni, ndege akaruka hadi mahali pengine na... plop! Sam akatoka katika sehemu mpya iliyojaa udongo.\n\n'Hujambo?' Sam aliita. 'Niko wapi?'\n\nDunia ikasema: 'Uko kwenye udongo, mbegu mdogo. Kunywa maji, jisikie jua, na utakua!'\n\nSam alikunywa maji ya mvua. Akajisikia joto la jua. Kitu cha ajabu kikatokea - gamba lake likapasuka!\n\nKwanza akatoka mzizi mdogo, ukienda chini gizani. 'Natafuta maji!' mzizi ukasema. Kisha akatoka mchipuko wa kijani, ukienda juu kutafuta mwanga. 'Natafuta jua!'\n\nSiku zikapita. Mchipuko ukawa shina. Majani yakatanda kama bendera ndogo za kijani. 'Tunakamata mwanga wa jua!' majani yalisema. 'Tunatengeneza chakula kwa mmea!'\n\nMiezi ikapita. Sam alikuwa mti mdogo sasa. Majani yake yalitengeneza chakula. Mizizi yake ilinywa maji. Alikua mrefu na hodari.\n\nMajira moja ya kuchipua, jambo la pekee lilitokea. Maua meupe yalitokea kote kwa Sam! Nyuki wakaja kutembelea, wakichukua poleni kutoka ua hadi ua.\n\nBaada ya maua kuanguka, matunda madogo ya kijani yalionekana. Yakakua na kukua. Yakaiva na kuwa mekundu. Yakawa maembe!\n\nNa ndani ya maembe hayo? Mbegu mpya, kama Sam. Tayari kuanza safari yao siku moja.",
            story_type="educational",
            age_range="7-11",
            reading_time=6,
            language="sw",
            points_earned=20,
            related_subject_id=3
        ),
        Story(
            title="Adventures ya Namba",
            content="Hapo zamani, katika Nchi ya Hesabu, waliishi namba 1, 2, 3, 4, na 5. Walikuwa marafiki wakubwa na walipenda kucheza pamoja.\n\nSiku moja, 1 akasema, 'Wacha tuunda namba kubwa zaidi!'\n\n'Vipi?' 2 akauliza.\n\n'Tazama!' 1 akasema. Akasimama karibu na 2. 'Sasa sisi ni 12!'\n\nLakini 3 akatikisa kichwa. 'Hiyo ni kuweka namba pamoja tu. Nionyeshe hesabu halisi!'\n\n3 alipata marafiki wawili nyuma ya mti. '1, 2, tokeni!' akawaita. Wawili wakatoka.\n\n'Sasa,' 3 akasema, 'tazama mwujiza huu: 3 pamoja na 1 pamoja na 1 ni sawa na... 5!'\n\nNamba zote zilishangilia! 'Tena, tena!'\n\nMara hii, 5 alitaka kujaribu. 'Nina tufaha 5,' akasema. 'Nikimpa 2 kwa 3, nitabakiwa na ngapi?'\n\n5 akafumba macho na kufikiri: '5 toa 2... ni sawa na 3!'\n\n'Sahihi!' wengine wakashangilia.\n\nKisha wakajaribu kuzidisha. 2 akamleta pacha wake. Sasa walikuwa na 2 mara mbili.\n\n'Mafungu mawili ya wawili,' 2 akasema. 'Hiyo ni 2 mara 2. Na jibu ni... 4!'\n\nNamba zikacheza kwa furaha. Siku hiyo walijifunza kwamba hesabu sio namba tu - ni mambo mazuri ambayo namba zinaweza kufanya wakifanya kazi pamoja!\n\nNa ukisikiliza kwa makini Nchi ya Hesabu, bado unaweza kusikia wakiimba: '1, 2, 3, 4, 5 - hesabu ni raha na hai!'",
            story_type="educational",
            age_range="6-10",
            reading_time=5,
            language="sw",
            points_earned=20,
            related_subject_id=1
        ),

        # HADITHI ZA MATUKIO (Adventure Stories)
        Story(
            title="Siri ya Pango la Siri",
            content="Maya na mbwa wake Rocky walikuwa wakichunguza ufukweni wakati wa likizo yao. Maji yalikuwa yamepwa, yakionyesha mawe na madimbwi ambayo hawajawahi kuona.\n\n'Tazama, Rocky!' Maya alinyesha kwenye sehemu nyeusi kati ya mawe mawili makubwa. 'Ni pango!'\n\nRocky alitingisha mkia na kunusa mwingilio. Maya akachukua tochi yake na kuingia ndani. Pango lilikuwa la baridi na likanuka kama chumvi na mwani.\n\nWalienda ndani zaidi. Ghafla, Rocky alianza kubweka. 'Ni nini, kijana?'\n\nPale, kwenye ukuta wa pango, kulikuwa na ujumbe ulioandikwa katika rangi iliyokuwa imechakaa: 'X inaashiria mahali ambapo hazina iko.'\n\nMoyo wa Maya uliruka kwa msisimko. Aliweka mwanga wake pande zote. Kulikuwa na X kubwa iliyochorwa chini! Yeye na Rocky wakachimba kwa mikono. Mchanga ukaruka kila mahali!\n\nKilichi! Mguu wa Rocky uligonga kitu kigumu. Wakachimba zaidi na kuvuta... sanduku la bati la zamani!\n\nMaya alilifungua kwa mikono inayotetemeka. Ndani yalikuwa makombe - mamia ya makombe mazuri ya bahari ya kila rangi! Pia kulikuwa na michoro kwenye mfuniko wa sanduku inayoonyesha pango na ufukwe wa zamani.\n\n'Mtu aliacha makombe haya kwa ajili ya watafiti wengine,' Maya alinong'ona. Alichukua konnmbi mmoja wa zambarau kwa ajili yake na kuwaacha wengine kwa ajili ya wagunduzi wengine.\n\nWaliporudi ufukweni, maji yalikuwa yanaingia. Mwingilio wa pango ulianza kutoweka chini ya mawimbi.\n\nMaya alitabasamu. Ilikuwa ni safari yao ya siri, na alikuwa na konnmbi wa zambarau kuthibitisha kuwa ilitokea kweli!",
            story_type="adventure",
            age_range="7-12",
            reading_time=6,
            language="sw",
            points_earned=20
        ),
        Story(
            title="Ramani ya Ajabu Darini",
            content="Sam alikuwa akimsaidia bibi yake kusafisha dari walipopata sanduku la mbao la zamani lililofunikwa na vumbi. Ndani yalikuwa ramani iliyokuwa imepauka yenye alama za ajabu na X kubwa nyekundu.\n\n'Bibi, hii ni nini?' Sam aliuliza.\n\nMacho ya bibi yakaangaza. 'Hiyo ni ramani ambayo babu yako alitengeneza akiwa na umri wako! Alisema kila wakati kuwa kuna siri kwenye mti wa mwaloni nyumbani.'\n\nSam alikimbilia nyuma ya nyumba akiwa na ramani. Mti wa mwaloni ulikuwa mkubwa sana, matawi yake yakifika angani. Alijifunza ramani - ilionyesha shimo kwenye tawi la tatu kutoka kushoto.\n\nSam alipanda kwa uangalifu. Tawi lililala lakini likabaki imara. Aliingiza mkono ndani ya shimo... na kuvuta kopo la bati lenye kutu!\n\nNdani yalikuwa daftari lililojaa mwandiko wa babu yake. 'Mtafuti mpendwa,' lilianza. 'Ikiwa unasoma hii, wewe ni mdadisi kama mimi!'\n\nDaftari lilijaa michoro ya ndege, wadudu, na mimea ambayo babu yake alikuwa ameiona nyuma ya nyumba. Katika ukurasa wa mwisho, lilisema: 'Hazina halisi ni udadisi. Endelea kuchunguza!'\n\nSam alitabasamu. Alichukua daftari lake mwenyewe na kuanza kuchora ndege aliowaona sasa hivi. Babu yake alikuwa sahihi - udadisi ni safari kubwa kuliko zote.",
            story_type="adventure",
            age_range="8-12",
            reading_time=6,
            language="sw",
            points_earned=20
        ),
    ]

    all_stories = stories + swahili_stories
    db.session.add_all(all_stories)
    db.session.commit()
    print("✅ Stories seeded successfully!")


def seed_cbc_data():
    """Seed CBC curriculum content (grades, topics, lessons)."""
    import seed_cbc as cbc

    print("🌱 Seeding CBC curriculum content...")

    # Always update subject categories for existing subjects
    subject_categories = {s['name']: s['category'] for s in cbc.SUBJECTS}
    for subj in Subject.query.all():
        try:
            if subj.name in subject_categories:
                current = getattr(subj, 'category', None)
                if current != subject_categories[subj.name]:
                    subj.category = subject_categories[subj.name]
        except Exception:
            pass
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()

    try:
        cbc.seed_grades(db, Grade)
        cbc.seed_subjects(db, Subject)
        if Topic.query.first():
            print("  CBC topics already exist, skipping content.")
        else:
            cbc.seed_cbc_content(db, Grade, Subject, Topic, Lesson)
            print("✅ CBC curriculum content seeded!")
        # Seed topic-linked quizzes (always run - checks for duplicates internally)
        from seed_topic_questions import seed_topic_questions
        seed_topic_questions()
    except Exception as e:
        print(f"  CBC seeding warning: {e}")
        db.session.rollback()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
