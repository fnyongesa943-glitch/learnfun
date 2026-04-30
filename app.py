"""
Kids Learning App - Main Application Entry Point
A fun, interactive educational platform for children aged 6-12.
"""
import os
from flask import Flask, session
from models import db
from config import Config


def create_app():
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Create database tables on first run
    with app.app_context():
        db.create_all()
        seed_data()

    # Register blueprints
    from blueprints.main import main_bp
    from blueprints.auth import auth_bp
    from blueprints.quiz import quiz_bp
    from blueprints.progress import progress_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    app.register_blueprint(progress_bp, url_prefix='/progress')

    # Make user available in all templates
    @app.context_processor
    def inject_user():
        """Inject current user into all templates."""
        user = None
        if 'user_id' in session:
            from models import User
            user = User.query.get(session['user_id'])
        return {'current_user': user}

    return app


def seed_data():
    """Seed the database with initial subjects, quizzes, and questions."""
    from models import Subject, Quiz, Question

    # Only seed if no subjects exist
    if Subject.query.first():
        return

    # Create subjects
    subjects = [
        Subject(name='Math', icon='🔢', color='#4F46E5', description='Learn numbers, addition, subtraction and more!'),
        Subject(name='Reading', icon='📚', color='#7C3AED', description='Improve your reading and vocabulary skills!'),
        Subject(name='Science', icon='🔬', color='#059669', description='Explore the amazing world of science!'),
    ]
    db.session.add_all(subjects)
    db.session.commit()

    # Math quizzes
    math_quizzes = [
        Quiz(title='Addition Fun', subject_id=1, difficulty='easy', description='Practice adding numbers together!'),
        Quiz(title='Subtraction Adventure', subject_id=1, difficulty='easy', description='Learn to subtract with fun problems!'),
        Quiz(title='Multiplication Magic', subject_id=1, difficulty='medium', description='Discover the magic of multiplication!'),
    ]
    db.session.add_all(math_quizzes)
    db.session.commit()

    # Math questions - Addition Fun
    addition_questions = [
        Question(quiz_id=1, text='What is 2 + 3?', option_a='4', option_b='5', option_c='6', option_d='7', correct_answer='B', explanation='2 + 3 = 5! Count on your fingers: 2 fingers plus 3 fingers = 5 fingers!', points=10),
        Question(quiz_id=1, text='What is 7 + 4?', option_a='10', option_b='11', option_c='12', option_d='9', correct_answer='B', explanation='7 + 4 = 11! Start at 7 and count up 4 more: 8, 9, 10, 11!', points=10),
        Question(quiz_id=1, text='What is 6 + 6?', option_a='10', option_b='11', option_c='12', option_d='14', correct_answer='C', explanation='6 + 6 = 12! When you add the same number twice, it is called doubling!', points=10),
        Question(quiz_id=1, text='What is 9 + 5?', option_a='13', option_b='14', option_c='15', option_d='12', correct_answer='B', explanation='9 + 5 = 14! Take 1 from 5 to make 10, then add the remaining 4!', points=10),
        Question(quiz_id=1, text='What is 8 + 7?', option_a='14', option_b='15', option_c='16', option_d='13', correct_answer='B', explanation='8 + 7 = 15! Start at 8 and count up 7 more!', points=10),
    ]

    # Math questions - Subtraction Adventure
    subtraction_questions = [
        Question(quiz_id=2, text='What is 8 - 3?', option_a='4', option_b='5', option_c='6', option_d='3', correct_answer='B', explanation='8 - 3 = 5! If you have 8 candies and eat 3, you have 5 left!', points=10),
        Question(quiz_id=2, text='What is 10 - 6?', option_a='3', option_b='5', option_c='4', option_d='6', correct_answer='C', explanation='10 - 6 = 4! Count backwards from 10: 9, 8, 7, 6, 5, 4!', points=10),
        Question(quiz_id=2, text='What is 15 - 7?', option_a='7', option_b='8', option_c='9', option_d='6', correct_answer='B', explanation='15 - 7 = 8! Think: 7 + 8 = 15, so 15 - 7 = 8!', points=10),
        Question(quiz_id=2, text='What is 12 - 5?', option_a='6', option_b='8', option_c='7', option_d='5', correct_answer='C', explanation='12 - 5 = 7! Start at 12 and count back 5!', points=10),
        Question(quiz_id=2, text='What is 20 - 9?', option_a='10', option_b='12', option_c='11', option_d='9', correct_answer='C', explanation='20 - 9 = 11! 20 minus 10 is 10, so minus 9 is one more = 11!', points=10),
    ]

    # Math questions - Multiplication Magic
    multiplication_questions = [
        Question(quiz_id=3, text='What is 3 x 4?', option_a='10', option_b='11', option_c='12', option_d='14', correct_answer='C', explanation='3 x 4 = 12! That means 3 groups of 4: 4 + 4 + 4 = 12!', points=15),
        Question(quiz_id=3, text='What is 5 x 2?', option_a='8', option_b='10', option_c='12', option_d='7', correct_answer='B', explanation='5 x 2 = 10! Two groups of 5: 5 + 5 = 10!', points=15),
        Question(quiz_id=3, text='What is 6 x 3?', option_a='16', option_b='18', option_c='20', option_d='15', correct_answer='B', explanation='6 x 3 = 18! Three groups of 6: 6 + 6 + 6 = 18!', points=15),
        Question(quiz_id=3, text='What is 4 x 4?', option_a='14', option_b='16', option_c='18', option_d='12', correct_answer='B', explanation='4 x 4 = 16! Four groups of 4: 4 + 4 + 4 + 4 = 16!', points=15),
        Question(quiz_id=3, text='What is 7 x 2?', option_a='12', option_b='16', option_c='14', option_d='15', correct_answer='C', explanation='7 x 2 = 14! Two groups of 7: 7 + 7 = 14!', points=15),
    ]

    # Reading quizzes
    reading_quizzes = [
        Quiz(title='Word Puzzles', subject_id=2, difficulty='easy', description='Can you find the right word?'),
        Quiz(title='Story Time', subject_id=2, difficulty='medium', description='Read short stories and answer questions!'),
        Quiz(title='Vocabulary Builder', subject_id=2, difficulty='medium', description='Learn new words and their meanings!'),
    ]
    db.session.add_all(reading_quizzes)
    db.session.commit()

    # Reading questions - Word Puzzles
    word_questions = [
        Question(quiz_id=4, text='Which word rhymes with "cat"?', option_a='dog', option_b='hat', option_c='sun', option_d='pen', correct_answer='B', explanation='"Hat" rhymes with "cat" because they both end with the "at" sound!', points=10),
        Question(quiz_id=4, text='What is the opposite of "hot"?', option_a='warm', option_b='big', option_c='cold', option_d='fast', correct_answer='C', explanation='"Cold" is the opposite of "hot". When something is not hot, it is cold!', points=10),
        Question(quiz_id=4, text='Which word starts with the letter "S"?', option_a='apple', option_b='ball', option_c='snake', option_d='dog', correct_answer='C', explanation='"Snake" starts with the letter S! S-n-a-k-e!', points=10),
        Question(quiz_id=4, text='Complete the sentence: "The sun is ____."', option_a='blue', option_b='bright', option_c='cold', option_d='soft', correct_answer='B', explanation='The sun is bright! It gives us light and warmth!', points=10),
        Question(quiz_id=4, text='Which word has 3 letters?', option_a='apple', option_b='sun', option_c='flower', option_d='butterfly', correct_answer='B', explanation='"Sun" has 3 letters: S-U-N!', points=10),
    ]

    # Reading questions - Story Time
    story_questions = [
        Question(quiz_id=5, text='Tom has a red ball. He throws it up. What color is the ball?', option_a='blue', option_b='green', option_c='red', option_d='yellow', correct_answer='C', explanation='The story says Tom has a "red" ball!', points=10),
        Question(quiz_id=5, text='Sara goes to the park. She swings on the swings. Where is Sara?', option_a='school', option_b='park', option_c='home', option_d='store', correct_answer='B', explanation='The story says Sara goes to the "park"!', points=10),
        Question(quiz_id=5, text='A bird sits in a tree. It sings a happy song. What does the bird do?', option_a='flies away', option_b='eats', option_c='sings', option_d='sleeps', correct_answer='C', explanation='The story says the bird "sings a happy song"!', points=10),
        Question(quiz_id=5, text='Max has 2 dogs and 1 cat. How many pets does Max have?', option_a='1', option_b='2', option_c='3', option_d='4', correct_answer='C', explanation='2 dogs + 1 cat = 3 pets total!', points=10),
        Question(quiz_id=5, text='It is raining. Lily opens her ___.', option_a='book', option_b='umbrella', option_c='toy', option_d='shoes', correct_answer='B', explanation='When it rains, you open an "umbrella" to stay dry!', points=10),
    ]

    # Reading questions - Vocabulary Builder
    vocab_questions = [
        Question(quiz_id=6, text='What does "enormous" mean?', option_a='very small', option_b='very big', option_c='very fast', option_d='very slow', correct_answer='B', explanation='"Enormous" means very big or huge! An elephant is enormous!', points=10),
        Question(quiz_id=6, text='What does "whisper" mean?', option_a='to shout loudly', option_b='to sing', option_c='to speak very softly', option_d='to laugh', correct_answer='C', explanation='To "whisper" means to speak very softly, like sharing a secret!', points=10),
        Question(quiz_id=6, text='Which word means the same as "happy"?', option_a='sad', option_b='angry', option_c='joyful', option_d='tired', correct_answer='C', explanation='"Joyful" means the same as "happy" - feeling good and smiling!', points=10),
        Question(quiz_id=6, text='What is a "habitat"?', option_a='a type of food', option_b='a place where animals live', option_c='a school subject', option_d='a game', correct_answer='B', explanation='A "habitat" is the natural home of an animal, like a forest for bears!', points=10),
        Question(quiz_id=6, text='What does "predict" mean?', option_a='to look back', option_b='to guess what will happen', option_c='to remember', option_d='to write', correct_answer='B', explanation='To "predict" means to make a smart guess about what will happen next!', points=10),
    ]

    # Science quizzes
    science_quizzes = [
        Quiz(title='Animal Kingdom', subject_id=3, difficulty='easy', description='Learn about amazing animals!'),
        Quiz(title='Weather Wonders', subject_id=3, difficulty='easy', description='Discover how weather works!'),
        Quiz(title='Space Explorer', subject_id=3, difficulty='medium', description='Blast off into space knowledge!'),
    ]
    db.session.add_all(science_quizzes)
    db.session.commit()

    # Science questions - Animal Kingdom
    animal_questions = [
        Question(quiz_id=7, text='Which animal is known as the King of the Jungle?', option_a='tiger', option_b='elephant', option_c='lion', option_d='bear', correct_answer='C', explanation='The lion is called the King of the Jungle because it is strong and brave!', points=10),
        Question(quiz_id=7, text='How many legs does a spider have?', option_a='6', option_b='8', option_c='10', option_d='4', correct_answer='B', explanation='Spiders have 8 legs! That is what makes them different from insects!', points=10),
        Question(quiz_id=7, text='Which animal can fly?', option_a='dog', option_b='fish', option_c='bird', option_d='cat', correct_answer='C', explanation='Birds have wings that let them fly through the sky!', points=10),
        Question(quiz_id=7, text='Where do fish live?', option_a='trees', option_b='water', option_c='sky', option_d='sand', correct_answer='B', explanation='Fish live in water - oceans, rivers, and lakes!', points=10),
        Question(quiz_id=7, text='Which animal gives us milk?', option_a='chicken', option_b='cow', option_c='dog', option_d='frog', correct_answer='B', explanation='Cows give us milk that we drink! Yummy!', points=10),
    ]

    # Science questions - Weather Wonders
    weather_questions = [
        Question(quiz_id=8, text='What falls from clouds when it is cold?', option_a='rain', option_b='sunshine', option_c='snow', option_d='wind', correct_answer='C', explanation='When it is very cold, water in clouds turns into snowflakes!', points=10),
        Question(quiz_id=8, text='What do you see in the sky after rain?', option_a='moon', option_b='stars', option_c='rainbow', option_d='clouds', correct_answer='C', explanation='A rainbow appears when sunlight shines through rain drops!', points=10),
        Question(quiz_id=8, text='Which season is the hottest?', option_a='winter', option_b='spring', option_c='summer', option_d='fall', correct_answer='C', explanation='Summer is the hottest season! That is why we go swimming!', points=10),
        Question(quiz_id=8, text='What gives us light during the day?', option_a='moon', option_b='stars', option_c='sun', option_d='lamp', correct_answer='C', explanation='The sun gives us light and warmth during the daytime!', points=10),
        Question(quiz_id=8, text='What makes wind blow?', option_a='trees', option_b='moving air', option_c='clouds', option_d='birds', correct_answer='B', explanation='Wind is just air that is moving from one place to another!', points=10),
    ]

    # Science questions - Space Explorer
    space_questions = [
        Question(quiz_id=9, text='What is the closest star to Earth?', option_a='Moon', option_b='Mars', option_c='Sun', option_d='Venus', correct_answer='C', explanation='The Sun is the closest star to Earth! It gives us light and heat!', points=15),
        Question(quiz_id=9, text='How many planets are in our solar system?', option_a='6', option_b='7', option_c='8', option_d='9', correct_answer='C', explanation='There are 8 planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune!', points=15),
        Question(quiz_id=9, text='Which planet do we live on?', option_a='Mars', option_b='Earth', option_c='Jupiter', option_d='Saturn', correct_answer='B', explanation='We live on Earth! It is the third planet from the Sun!', points=15),
        Question(quiz_id=9, text='What goes around the Earth?', option_a='Sun', option_b='Mars', option_c='Moon', option_d='Stars', correct_answer='C', explanation='The Moon goes around the Earth! It takes about 27 days for one trip!', points=15),
        Question(quiz_id=9, text='Which planet is known as the Red Planet?', option_a='Venus', option_b='Mars', option_c='Jupiter', option_d='Saturn', correct_answer='B', explanation='Mars is called the Red Planet because it looks red in the sky!', points=15),
    ]

    # Add all questions
    all_questions = (addition_questions + subtraction_questions + multiplication_questions +
                     word_questions + story_questions + vocab_questions +
                     animal_questions + weather_questions + space_questions)
    db.session.add_all(all_questions)
    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
