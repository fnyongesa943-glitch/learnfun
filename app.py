"""
Kids Learning App - Main Application Entry Point
Updated with new subjects, shop, and enhanced features.
"""
import os
from flask import Flask, session
from models import db, User, Subject, Quiz, Question, Score, UserBadge, ShopItem, UserOwnedItem
from config import Config


def create_app():
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        run_migrations()
        seed_data()

    from blueprints.main import main_bp
    from blueprints.auth import auth_bp
    from blueprints.quiz import quiz_bp
    from blueprints.progress import progress_bp
    from blueprints.shop import shop_bp
    from blueprints.parent import parent_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    app.register_blueprint(progress_bp, url_prefix='/progress')
    app.register_blueprint(shop_bp, url_prefix='/shop')
    app.register_blueprint(parent_bp, url_prefix='/parent')

    @app.context_processor
    def inject_user():
        user = None
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
        return {'current_user': user}

    return app


def run_migrations():
    """Add missing columns to existing SQLite tables safely."""
    from sqlalchemy import inspect, text
    inspector = inspect(db.engine)
    
    # Check User table
    if 'users' in inspector.get_table_names():
        cols = {c['name']: c for c in inspector.get_columns('users')}
        
        if 'avatar_frame' not in cols:
            db.session.execute(text('ALTER TABLE users ADD COLUMN avatar_frame VARCHAR(20) DEFAULT "none"'))
        if 'coins' not in cols:
            db.session.execute(text('ALTER TABLE users ADD COLUMN coins INTEGER DEFAULT 0'))
        if 'streak_days' not in cols:
            db.session.execute(text('ALTER TABLE users ADD COLUMN streak_days INTEGER DEFAULT 0'))
        if 'last_active' not in cols:
            db.session.execute(text('ALTER TABLE users ADD COLUMN last_active DATETIME'))
        if 'parent_pin' not in cols:
            db.session.execute(text('ALTER TABLE users ADD COLUMN parent_pin VARCHAR(4) DEFAULT "0000"'))

    # Check questions table
    if 'questions' in inspector.get_table_names():
        cols = {c['name']: c for c in inspector.get_columns('questions')}
        if 'hint' not in cols:
            db.session.execute(text('ALTER TABLE questions ADD COLUMN hint VARCHAR(200) DEFAULT ""'))

    # Create new tables if they don't exist
    if 'shop_items' not in inspector.get_table_names():
        db.create_all()
    if 'user_owned_items' not in inspector.get_table_names():
        db.create_all()

    db.session.commit()


def seed_data():
    """Seed database with subjects, quizzes, shop items, and questions."""
    if Subject.query.first():
        return

    # 1. Subjects
    subjects = [
        Subject(name='Math', icon='🔢', color='#4F46E5', description='Addition, subtraction, multiplication!'),
        Subject(name='Reading', icon='📚', color='#7C3AED', description='Word puzzles and stories!'),
        Subject(name='Science', icon='🔬', color='#059669', description='Animals, weather, and space!'),
        Subject(name='Geography', icon='🌍', color='#D97706', description='Countries, maps, and landmarks!'),
        Subject(name='Art', icon='🎨', color='#EC4899', description='Colors, shapes, and famous artists!'),
        Subject(name='Coding', icon='💻', color='#3B82F6', description='Logic puzzles and algorithms!'),
        Subject(name='Music', icon='🎵', color='#8B5CF6', description='Instruments and rhythms!'),
    ]
    db.session.add_all(subjects)
    db.session.commit()

    # 2. Shop Items
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

    # Helper to add questions
    def add_questions(quiz_id, qs):
        db.session.add_all(qs)
        db.session.commit()

    # --- MATH QUIZZES ---
    m1 = Quiz(title='Addition Fun', subject_id=1, difficulty='easy', description='Practice adding numbers!')
    m2 = Quiz(title='Subtraction Pro', subject_id=1, difficulty='easy', description='Subtract with ease!')
    m3 = Quiz(title='Multiplication Magic', subject_id=1, difficulty='medium', description='Multiply and conquer!')
    db.session.add_all([m1, m2, m3])
    db.session.commit()

    q1 = [
        Question(quiz_id=m1.id, text='2 + 3 = ?', option_a='4', option_b='5', option_c='6', option_d='7', correct_answer='B', explanation='2 + 3 = 5!', hint='Count on your fingers: 2 and then 3 more.', points=10),
        Question(quiz_id=m1.id, text='7 + 4 = ?', option_a='10', option_b='11', option_c='12', option_d='9', correct_answer='B', explanation='7 + 4 = 11!', hint='Start at 7 and count up 4 more.', points=10),
        Question(quiz_id=m1.id, text='6 + 6 = ?', option_a='10', option_b='11', option_c='12', option_d='14', correct_answer='C', explanation='6 + 6 = 12!', hint='Double 6!', points=10),
        Question(quiz_id=m1.id, text='9 + 5 = ?', option_a='13', option_b='14', option_c='15', option_d='12', correct_answer='B', explanation='9 + 5 = 14!', hint='Take 1 from 5 to make 10, then add 4.', points=10),
        Question(quiz_id=m1.id, text='8 + 7 = ?', option_a='14', option_b='15', option_c='16', option_d='13', correct_answer='B', explanation='8 + 7 = 15!', hint='Start at 8 and count up 7.', points=10),
    ]
    add_questions(m1.id, q1)

    q2 = [
        Question(quiz_id=m2.id, text='8 - 3 = ?', option_a='4', option_b='5', option_c='6', option_d='3', correct_answer='B', explanation='8 - 3 = 5!', hint='If you have 8 candies and eat 3...', points=10),
        Question(quiz_id=m2.id, text='10 - 6 = ?', option_a='3', option_b='5', option_c='4', option_d='6', correct_answer='C', explanation='10 - 6 = 4!', hint='Count backwards from 10.', points=10),
        Question(quiz_id=m2.id, text='15 - 7 = ?', option_a='7', option_b='8', option_c='9', option_d='6', correct_answer='B', explanation='15 - 7 = 8!', hint='7 + 8 = 15, so 15 - 7 = ?', points=10),
        Question(quiz_id=m2.id, text='12 - 5 = ?', option_a='6', option_b='8', option_c='7', option_d='5', correct_answer='C', explanation='12 - 5 = 7!', hint='Start at 12 and count back 5.', points=10),
        Question(quiz_id=m2.id, text='20 - 9 = ?', option_a='10', option_b='12', option_c='11', option_d='9', correct_answer='C', explanation='20 - 9 = 11!', hint='20 - 10 is 10, so 20 - 9 is one more.', points=10),
    ]
    add_questions(m2.id, q2)

    q3 = [
        Question(quiz_id=m3.id, text='3 x 4 = ?', option_a='10', option_b='11', option_c='12', option_d='14', correct_answer='C', explanation='3 x 4 = 12!', hint='3 groups of 4.', points=15),
        Question(quiz_id=m3.id, text='5 x 2 = ?', option_a='8', option_b='10', option_c='12', option_d='7', correct_answer='B', explanation='5 x 2 = 10!', hint='Two groups of 5.', points=15),
        Question(quiz_id=m3.id, text='6 x 3 = ?', option_a='16', option_b='18', option_c='20', option_d='15', correct_answer='B', explanation='6 x 3 = 18!', hint='6 + 6 + 6 = ?', points=15),
        Question(quiz_id=m3.id, text='4 x 4 = ?', option_a='14', option_b='16', option_c='18', option_d='12', correct_answer='B', explanation='4 x 4 = 16!', hint='Four groups of 4.', points=15),
        Question(quiz_id=m3.id, text='7 x 2 = ?', option_a='12', option_b='16', option_c='14', option_d='15', correct_answer='C', explanation='7 x 2 = 14!', hint='7 + 7 = ?', points=15),
    ]
    add_questions(m3.id, q3)

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
    add_questions(r1.id, qr1)

    qr2 = [
        Question(quiz_id=r2.id, text='Tom has a red ball. Color?', option_a='blue', option_b='green', option_c='red', option_d='yellow', correct_answer='C', explanation='It says "red ball"!', hint='Check the story.', points=10),
        Question(quiz_id=r2.id, text='Sara goes to park. Where?', option_a='school', option_b='park', option_c='home', option_d='store', correct_answer='B', explanation='Park!', hint='Look at the text.', points=10),
        Question(quiz_id=r2.id, text='Bird in tree. What does it do?', option_a='flies', option_b='eats', option_c='sings', option_d='sleeps', correct_answer='C', explanation='Sings!', hint='Happy song.', points=10),
        Question(quiz_id=r2.id, text='Max has 2 dogs, 1 cat. Pets?', option_a='1', option_b='2', option_c='3', option_d='4', correct_answer='C', explanation='2+1=3 pets.', hint='Add them up.', points=10),
        Question(quiz_id=r2.id, text='Raining. Lily opens ___', option_a='book', option_b='umbrella', option_c='toy', option_d='shoes', correct_answer='B', explanation='Umbrella!', hint='Keeps dry.', points=10),
    ]
    add_questions(r2.id, qr2)

    qr3 = [
        Question(quiz_id=r3.id, text='"Enormous" means?', option_a='small', option_b='big', option_c='fast', option_d='slow', correct_answer='B', explanation='Huge!', hint='Like an elephant.', points=10),
        Question(quiz_id=r3.id, text='"Whisper" means?', option_a='shout', option_b='sing', option_c='speak soft', option_d='laugh', correct_answer='C', explanation='Speak very softly.', hint='Like a secret.', points=10),
        Question(quiz_id=r3.id, text='Same as "happy"?', option_a='sad', option_b='angry', option_c='joyful', option_d='tired', correct_answer='C', explanation='Joyful!', hint='Smiling.', points=10),
        Question(quiz_id=r3.id, text='"Habitat" is?', option_a='food', option_b='home', option_c='school', option_d='game', correct_answer='B', explanation='Where animals live.', hint='Bear lives in forest.', points=10),
        Question(quiz_id=r3.id, text='"Predict" means?', option_a='look back', option_b='guess future', option_c='remember', option_d='write', correct_answer='B', explanation='Guess what will happen.', hint='Before it happens.', points=10),
    ]
    add_questions(r3.id, qr3)

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
    add_questions(s1.id, qs1)

    qs2 = [
        Question(quiz_id=s2.id, text='Cold sky falls as?', option_a='rain', option_b='sun', option_c='snow', option_d='wind', correct_answer='C', explanation='Snow!', hint='Winter flakes.', points=10),
        Question(quiz_id=s2.id, text='After rain you see?', option_a='moon', option_b='stars', option_c='rainbow', option_d='clouds', correct_answer='C', explanation='Rainbow!', hint='Colorful arc.', points=10),
        Question(quiz_id=s2.id, text='Hottest season?', option_a='winter', option_b='spring', option_c='summer', option_d='fall', correct_answer='C', explanation='Summer!', hint='Swimming time.', points=10),
        Question(quiz_id=s2.id, text='Day light from?', option_a='moon', option_b='stars', option_c='sun', option_d='lamp', correct_answer='C', explanation='Sun!', hint='Shines bright.', points=10),
        Question(quiz_id=s2.id, text='Wind is?', option_a='trees', option_b='moving air', option_c='clouds', option_d='birds', correct_answer='B', explanation='Moving air!', hint='Invisible push.', points=10),
    ]
    add_questions(s2.id, qs2)

    qs3 = [
        Question(quiz_id=s3.id, text='Closest star?', option_a='Moon', option_b='Mars', option_c='Sun', option_d='Venus', correct_answer='C', explanation='Sun!', hint='In the sky.', points=15),
        Question(quiz_id=s3.id, text='Planets in solar system?', option_a='6', option_b='7', option_c='8', option_d='9', correct_answer='C', explanation='8!', hint='Mercury to Neptune.', points=15),
        Question(quiz_id=s3.id, text='We live on?', option_a='Mars', option_b='Earth', option_c='Jupiter', option_d='Saturn', correct_answer='B', explanation='Earth!', hint='Home.', points=15),
        Question(quiz_id=s3.id, text='Goes around Earth?', option_a='Sun', option_b='Mars', option_c='Moon', option_d='Stars', correct_answer='C', explanation='Moon!', hint='Night light.', points=15),
        Question(quiz_id=s3.id, text='Red Planet?', option_a='Venus', option_b='Mars', option_c='Jupiter', option_d='Saturn', correct_answer='B', explanation='Mars!', hint='Looks red.', points=15),
    ]
    add_questions(s3.id, qs3)

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
    add_questions(g1.id, qg1)

    qg2 = [
        Question(quiz_id=g2.id, text='Largest ocean?', option_a='Atlantic', option_b='Pacific', option_c='Indian', option_d='Arctic', correct_answer='B', explanation='Pacific!', hint='Peaceful.', points=10),
        Question(quiz_id=g2.id, text='Longest river?', option_a='Amazon', option_b='Nile', option_c='Mississippi', option_d='Yangtze', correct_answer='B', explanation='Nile!', hint='In Africa.', points=10),
        Question(quiz_id=g2.id, text='How many oceans?', option_a='3', option_b='4', option_c='5', option_d='6', correct_answer='C', explanation='5!', hint='Atlantic, Pacific, Indian, Arctic, Southern.', points=10),
        Question(quiz_id=g2.id, text='Salt water or fresh?', option_a='Salt', option_b='Fresh', option_c='Sweet', option_d='Sour', correct_answer='A', explanation='Salt!', hint='Sea.', points=10),
        Question(quiz_id=g2.id, text='Where rivers end?', option_a='Mountain', option_b='Sea', option_c='Sky', option_d='Forest', correct_answer='B', explanation='Sea!', hint='Ocean.', points=10),
    ]
    add_questions(g2.id, qg2)

    qg3 = [
        Question(quiz_id=g3.id, text='Great Wall is in?', option_a='India', option_b='China', option_c='Japan', option_d='Russia', correct_answer='B', explanation='China!', hint='Long wall.', points=15),
        Question(quiz_id=g3.id, text='Pyramids are in?', option_a='Mexico', option_b='Egypt', option_c='Peru', option_d='Greece', correct_answer='B', explanation='Egypt!', hint='Pharaohs.', points=15),
        Question(quiz_id=g3.id, text='Eiffel Tower city?', option_a='London', option_b='Paris', option_c='Rome', option_d='Berlin', correct_answer='B', explanation='Paris!', hint='France.', points=15),
        Question(quiz_id=g3.id, text='Taj Mahal is?', option_a='Palace', option_b='Tomb', option_c='School', option_d='Mall', correct_answer='B', explanation='A tomb!', hint='In India.', points=15),
        Question(quiz_id=g3.id, text='Statue of Liberty is?', option_a='USA', option_b='UK', option_c='France', option_d='Italy', correct_answer='A', explanation='USA!', hint='New York.', points=15),
    ]
    add_questions(g3.id, qg3)

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
    add_questions(a1.id, qa1)

    qa2 = [
        Question(quiz_id=a2.id, text='Mona Lisa painter?', option_a='Van Gogh', option_b='Da Vinci', option_c='Picasso', option_d='Monet', correct_answer='B', explanation='Leonardo da Vinci!', hint='Also inventor.', points=15),
        Question(quiz_id=a2.id, text='Sunflowers painter?', option_a='Van Gogh', option_b='Da Vinci', option_c='Picasso', option_d='Monet', correct_answer='A', explanation='Van Gogh!', hint='Yellow flowers.', points=15),
        Question(quiz_id=a2.id, text='Starry Night is?', option_a='Painting', option_b='Song', option_c='Book', option_d='Movie', correct_answer='A', explanation='Painting!', hint='Night sky swirls.', points=15),
        Question(quiz_id=a2.id, text='Sculpture is?', option_a='Drawing', option_b='Carving', option_c='Photo', option_d='Music', correct_answer='B', explanation='Carving!', hint='3D art.', points=15),
        Question(quiz_id=a2.id, text='Canvas is for?', option_a='Painting', option_b='Singing', option_c='Dancing', option_d='Running', correct_answer='A', explanation='Painting!', hint='Holds paint.', points=15),
    ]
    add_questions(a2.id, qa2)

    qa3 = [
        Question(quiz_id=a3.id, text='String instrument?', option_a='Drum', option_b='Violin', option_c='Flute', option_d='Trumpet', correct_answer='B', explanation='Violin!', hint='4 strings, bow.', points=15),
        Question(quiz_id=a3.id, text='Piano has?', option_a='Keys', option_b='Strings', option_c='Sticks', option_d='Horns', correct_answer='A', explanation='Keys!', hint='Black and white.', points=15),
        Question(quiz_id=a3.id, text='Trumpet family?', option_a='Woodwind', option_b='Brass', option_c='String', option_d='Percussion', correct_answer='B', explanation='Brass!', hint='Shiny metal.', points=15),
        Question(quiz_id=a3.id, text='Drums are?', option_a='String', option_b='Wind', option_c='Percussion', option_d='Brass', correct_answer='C', explanation='Percussion!', hint='Hit them.', points=15),
        Question(quiz_id=a3.id, text='Flute is?', option_a='Woodwind', option_b='Brass', option_c='String', option_d='Percussion', correct_answer='A', explanation='Woodwind!', hint='Blow across.', points=15),
    ]
    add_questions(a3.id, qa3)

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
    add_questions(c1.id, qc1)

    qc2 = [
        Question(quiz_id=c2.id, text='Algorithm is?', option_a='Steps', option_b='Food', option_c='Game', option_d='Song', correct_answer='A', explanation='Steps!', hint='Recipe for code.', points=15),
        Question(quiz_id=c2.id, text='IF statement?', option_a='Choice', option_b='Loop', option_c='Number', option_d='Word', correct_answer='A', explanation='Choice!', hint='If this, then that.', points=15),
        Question(quiz_id=c2.id, text='Variable stores?', option_a='Power', option_b='Data', option_c='Music', option_d='Air', correct_answer='B', explanation='Data!', hint='Like a box.', points=15),
        Question(quiz_id=c2.id, text='Debug means?', option_a='Create', option_b='Delete', option_c='Fix', option_d='Run', correct_answer='C', explanation='Fix!', hint='Remove bugs.', points=15),
        Question(quiz_id=c2.id, text='Start of program?', option_a='End', option_b='Start', option_c='Middle', option_d='Loop', correct_answer='B', explanation='Start!', hint='Beginning.', points=15),
    ]
    add_questions(c2.id, qc2)

    qc3 = [
        Question(quiz_id=c3.id, text='Binary uses?', option_a='1-10', option_b='A-Z', option_c='0-1', option_d='!@#', correct_answer='C', explanation='0 and 1!', hint='Yes/No.', points=15),
        Question(quiz_id=c3.id, text='10 in binary?', option_a='10', option_b='1010', option_c='11', option_d='111', correct_answer='B', explanation='1010!', hint='8+2.', points=15),
        Question(quiz_id=c3.id, text='Bit means?', option_a='Binary Digit', option_b='Big Byte', option_c='Base Item', option_d='Byte', correct_answer='A', explanation='Binary Digit!', hint='Smallest unit.', points=15),
        Question(quiz_id=c3.id, text='Byte has bits?', option_a='4', option_b='8', option_c='16', option_d='32', correct_answer='B', explanation='8 bits!', hint='Half dozen + 2.', points=15),
        Question(quiz_id=c3.id, text='1111 in decimal?', option_a='10', option_b='12', option_c='15', option_d='14', correct_answer='C', explanation='15!', hint='8+4+2+1.', points=15),
    ]
    add_questions(c3.id, qc3)

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
    add_questions(u1.id, qu1)

    qu2 = [
        Question(quiz_id=u2.id, text='Guitar strings?', option_a='4', option_b='5', option_c='6', option_d='7', correct_answer='C', explanation='6!', hint='Standard guitar.', points=10),
        Question(quiz_id=u2.id, text='Violin played with?', option_a='Hands', option_b='Bow', option_c='Stick', option_d='Blow', correct_answer='B', explanation='Bow!', hint='Hair and wood.', points=10),
        Question(quiz_id=u2.id, text='Piano keys?', option_a='66', option_b='88', option_c='100', option_d='50', correct_answer='B', explanation='88!', hint='Black and white.', points=10),
        Question(quiz_id=u2.id, text='Saxophone is?', option_a='Woodwind', option_b='Brass', option_c='String', option_d='Percussion', correct_answer='A', explanation='Woodwind!', hint='Uses reed.', points=10),
        Question(quiz_id=u2.id, text='Cymbals family?', option_a='String', option_b='Percussion', option_c='Brass', option_d='Woodwind', correct_answer='B', explanation='Percussion!', hint='Clash them.', points=10),
    ]
    add_questions(u2.id, qu2)

    qu3 = [
        Question(quiz_id=u3.id, text='Beethoven was?', option_a='Singer', option_b='Composer', option_c='Dancer', option_d='Painter', correct_answer='B', explanation='Composer!', hint='Classical music.', points=15),
        Question(quiz_id=u3.id, text='Twinkle Twinkle is?', option_a='Lullaby', option_b='Rock', option_c='Rap', option_d='Jazz', correct_answer='A', explanation='Lullaby!', hint='For sleeping.', points=15),
        Question(quiz_id=u3.id, text='Mozart wrote?', option_a='Songs', option_b='Symphonies', option_c='Poems', option_d='Stories', correct_answer='B', explanation='Symphonies!', hint='Orchestras.', points=15),
        Question(quiz_id=u3.id, text='National Anthem?', option_a='Lullaby', option_b='Patriotic', option_c='Dance', option_d='Pop', correct_answer='B', explanation='Patriotic!', hint='Country song.', points=15),
        Question(quiz_id=u3.id, text='Happy Birthday is?', option_a='Rock', option_b='Celebration', option_c='Sad', option_d='Fast', correct_answer='B', explanation='Celebration!', hint='Cakes.', points=15),
    ]
    add_questions(u3.id, qu3)

    print("✅ Database seeded successfully!")


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
