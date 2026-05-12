from models import Subject, Quiz, Question, db


def seed_more_questions():
    """Add more questions to every subject (20-100 per subject)."""

    subject_map = {s.name: s for s in Subject.query.all()}
    if not subject_map:
        print("  No subjects found, skipping question seeding.")
        return

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

    def add_questions_if_missing(quiz, qs):
        if not quiz or Question.query.filter_by(quiz_id=quiz.id).first():
            return
        db.session.add_all(qs)
        db.session.commit()

    # ========================
    # MATH - additional 60 questions
    # ========================
    m9 = add_quiz_if_missing('Addition Challenge', 'Math', 'easy', 'More addition fun!')
    if m9:
        add_questions_if_missing(m9, [
            Question(quiz_id=m9.id, text='12 + 8 = ?', option_a='18', option_b='20', option_c='22', option_d='16', correct_answer='B', explanation='12 + 8 = 20!', hint='10 + 10 = 20.', points=10),
            Question(quiz_id=m9.id, text='15 + 7 = ?', option_a='21', option_b='23', option_c='22', option_d='20', correct_answer='C', explanation='15 + 7 = 22!', hint='15 + 5 = 20, plus 2 more.', points=10),
            Question(quiz_id=m9.id, text='24 + 6 = ?', option_a='28', option_b='32', option_c='30', option_d='26', correct_answer='C', explanation='24 + 6 = 30!', hint='It makes a round number.', points=10),
            Question(quiz_id=m9.id, text='33 + 9 = ?', option_a='40', option_b='41', option_c='43', option_d='42', correct_answer='D', explanation='33 + 9 = 42!', hint='33 + 7 = 40, plus 2.', points=10),
            Question(quiz_id=m9.id, text='18 + 14 = ?', option_a='30', option_b='32', option_c='34', option_d='28', correct_answer='B', explanation='18 + 14 = 32!', hint='18 + 10 = 28, plus 4.', points=10),
            Question(quiz_id=m9.id, text='27 + 15 = ?', option_a='42', option_b='44', option_c='40', option_d='38', correct_answer='A', explanation='27 + 15 = 42!', hint='27 + 10 = 37, plus 5.', points=10),
            Question(quiz_id=m9.id, text='45 + 18 = ?', option_a='65', option_b='61', option_c='63', option_d='59', correct_answer='C', explanation='45 + 18 = 63!', hint='45 + 20 = 65, minus 2.', points=10),
        ])

    m10 = add_quiz_if_missing('Subtraction Skills', 'Math', 'easy', 'Sharpen subtraction!')
    if m10:
        add_questions_if_missing(m10, [
            Question(quiz_id=m10.id, text='14 - 6 = ?', option_a='6', option_b='7', option_c='8', option_d='9', correct_answer='C', explanation='14 - 6 = 8!', hint='Count back from 14.', points=10),
            Question(quiz_id=m10.id, text='25 - 8 = ?', option_a='15', option_b='16', option_c='18', option_d='17', correct_answer='D', explanation='25 - 8 = 17!', hint='25 - 5 = 20, minus 3 more.', points=10),
            Question(quiz_id=m10.id, text='30 - 12 = ?', option_a='16', option_b='20', option_c='18', option_d='14', correct_answer='C', explanation='30 - 12 = 18!', hint='30 - 10 = 20, minus 2.', points=10),
            Question(quiz_id=m10.id, text='40 - 15 = ?', option_a='25', option_b='20', option_c='30', option_d='35', correct_answer='A', explanation='40 - 15 = 25!', hint='40 - 10 = 30, minus 5.', points=10),
            Question(quiz_id=m10.id, text='50 - 22 = ?', option_a='26', option_b='30', option_c='28', option_d='32', correct_answer='C', explanation='50 - 22 = 28!', hint='50 - 20 = 30, minus 2.', points=10),
            Question(quiz_id=m10.id, text='36 - 19 = ?', option_a='15', option_b='19', option_c='17', option_d='13', correct_answer='C', explanation='36 - 19 = 17!', hint='36 - 20 = 16, plus 1.', points=10),
            Question(quiz_id=m10.id, text='60 - 25 = ?', option_a='30', option_b='35', option_c='40', option_d='45', correct_answer='B', explanation='60 - 25 = 35!', hint='60 - 20 = 40, minus 5.', points=10),
        ])

    m11 = add_quiz_if_missing('Multiplication Practice', 'Math', 'medium', 'Times tables!')
    if m11:
        add_questions_if_missing(m11, [
            Question(quiz_id=m11.id, text='6 x 7 = ?', option_a='40', option_b='42', option_c='44', option_d='36', correct_answer='B', explanation='6 x 7 = 42!', hint='6 groups of 7.', points=15),
            Question(quiz_id=m11.id, text='8 x 9 = ?', option_a='64', option_b='72', option_c='81', option_d='63', correct_answer='B', explanation='8 x 9 = 72!', hint='9 groups of 8.', points=15),
            Question(quiz_id=m11.id, text='7 x 5 = ?', option_a='30', option_b='40', option_c='35', option_d='42', correct_answer='C', explanation='7 x 5 = 35!', hint='7 groups of 5.', points=15),
            Question(quiz_id=m11.id, text='9 x 3 = ?', option_a='18', option_b='21', option_c='24', option_d='27', correct_answer='D', explanation='9 x 3 = 27!', hint='9 + 9 + 9 = ?', points=15),
            Question(quiz_id=m11.id, text='4 x 8 = ?', option_a='28', option_b='30', option_c='32', option_d='36', correct_answer='C', explanation='4 x 8 = 32!', hint='4 groups of 8.', points=15),
            Question(quiz_id=m11.id, text='11 x 3 = ?', option_a='30', option_b='31', option_c='33', option_d='36', correct_answer='C', explanation='11 x 3 = 33!', hint='11 + 11 + 11 = ?', points=15),
            Question(quiz_id=m11.id, text='12 x 2 = ?', option_a='20', option_b='22', option_c='24', option_d='26', correct_answer='C', explanation='12 x 2 = 24!', hint='12 + 12 = ?', points=15),
        ])

    m12 = add_quiz_if_missing('Division Practice', 'Math', 'medium', 'Divide and conquer!')
    if m12:
        add_questions_if_missing(m12, [
            Question(quiz_id=m12.id, text='24 ÷ 4 = ?', option_a='4', option_b='6', option_c='8', option_d='5', correct_answer='B', explanation='24 ÷ 4 = 6!', hint='4 x 6 = 24.', points=15),
            Question(quiz_id=m12.id, text='30 ÷ 5 = ?', option_a='5', option_b='7', option_c='6', option_d='4', correct_answer='C', explanation='30 ÷ 5 = 6!', hint='5 x 6 = 30.', points=15),
            Question(quiz_id=m12.id, text='18 ÷ 2 = ?', option_a='7', option_b='8', option_c='9', option_d='10', correct_answer='C', explanation='18 ÷ 2 = 9!', hint='2 x 9 = 18.', points=15),
            Question(quiz_id=m12.id, text='28 ÷ 7 = ?', option_a='3', option_b='5', option_c='4', option_d='6', correct_answer='C', explanation='28 ÷ 7 = 4!', hint='7 x 4 = 28.', points=15),
            Question(quiz_id=m12.id, text='42 ÷ 6 = ?', option_a='6', option_b='8', option_c='7', option_d='5', correct_answer='C', explanation='42 ÷ 6 = 7!', hint='6 x 7 = 42.', points=15),
            Question(quiz_id=m12.id, text='56 ÷ 8 = ?', option_a='6', option_b='7', option_c='8', option_d='9', correct_answer='B', explanation='56 ÷ 8 = 7!', hint='8 x 7 = 56.', points=15),
            Question(quiz_id=m12.id, text='81 ÷ 9 = ?', option_a='7', option_b='8', option_c='9', option_d='10', correct_answer='C', explanation='81 ÷ 9 = 9!', hint='9 x 9 = 81.', points=15),
        ])

    m13 = add_quiz_if_missing('Fractions & Decimals', 'Math', 'hard', 'Advanced fractions!')
    if m13:
        add_questions_if_missing(m13, [
            Question(quiz_id=m13.id, text='1/2 of 20 = ?', option_a='5', option_b='10', option_c='15', option_d='12', correct_answer='B', explanation='Half of 20 is 10!', hint='20 split into 2 equal parts.', points=20),
            Question(quiz_id=m13.id, text='3/4 of 16 = ?', option_a='8', option_b='10', option_c='12', option_d='14', correct_answer='C', explanation='3/4 of 16 = 12!', hint='1/4 of 16 = 4, times 3.', points=20),
            Question(quiz_id=m13.id, text='0.5 as fraction is?', option_a='1/4', option_b='1/3', option_c='1/2', option_d='2/3', correct_answer='C', explanation='0.5 = 1/2!', hint='Half.', points=20),
            Question(quiz_id=m13.id, text='1/10 + 3/10 = ?', option_a='2/5', option_b='3/10', option_c='4/5', option_d='4/10', correct_answer='D', explanation='1/10 + 3/10 = 4/10!', hint='Add the top numbers.', points=20),
            Question(quiz_id=m13.id, text='Which is bigger: 0.75 or 0.5?', option_a='0.75', option_b='0.5', option_c='Same', option_d='Neither', correct_answer='A', explanation='0.75 is bigger than 0.5!', hint='75 cents vs 50 cents.', points=20),
            Question(quiz_id=m13.id, text='2/5 of 25 = ?', option_a='8', option_b='10', option_c='12', option_d='15', correct_answer='B', explanation='2/5 of 25 = 10!', hint='1/5 of 25 = 5, times 2.', points=20),
            Question(quiz_id=m13.id, text='0.25 as fraction is?', option_a='1/2', option_b='1/5', option_c='1/4', option_d='1/3', correct_answer='C', explanation='0.25 = 1/4!', hint='A quarter.', points=20),
        ])

    m14 = add_quiz_if_missing('Word Problems', 'Math', 'hard', 'Real-world math!')
    if m14:
        add_questions_if_missing(m14, [
            Question(quiz_id=m14.id, text='Sarah has 15 apples. She gives 7 to Tom. How many left?', option_a='6', option_b='7', option_c='8', option_d='9', correct_answer='C', explanation='15 - 7 = 8 apples left!', hint='Subtract 7 from 15.', points=20),
            Question(quiz_id=m14.id, text='There are 4 rows of chairs. Each row has 6 chairs. Total chairs?', option_a='20', option_b='22', option_c='24', option_d='26', correct_answer='C', explanation='4 x 6 = 24 chairs!', hint='Multiply rows by chairs per row.', points=20),
            Question(quiz_id=m14.id, text='Mom bakes 24 cookies. She puts them on 3 plates equally. Cookies per plate?', option_a='6', option_b='7', option_c='8', option_d='9', correct_answer='C', explanation='24 ÷ 3 = 8 cookies per plate!', hint='Divide cookies by plates.', points=20),
            Question(quiz_id=m14.id, text='John has 3 packs of markers. Each pack has 8 markers. Total markers?', option_a='20', option_b='22', option_c='24', option_d='26', correct_answer='C', explanation='3 x 8 = 24 markers!', hint='Multiply packs by markers per pack.', points=20),
            Question(quiz_id=m14.id, text='Emma reads 12 pages on Monday and 15 on Tuesday. Total pages?', option_a='25', option_b='27', option_c='28', option_d='30', correct_answer='B', explanation='12 + 15 = 27 pages!', hint='Add Monday and Tuesday.', points=20),
            Question(quiz_id=m14.id, text='A pizza has 8 slices. 4 friends share equally. Slices per friend?', option_a='1', option_b='2', option_c='3', option_d='4', correct_answer='B', explanation='8 ÷ 4 = 2 slices each!', hint='Divide slices by friends.', points=20),
            Question(quiz_id=m14.id, text='Tom is 5 years old. His sister is twice his age. How old is sister?', option_a='8', option_b='9', option_c='10', option_d='12', correct_answer='C', explanation='5 x 2 = 10 years old!', hint='Multiply Tom age by 2.', points=20),
        ])

    # ========================
    # READING - additional 40 questions
    # ========================
    r4 = add_quiz_if_missing('Rhyming Words', 'Reading', 'easy', 'Words that sound alike!')
    if r4:
        add_questions_if_missing(r4, [
            Question(quiz_id=r4.id, text='Which rhymes with "ball"?', option_a='bell', option_b='tall', option_c='bill', option_d='bowl', correct_answer='B', explanation='Tall and ball rhyme!', hint='Ends with "all".', points=10),
            Question(quiz_id=r4.id, text='Which rhymes with "light"?', option_a='late', option_b='let', option_c='kite', option_d='lit', correct_answer='C', explanation='Kite and light rhyme!', hint='Ends with "ite".', points=10),
            Question(quiz_id=r4.id, text='Which rhymes with "make"?', option_a='milk', option_b='cake', option_c='mask', option_d='lake', correct_answer='B', explanation='Cake and make rhyme!', hint='Ends with "ake".', points=10),
            Question(quiz_id=r4.id, text='Which rhymes with "tree"?', option_a='tray', option_b='three', option_c='true', option_d='train', correct_answer='B', explanation='Three and tree rhyme!', hint='Ends with "ee".', points=10),
            Question(quiz_id=r4.id, text='Which rhymes with "bear"?', option_a='beer', option_b='bare', option_c='chair', option_d='dear', correct_answer='C', explanation='Chair and bear rhyme!', hint='Ends with "air".', points=10),
            Question(quiz_id=r4.id, text='Which rhymes with "book"?', option_a='back', option_b='bike', option_c='hook', option_d='box', correct_answer='C', explanation='Hook and book rhyme!', hint='Ends with "ook".', points=10),
            Question(quiz_id=r4.id, text='Which rhymes with "day"?', option_a='die', option_b='tray', option_c='toy', option_d='dot', correct_answer='B', explanation='Tray and day rhyme!', hint='Ends with "ay".', points=10),
        ])

    r5 = add_quiz_if_missing('Reading Comprehension', 'Reading', 'medium', 'Read stories and answer!')
    if r5:
        add_questions_if_missing(r5, [
            Question(quiz_id=r5.id, text='Jill went to the store to buy milk. Where did Jill go?', option_a='park', option_b='store', option_c='school', option_d='home', correct_answer='B', explanation='Jill went to the store!', hint='Read the sentence carefully.', points=10),
            Question(quiz_id=r5.id, text='The dog is brown. It likes to play fetch. What color is the dog?', option_a='black', option_b='white', option_c='brown', option_d='gray', correct_answer='C', explanation='The dog is brown!', hint='Look at the color word.', points=10),
            Question(quiz_id=r5.id, text='Anna wakes up at 7 AM. She eats breakfast. What does Anna do after waking up?', option_a='sleep', option_b='eat breakfast', option_c='go to school', option_d='play', correct_answer='B', explanation='Anna eats breakfast after waking up!', hint='What comes next?', points=10),
            Question(quiz_id=r5.id, text='The cat sat on the mat. The mat is red. What color is the mat?', option_a='blue', option_b='green', option_c='red', option_d='yellow', correct_answer='C', explanation='The mat is red!', hint='Find the color.', points=10),
            Question(quiz_id=r5.id, text='Ben has a blue bike. He rides it to school. How does Ben go to school?', option_a='car', option_b='bike', option_c='bus', option_d='walk', correct_answer='B', explanation='Ben rides his bike to school!', hint='Look for the vehicle.', points=10),
            Question(quiz_id=r5.id, text='It is raining. Lily takes her umbrella. Why does Lily take an umbrella?', option_a='sunny', option_b='raining', option_c='snowing', option_d='windy', correct_answer='B', explanation='Because it is raining!', hint='Check the weather.', points=10),
            Question(quiz_id=r5.id, text='The bird sings in the tree. Where is the bird?', option_a='on ground', option_b='in tree', option_c='in water', option_d='in sky', correct_answer='B', explanation='The bird is in the tree!', hint='Find the location.', points=10),
        ])

    r6 = add_quiz_if_missing('Vocabulary Builder', 'Reading', 'medium', 'Learn new words!')
    if r6:
        add_questions_if_missing(r6, [
            Question(quiz_id=r6.id, text='"Brave" means?', option_a='scared', option_b='courageous', option_c='tired', option_d='sad', correct_answer='B', explanation='Brave means courageous!', hint='Like a superhero.', points=10),
            Question(quiz_id=r6.id, text='"Ancient" means?', option_a='new', option_b='old', option_c='young', option_d='fast', correct_answer='B', explanation='Ancient means very old!', hint='From long ago.', points=10),
            Question(quiz_id=r6.id, text='"Delicious" means?', option_a='yucky', option_b='tasty', option_c='sour', option_d='bitter', correct_answer='B', explanation='Delicious means very tasty!', hint='Yummy!', points=10),
            Question(quiz_id=r6.id, text='"Tiny" means?', option_a='huge', option_b='small', option_c='tall', option_d='wide', correct_answer='B', explanation='Tiny means very small!', hint='Like an ant.', points=10),
            Question(quiz_id=r6.id, text='"Friend" means?', option_a='enemy', option_b='pal', option_c='stranger', option_d='teacher', correct_answer='B', explanation='A friend is a pal!', hint='Someone you like.', points=10),
            Question(quiz_id=r6.id, text='"Rapid" means?', option_a='slow', option_b='quick', option_c='loud', option_d='quiet', correct_answer='B', explanation='Rapid means very fast!', hint='Like a cheetah.', points=10),
            Question(quiz_id=r6.id, text='"Gaze" means?', option_a='look quickly', option_b='stare', option_c='ignore', option_d='forget', correct_answer='B', explanation='Gaze means to stare for a long time!', hint='Looking without blinking.', points=10),
        ])

    r7 = add_quiz_if_missing('Grammar Basics', 'Reading', 'hard', 'Nouns, verbs, more!')
    if r7:
        add_questions_if_missing(r7, [
            Question(quiz_id=r7.id, text='Which is a noun?', option_a='run', option_b='beautiful', option_c='dog', option_d='quickly', correct_answer='C', explanation='Dog is a noun (person, place, thing)!', hint='A thing.', points=15),
            Question(quiz_id=r7.id, text='Which is a verb?', option_a='jump', option_b='happy', option_c='table', option_d='red', correct_answer='A', explanation='Jump is a verb (action)!', hint='An action word.', points=15),
            Question(quiz_id=r7.id, text='Which is an adjective?', option_a='quickly', option_b='blue', option_c='chair', option_d='eat', correct_answer='B', explanation='Blue is an adjective (describes)!', hint='Describes a noun.', points=15),
            Question(quiz_id=r7.id, text='I ___ to school every day.', option_a='go', option_b='goes', option_c='going', option_d='went', correct_answer='A', explanation='I go to school every day!', hint='Present tense.', points=15),
            Question(quiz_id=r7.id, text='She ___ a nice girl.', option_a='am', option_b='are', option_c='is', option_d='be', correct_answer='C', explanation='She is a nice girl!', hint='Use with she/he/it.', points=15),
            Question(quiz_id=r7.id, text='Fill blank: two ____', option_a='cat', option_b='cats', option_c='cates', option_d='caties', correct_answer='B', explanation='Two cats (plural)!', hint='More than one.', points=15),
            Question(quiz_id=r7.id, text='Past of "eat"?', option_a='eated', option_b='eating', option_c='ate', option_d='eaten', correct_answer='C', explanation='Ate is the past tense of eat!', hint='Already happened.', points=15),
        ])

    # ========================
    # SCIENCE - additional 40 questions
    # ========================
    s4 = add_quiz_if_missing('Body & Health', 'Science', 'easy', 'Your amazing body!')
    if s4:
        add_questions_if_missing(s4, [
            Question(quiz_id=s4.id, text='How many bones in adult human body?', option_a='106', option_b='206', option_c='306', option_d='156', correct_answer='B', explanation='206 bones!', hint='About 200.', points=10),
            Question(quiz_id=s4.id, text='What pumps blood in your body?', option_a='brain', option_b='heart', option_c='lungs', option_d='stomach', correct_answer='B', explanation='The heart pumps blood!', hint='Thump-thump.', points=10),
            Question(quiz_id=s4.id, text='Which organ helps you breathe?', option_a='heart', option_b='lungs', option_c='liver', option_d='kidney', correct_answer='B', explanation='Lungs help you breathe!', hint='In your chest.', points=10),
            Question(quiz_id=s4.id, text='What do your teeth help with?', option_a='seeing', option_b='hearing', option_c='chewing', option_d='smelling', correct_answer='C', explanation='Teeth help chew food!', hint='Eating.', points=10),
            Question(quiz_id=s4.id, text='What sense does your nose give?', option_a='taste', option_b='touch', option_c='smell', option_d='sight', correct_answer='C', explanation='Your nose lets you smell!', hint='Flowers and food.', points=10),
            Question(quiz_id=s4.id, text='What color is blood when oxygen-rich?', option_a='blue', option_b='red', option_c='green', option_d='purple', correct_answer='B', explanation='Oxygen-rich blood is bright red!', hint='Not blue.', points=10),
            Question(quiz_id=s4.id, text='How many teeth does a child have?', option_a='20', option_b='28', option_c='32', option_d='24', correct_answer='A', explanation='Children have 20 baby teeth!', hint='Less than adults.', points=10),
        ])

    s5 = add_quiz_if_missing('Plants & Nature', 'Science', 'easy', 'Green world!')
    if s5:
        add_questions_if_missing(s5, [
            Question(quiz_id=s5.id, text='What do plants need to grow?', option_a='water, sun, soil', option_b='only water', option_c='only sun', option_d='only soil', correct_answer='A', explanation='Plants need water, sun, and soil!', hint='Three things.', points=10),
            Question(quiz_id=s5.id, text='What part of plant is underground?', option_a='leaves', option_b='stem', option_c='roots', option_d='flower', correct_answer='C', explanation='Roots grow underground!', hint='Holds plant in place.', points=10),
            Question(quiz_id=s5.id, text='What do leaves make for the plant?', option_a='water', option_b='food', option_c='seeds', option_d='dirt', correct_answer='B', explanation='Leaves make food using sunlight!', hint='Yummy for plant.', points=10),
            Question(quiz_id=s5.id, text='What is a baby plant called?', option_a='seedling', option_b='tree', option_c='flower', option_d='fruit', correct_answer='A', explanation='A baby plant is a seedling!', hint='Just sprouted.', points=10),
            Question(quiz_id=s5.id, text='What color is chlorophyll?', option_a='red', option_b='blue', option_c='green', option_d='yellow', correct_answer='C', explanation='Chlorophyll is green!', hint='Leaf color.', points=10),
            Question(quiz_id=s5.id, text='How do bees help flowers?', option_a='pollination', option_b='eating', option_c='watering', option_d='planting', correct_answer='A', explanation='Bees pollinate flowers!', hint='Carry pollen.', points=10),
            Question(quiz_id=s5.id, text='What part becomes a fruit?', option_a='leaf', option_b='stem', option_c='flower', option_d='root', correct_answer='C', explanation='The flower becomes a fruit!', hint='Blooms then grows.', points=10),
        ])

    s6 = add_quiz_if_missing('Our Planet Earth', 'Science', 'medium', 'Earth science!')
    if s6:
        add_questions_if_missing(s6, [
            Question(quiz_id=s6.id, text='What is Earth mostly covered with?', option_a='land', option_b='water', option_c='ice', option_d='sand', correct_answer='B', explanation='About 71% of Earth is water!', hint='Oceans.', points=15),
            Question(quiz_id=s6.id, text='What causes day and night?', option_a='Earth spinning', option_b='Sun moving', option_c='Moon moving', option_d='Clouds', correct_answer='A', explanation='Earth spins on its axis!', hint='Rotation.', points=15),
            Question(quiz_id=s6.id, text='What gas do we breathe out?', option_a='oxygen', option_b='nitrogen', option_c='carbon dioxide', option_d='hydrogen', correct_answer='C', explanation='We breathe out carbon dioxide!', hint='Plants need this.', points=15),
            Question(quiz_id=s6.id, text='What layer of Earth do we live on?', option_a='mantle', option_b='crust', option_c='core', option_d='magma', correct_answer='B', explanation='We live on the Earth\'s crust!', hint='The top layer.', points=15),
            Question(quiz_id=s6.id, text='What is a volcano?', option_a='mountain that erupts', option_b='a big river', option_c='a deep lake', option_d='a flat plain', correct_answer='A', explanation='A volcano is a mountain that erupts lava!', hint='Hot lava!', points=15),
            Question(quiz_id=s6.id, text='What causes an earthquake?', option_a='wind', option_b='tectonic plates moving', option_c='rain', option_d='snow', correct_answer='B', explanation='Earthquakes happen when tectonic plates move!', hint='Ground shaking.', points=15),
            Question(quiz_id=s6.id, text='What fossil fuel comes from dinosaurs?', option_a='wood', option_b='coal', option_c='paper', option_d='plastic', correct_answer='B', explanation='Coal comes from ancient plants and animals!', hint='Black rock that burns.', points=15),
        ])

    s7 = add_quiz_if_missing('Animals & Habitats', 'Science', 'medium', 'Where animals live!')
    if s7:
        add_questions_if_missing(s7, [
            Question(quiz_id=s7.id, text='Where do polar bears live?', option_a='Africa', option_b='Arctic', option_c='Antarctica', option_d='Australia', correct_answer='B', explanation='Polar bears live in the Arctic (North Pole)!', hint='Very cold north.', points=15),
            Question(quiz_id=s7.id, text='What is a mammal?', option_a='lays eggs', option_b='has fur, feeds milk', option_c='has feathers', option_d='lives in water', correct_answer='B', explanation='Mammals have fur and feed milk to babies!', hint='Humans are mammals.', points=15),
            Question(quiz_id=s7.id, text='Which animal hibernates?', option_a='fish', option_b='bird', option_c='bear', option_d='frog', correct_answer='C', explanation='Bears hibernate (sleep all winter)!', hint='Big, furry, sleeps.', points=15),
            Question(quiz_id=s7.id, text='What do herbivores eat?', option_a='meat', option_b='plants', option_c='both', option_d='insects', correct_answer='B', explanation='Herbivores eat only plants!', hint='Like cows and deer.', points=15),
            Question(quiz_id=s7.id, text='Which is the fastest land animal?', option_a='lion', option_b='horse', option_c='cheetah', option_d='rabbit', correct_answer='C', explanation='Cheetah is fastest! Up to 120 km/h!', hint='Big cat with spots.', points=15),
            Question(quiz_id=s7.id, text='What is metamorphosis?', option_a='changing form', option_b='growing bigger', option_c='dying', option_d='eating', correct_answer='A', explanation='Metamorphosis is changing form like caterpillar to butterfly!', hint='Caterpillar to butterfly.', points=15),
            Question(quiz_id=s7.id, text='Which animal lives in a herd?', option_a='tiger', option_b='lion', option_c='eagle', option_d='shark', correct_answer='B', explanation='Lions live in groups called prides!', hint='King of jungle.', points=15),
        ])

    s8 = add_quiz_if_missing('Space & Beyond', 'Science', 'hard', 'Explore the universe!')
    if s8:
        add_questions_if_missing(s8, [
            Question(quiz_id=s8.id, text='What is a galaxy?', option_a='a star', option_b='a planet', option_c='a group of stars', option_d='a moon', correct_answer='C', explanation='A galaxy is a huge group of stars!', hint='Milky Way.', points=20),
            Question(quiz_id=s8.id, text='What is the hottest planet?', option_a='Mercury', option_b='Venus', option_c='Mars', option_d='Jupiter', correct_answer='B', explanation='Venus is the hottest due to greenhouse effect!', hint='Earth\'s sister planet.', points=20),
            Question(quiz_id=s8.id, text='What keeps planets orbiting the Sun?', option_a='gravity', option_b='wind', option_c='magnetism', option_d='light', correct_answer='A', explanation='Gravity keeps planets in orbit!', hint='Pulls things together.', points=20),
            Question(quiz_id=s8.id, text='What is an asteroid?', option_a='a star', option_b='a small rocky body', option_c='a gas cloud', option_d='a moon', correct_answer='B', explanation='An asteroid is a small rocky body in space!', hint='Space rock.', points=20),
            Question(quiz_id=s8.id, text='Light travels at?', option_a='300 km/s', option_b='300,000 km/s', option_c='3,000 km/s', option_d='30,000 km/s', correct_answer='B', explanation='Light travels at 300,000 km per second!', hint='Very, very fast.', points=20),
            Question(quiz_id=s8.id, text='What is a black hole?', option_a='a dark star', option_b='super strong gravity', option_c='a cave in space', option_d='a dark planet', correct_answer='B', explanation='A black hole has gravity so strong nothing escapes!', hint='Not even light.', points=20),
            Question(quiz_id=s8.id, text='Which planet has the most moons?', option_a='Earth', option_b='Mars', option_c='Jupiter', option_d='Saturn', correct_answer='C', explanation='Jupiter has the most known moons (95+)!', hint='Biggest planet.', points=20),
        ])

    # ========================
    # GEOGRAPHY - additional 40 questions
    # ========================
    g4 = add_quiz_if_missing('Countries & Capitals', 'Geography', 'easy', 'Capital cities!')
    if g4:
        add_questions_if_missing(g4, [
            Question(quiz_id=g4.id, text='Capital of France?', option_a='London', option_b='Paris', option_c='Berlin', option_d='Rome', correct_answer='B', explanation='Paris is the capital of France!', hint='City of lights.', points=10),
            Question(quiz_id=g4.id, text='Capital of Japan?', option_a='Seoul', option_b='Beijing', option_c='Tokyo', option_d='Bangkok', correct_answer='C', explanation='Tokyo is the capital of Japan!', hint='Land of the rising sun.', points=10),
            Question(quiz_id=g4.id, text='Capital of Egypt?', option_a='Cairo', option_b='Nairobi', option_c='Lagos', option_d='Casablanca', correct_answer='A', explanation='Cairo is the capital of Egypt!', hint='Near pyramids.', points=10),
            Question(quiz_id=g4.id, text='Capital of Australia?', option_a='Sydney', option_b='Melbourne', option_c='Canberra', option_d='Perth', correct_answer='C', explanation='Canberra is the capital of Australia!', hint='Not Sydney.', points=10),
            Question(quiz_id=g4.id, text='Capital of Canada?', option_a='Toronto', option_b='Vancouver', option_c='Ottawa', option_d='Montreal', correct_answer='C', explanation='Ottawa is the capital of Canada!', hint='Maple leaf country.', points=10),
            Question(quiz_id=g4.id, text='Capital of Brazil?', option_a='Rio de Janeiro', option_b='Sao Paulo', option_c='Brasilia', option_d='Salvador', correct_answer='C', explanation='Brasilia is the capital of Brazil!', hint='South America.', points=10),
            Question(quiz_id=g4.id, text='Capital of India?', option_a='Mumbai', option_b='New Delhi', option_c='Chennai', option_d='Kolkata', correct_answer='B', explanation='New Delhi is the capital of India!', hint='Taj Mahal country.', points=10),
        ])

    g5 = add_quiz_if_missing('Landforms', 'Geography', 'easy', 'Mountains and more!')
    if g5:
        add_questions_if_missing(g5, [
            Question(quiz_id=g5.id, text='Highest mountain in the world?', option_a='K2', option_b='Everest', option_c='Kilimanjaro', option_d='Denali', correct_answer='B', explanation='Mt Everest is the highest!', hint='Nepal/Tibet.', points=10),
            Question(quiz_id=g5.id, text='What is a desert?', option_a='wet place', option_b='cold place', option_c='dry place', option_d='forest', correct_answer='C', explanation='A desert gets very little rain!', hint='Sandy and dry.', points=10),
            Question(quiz_id=g5.id, text='What is an island?', option_a='land surrounded by water', option_b='big mountain', option_c='deep valley', option_d='flat land', correct_answer='A', explanation='An island is land surrounded by water!', hint='Like Hawaii.', points=10),
            Question(quiz_id=g5.id, text='Longest mountain range?', option_a='Himalayas', option_b='Andes', option_c='Alps', option_d='Rockies', correct_answer='B', explanation='The Andes is the longest mountain range!', hint='South America.', points=10),
            Question(quiz_id=g5.id, text='What is a peninsula?', option_a='land surrounded by water on 3 sides', option_b='island', option_c='desert', option_d='volcano', correct_answer='A', explanation='A peninsula is land with water on 3 sides!', hint='Like Florida.', points=10),
            Question(quiz_id=g5.id, text='Deepest ocean trench?', option_a='Mariana', option_b='Puerto Rico', option_c='Java', option_d='Peru-Chile', correct_answer='A', explanation='The Mariana Trench is deepest!', hint='Pacific Ocean.', points=10),
            Question(quiz_id=g5.id, text='What is a glacier?', option_a='hot spring', option_b='ice river', option_c='fast river', option_d='dry lake', correct_answer='B', explanation='A glacier is a slow-moving river of ice!', hint='Very cold ice formation.', points=10),
        ])

    g6 = add_quiz_if_missing('World Cultures', 'Geography', 'medium', 'People around the world!')
    if g6:
        add_questions_if_missing(g6, [
            Question(quiz_id=g6.id, text='Most spoken language in the world?', option_a='English', option_b='Mandarin Chinese', option_c='Spanish', option_d='Hindi', correct_answer='B', explanation='Mandarin Chinese is the most spoken!', hint='Spoken by most people.', points=15),
            Question(quiz_id=g6.id, text='Largest country by area?', option_a='USA', option_b='China', option_c='Russia', option_d='Canada', correct_answer='C', explanation='Russia is the largest country!', hint='Spans two continents.', points=15),
            Question(quiz_id=g6.id, text='Most populous country?', option_a='India', option_b='China', option_c='USA', option_d='Indonesia', correct_answer='A', explanation='India is the most populous country!', hint='Over 1.4 billion people.', points=15),
            Question(quiz_id=g6.id, text='Which continent has the most countries?', option_a='Asia', option_b='Africa', option_c='Europe', option_d='South America', correct_answer='B', explanation='Africa has 54 countries!', hint='Second largest continent.', points=15),
            Question(quiz_id=g6.id, text='What is the currency of Japan?', option_a='Yuan', option_b='Won', option_c='Yen', option_d='Dollar', correct_answer='C', explanation='Japan uses the Yen!', hint='Symbol is ¥.', points=15),
            Question(quiz_id=g6.id, text='Which country has the most time zones?', option_a='USA', option_b='Russia', option_c='France', option_d='China', correct_answer='C', explanation='France has the most time zones (12-13)!', hint='Includes overseas territories.', points=15),
            Question(quiz_id=g6.id, text='What is the world population?', option_a='5 billion', option_b='7 billion', option_c='8 billion', option_d='10 billion', correct_answer='C', explanation='World population is about 8 billion!', hint='Around 8,000,000,000.', points=15),
        ])

    # ========================
    # ART - additional 40 questions
    # ========================
    a4 = add_quiz_if_missing('Color Theory', 'Art', 'easy', 'How colors work!')
    if a4:
        add_questions_if_missing(a4, [
            Question(quiz_id=a4.id, text='Red + Yellow = ?', option_a='Green', option_b='Purple', option_c='Orange', option_d='Blue', correct_answer='C', explanation='Red and Yellow make Orange!', hint='Think of a pumpkin!', points=10),
            Question(quiz_id=a4.id, text='Blue + Yellow = ?', option_a='Green', option_b='Purple', option_c='Orange', option_d='Red', correct_answer='A', explanation='Blue and Yellow make Green!', hint='Grass color.', points=10),
            Question(quiz_id=a4.id, text='Warm colors are?', option_a='blue, green, purple', option_b='red, orange, yellow', option_c='pink, brown, gray', option_d='black, white', correct_answer='B', explanation='Warm colors include red, orange, yellow!', hint='Fire colors.', points=10),
            Question(quiz_id=a4.id, text='Cool colors are?', option_a='red, orange', option_b='blue, green, purple', option_c='yellow, pink', option_d='brown, tan', correct_answer='B', explanation='Cool colors include blue, green, purple!', hint='Water colors.', points=10),
            Question(quiz_id=a4.id, text='Black and white are?', option_a='primary', option_b='secondary', option_c='neutral', option_d='warm', correct_answer='C', explanation='Black and white are neutral colors!', hint='They match everything.', points=10),
            Question(quiz_id=a4.id, text='What are primary colors?', option_a='RGB', option_b='RYB', option_c='GBO', option_d='RGP', correct_answer='B', explanation='Primary colors are Red, Yellow, Blue!', hint='Cannot be made by mixing.', points=10),
            Question(quiz_id=a4.id, text='What are secondary colors?', option_a='RGB', option_b='purple, orange, green', option_c='red, yellow, blue', option_d='black, white, gray', correct_answer='B', explanation='Secondary colors are made by mixing two primaries!', hint='Mix two primary colors.', points=10),
        ])

    a5 = add_quiz_if_missing('Art Techniques', 'Art', 'medium', 'How to create art!')
    if a5:
        add_questions_if_missing(a5, [
            Question(quiz_id=a5.id, text='What is a self-portrait?', option_a='painting of nature', option_b='painting of yourself', option_c='painting of food', option_d='painting of house', correct_answer='B', explanation='A self-portrait is a painting of yourself!', hint='Draw your own face.', points=15),
            Question(quiz_id=a5.id, text='What is perspective in art?', option_a='color mixing', option_b='depth and distance illusion', option_c='type of brush', option_d='kind of paper', correct_answer='B', explanation='Perspective creates depth in art!', hint='Things far away look smaller.', points=15),
            Question(quiz_id=a5.id, text='What is a still life?', option_a='living person painting', option_b='object arrangement painting', option_c='landscape painting', option_d='abstract work', correct_answer='B', explanation='Still life is a painting of arranged objects!', hint='Fruit bowls, flowers, etc.', points=15),
            Question(quiz_id=a5.id, text='What medium uses pigment and egg yolk?', option_a='watercolor', option_b='tempera', option_c='oil', option_d='acrylic', correct_answer='B', explanation='Tempera uses egg yolk as binder!', hint='Very old technique.', points=15),
            Question(quiz_id=a5.id, text='What is a mural?', option_a='small drawing', option_b='large wall painting', option_c='clay sculpture', option_d='photo collage', correct_answer='B', explanation='A mural is a large painting on a wall!', hint='On buildings.', points=15),
            Question(quiz_id=a5.id, text='What tool do sculptors use?', option_a='brush', option_b='chisel', option_c='pencil', option_d='camera', correct_answer='B', explanation='Sculptors use chisels to carve!', hint='For stone and wood.', points=15),
            Question(quiz_id=a5.id, text='What is a sketch?', option_a='finished painting', option_b='quick rough drawing', option_c='type of print', option_d='clay model', correct_answer='B', explanation='A sketch is a quick rough drawing!', hint='Planning stage.', points=15),
        ])

    a6 = add_quiz_if_missing('Famous Artists', 'Art', 'medium', 'Art masters!')
    if a6:
        add_questions_if_missing(a6, [
            Question(quiz_id=a6.id, text='Which artist cut off his ear?', option_a='Picasso', option_b='Van Gogh', option_c='Monet', option_d='Rembrandt', correct_answer='B', explanation='Van Gogh cut off his ear!', hint='Starry Night painter.', points=15),
            Question(quiz_id=a6.id, text='Picasso co-founded which art movement?', option_a='Impressionism', option_b='Cubism', option_c='Surrealism', option_d='Pop Art', correct_answer='B', explanation='Picasso co-founded Cubism!', hint='Geometric shapes.', points=15),
            Question(quiz_id=a6.id, text='Which artist painted the Sistine Chapel?', option_a='Da Vinci', option_b='Michelangelo', option_c='Raphael', option_d='Donatello', correct_answer='B', explanation='Michelangelo painted the Sistine Chapel ceiling!', hint='Lying on scaffolding.', points=15),
            Question(quiz_id=a6.id, text='Which artist is known for pop art?', option_a='Warhol', option_b='Monet', option_c='Van Gogh', option_d='Rembrandt', correct_answer='A', explanation='Andy Warhol made pop art like Campbell Soup cans!', hint='Soup cans.', points=15),
            Question(quiz_id=a6.id, text='Claude Monet was part of which movement?', option_a='Cubism', option_b='Impressionism', option_c='Realism', option_d='Baroque', correct_answer='B', explanation='Monet was an Impressionist!', hint='Water lilies.', points=15),
            Question(quiz_id=a6.id, text='Which artist is known for melting clocks?', option_a='Dali', option_b='Magritte', option_c='Picasso', option_d='Matisse', correct_answer='A', explanation='Salvador Dali painted melting clocks!', hint='Surrealist.', points=15),
            Question(quiz_id=a6.id, text='Renaissance means?', option_a='rebirth', option_b='dark age', option_c='new art', option_d='old style', correct_answer='A', explanation='Renaissance means rebirth in French!', hint='Born again.', points=15),
        ])

    # ========================
    # CODING - additional 40 questions
    # ========================
    c4 = add_quiz_if_missing('Programming Basics', 'Coding', 'easy', 'Learn to code!')
    if c4:
        add_questions_if_missing(c4, [
            Question(quiz_id=c4.id, text='What is a computer program?', option_a='a TV show', option_b='a set of instructions', option_c='a video game', option_d='a website', correct_answer='B', explanation='A program is a set of instructions for a computer!', hint='Like a recipe.', points=10),
            Question(quiz_id=c4.id, text='What does CPU stand for?', option_a='Central Processing Unit', option_b='Computer Personal Unit', option_c='Core Program Utility', option_d='Central Power Unit', correct_answer='A', explanation='CPU = Central Processing Unit, the brain of the computer!', hint='The brain.', points=10),
            Question(quiz_id=c4.id, text='What is a variable?', option_a='a fixed number', option_b='a storage container for data', option_c='a type of loop', option_d='a mouse', correct_answer='B', explanation='A variable stores data that can change!', hint='Like a labeled box.', points=10),
            Question(quiz_id=c4.id, text='What is a function?', option_a='a party', option_b='a reusable block of code', option_c='a type of keyboard', option_d='a monitor', correct_answer='B', explanation='A function is a reusable block of code that does a task!', hint='def something():', points=10),
            Question(quiz_id=c4.id, text='What is a string?', option_a='a number', option_b='a list of items', option_c='a sequence of characters', option_d='a boolean', correct_answer='C', explanation='A string is a sequence of characters like "hello"!', hint='Text in quotes.', points=10),
            Question(quiz_id=c4.id, text='Boolean values are?', option_a='numbers', option_b='true or false', option_c='letters', option_d='symbols', correct_answer='B', explanation='Boolean values are True or False!', hint='Yes or No.', points=10),
            Question(quiz_id=c4.id, text='What does "debug" mean?', option_a='run faster', option_b='find and fix errors', option_c='write new code', option_d='delete code', correct_answer='B', explanation='Debugging means finding and fixing errors in code!', hint='Remove bugs.', points=10),
        ])

    c5 = add_quiz_if_missing('Web Development', 'Coding', 'medium', 'Build websites!')
    if c5:
        add_questions_if_missing(c5, [
            Question(quiz_id=c5.id, text='What does HTML stand for?', option_a='HyperText Markup Language', option_b='High Tech Modern Language', option_c='Home Tool Markup Language', option_d='HyperText Modern Links', correct_answer='A', explanation='HTML = HyperText Markup Language!', hint='Structure of web pages.', points=15),
            Question(quiz_id=c5.id, text='What does CSS do?', option_a='adds structure', option_b='adds style', option_c='adds logic', option_d='adds data', correct_answer='B', explanation='CSS styles web pages (colors, layout, fonts)!', hint='Makes things pretty.', points=15),
            Question(quiz_id=c5.id, text='What does JavaScript do?', option_a='styles pages', option_b='adds interactivity', option_c='structures content', option_d='stores data', correct_answer='B', explanation='JavaScript adds interactivity to web pages!', hint='Makes things move.', points=15),
            Question(quiz_id=c5.id, text='What is a tag in HTML?', option_a='<like this>', option_b='(like this)', option_c='[like this]', option_d='{like this}', correct_answer='A', explanation='HTML tags use angle brackets like <tag>!', hint='Pointy brackets.', points=15),
            Question(quiz_id=c5.id, text='What does a link use?', option_a='<a> tag', option_b='<link> tag', option_c='<href> tag', option_d='<url> tag', correct_answer='A', explanation='Links use the <a> (anchor) tag!', hint='Anchor creates links.', points=15),
            Question(quiz_id=c5.id, text='What is a database?', option_a='a spreadsheet', option_b='organized data storage', option_c='a programming language', option_d='a web server', correct_answer='B', explanation='A database is organized data storage!', hint='Stores information.', points=15),
            Question(quiz_id=c5.id, text='What does API stand for?', option_a='Application Programming Interface', option_b='Automatic Program Integration', option_c='Applied Processing Input', option_d='Advanced Programming Idea', correct_answer='A', explanation='API = Application Programming Interface!', hint='Connects programs.', points=15),
        ])

    c6 = add_quiz_if_missing('Internet & Networks', 'Coding', 'medium', 'How the web works!')
    if c6:
        add_questions_if_missing(c6, [
            Question(quiz_id=c6.id, text='What does IP stand for?', option_a='Internet Protocol', option_b='Internal Program', option_c='Input Process', option_d='Integrated Path', correct_answer='A', explanation='IP = Internet Protocol!', hint='Address for devices.', points=15),
            Question(quiz_id=c6.id, text='What is a server?', option_a='a waiter', option_b='a computer that provides data', option_c='a type of keyboard', option_d='a mouse', correct_answer='B', explanation='A server provides data to other computers!', hint='Serves information.', points=15),
            Question(quiz_id=c6.id, text='What is a router?', option_a='a cutting tool', option_b='connects networks', option_c='a file type', option_d='a type of cable', correct_answer='B', explanation='A router connects different networks together!', hint='Directs traffic.', points=15),
            Question(quiz_id=c6.id, text='What does URL stand for?', option_a='Universal Resource Locator', option_b='Uniform Resource Locator', option_c='Unified Resource Link', option_d='Universal Reference Link', correct_answer='B', explanation='URL = Uniform Resource Locator!', hint='Web address.', points=15),
            Question(quiz_id=c6.id, text='What is a firewall?', option_a='a wall that burns', option_b='network security system', option_c='a type of virus', option_d='a browser', correct_answer='B', explanation='A firewall protects networks from unauthorized access!', hint='Keeps bad things out.', points=15),
            Question(quiz_id=c6.id, text='What does HTTP do?', option_a='transfers web pages', option_b='sends emails', option_c='downloads files', option_d='prints documents', correct_answer='A', explanation='HTTP transfers web pages and data on the internet!', hint='Web protocol.', points=15),
            Question(quiz_id=c6.id, text='What is encryption?', option_a='deleting data', option_b='encoding data for security', option_c='sorting data', option_d='copying data', correct_answer='B', explanation='Encryption encodes data so only authorized people can read it!', hint='Secret code.', points=15),
        ])

    # ========================
    # MUSIC - additional 40 questions
    # ========================
    u4 = add_quiz_if_missing('Music Notes & Rhythm', 'Music', 'easy', 'Read music!')
    if u4:
        add_questions_if_missing(u4, [
            Question(quiz_id=u4.id, text='How many beats in a whole note?', option_a='1', option_b='2', option_c='3', option_d='4', correct_answer='D', explanation='A whole note gets 4 beats!', hint='Longest note.', points=10),
            Question(quiz_id=u4.id, text='How many beats in a half note?', option_a='4', option_b='3', option_c='2', option_d='1', correct_answer='C', explanation='A half note gets 2 beats!', hint='Half of whole note.', points=10),
            Question(quiz_id=u4.id, text='How many beats in a quarter note?', option_a='4', option_b='3', option_c='2', option_d='1', correct_answer='D', explanation='A quarter note gets 1 beat!', hint='One tap.', points=10),
            Question(quiz_id=u4.id, text='Musical staff has how many lines?', option_a='4', option_b='5', option_c='6', option_d='3', correct_answer='B', explanation='The staff has 5 lines!', hint='Notes sit on lines and spaces.', points=10),
            Question(quiz_id=u4.id, text='What is a rest in music?', option_a='sleep time', option_b='a pause in sound', option_c='a type of note', option_d='a loud part', correct_answer='B', explanation='A rest is silence in music!', hint='No sound.', points=10),
            Question(quiz_id=u4.id, text='What is tempo?', option_a='loudness', option_b='speed of music', option_c='pitch', option_d='tone color', correct_answer='B', explanation='Tempo is the speed of the music!', hint='Fast or slow.', points=10),
            Question(quiz_id=u4.id, text='What is a scale?', option_a='a type of instrument', option_b='a series of notes in order', option_c='a big sound', option_d='a music stand', correct_answer='B', explanation='A scale is a series of notes in ascending/descending order!', hint='Do Re Mi Fa Sol La Ti Do.', points=10),
        ])

    u5 = add_quiz_if_missing('Music History', 'Music', 'medium', 'Famous composers!')
    if u5:
        add_questions_if_missing(u5, [
            Question(quiz_id=u5.id, text='Which composer went deaf?', option_a='Mozart', option_b='Beethoven', option_c='Bach', option_d='Chopin', correct_answer='B', explanation='Beethoven continued composing even after going deaf!', hint='5th Symphony.', points=15),
            Question(quiz_id=u5.id, text='Which composer wrote "The Four Seasons"?', option_a='Vivaldi', option_b='Mozart', option_c='Bach', option_d='Handel', correct_answer='A', explanation='Vivaldi wrote "The Four Seasons"!', hint='Italian composer.', points=15),
            Question(quiz_id=u5.id, text='Which era did Mozart compose in?', option_a='Baroque', option_b='Classical', option_c='Romantic', option_d='Modern', correct_answer='B', explanation='Mozart composed in the Classical era!', hint='1700s.', points=15),
            Question(quiz_id=u5.id, text='Bach is from which era?', option_a='Classical', option_b='Baroque', option_c='Romantic', option_d='Renaissance', correct_answer='B', explanation='Bach is from the Baroque era!', hint='1600s-1700s.', points=15),
            Question(quiz_id=u5.id, text='"The Magic Flute" is by?', option_a='Beethoven', option_b='Mozart', option_c='Bach', option_d='Wagner', correct_answer='B', explanation='Mozart wrote "The Magic Flute"!', hint='An opera.', points=15),
            Question(quiz_id=u5.id, text='What instrument did Chopin play?', option_a='violin', option_b='cello', option_c='piano', option_d='flute', correct_answer='C', explanation='Chopin composed mainly for piano!', hint='Keyboard instrument.', points=15),
            Question(quiz_id=u5.id, text='Which composer wrote 9 symphonies?', option_a='Mozart', option_b='Bach', option_c='Beethoven', option_d='Brahms', correct_answer='C', explanation='Beethoven wrote 9 famous symphonies!', hint='Ode to Joy is Symphony No. 9.', points=15),
        ])

    u6 = add_quiz_if_missing('Instruments of the Orchestra', 'Music', 'medium', 'Orchestra instruments!')
    if u6:
        add_questions_if_missing(u6, [
            Question(quiz_id=u6.id, text='Which instrument has the highest pitch in orchestra?', option_a='violin', option_b='flute', option_c='piccolo', option_d='trumpet', correct_answer='C', explanation='The piccolo is the highest pitched!', hint='Small flute.', points=15),
            Question(quiz_id=u6.id, text='Lowest string instrument?', option_a='violin', option_b='viola', option_c='cello', option_d='double bass', correct_answer='D', explanation='The double bass is the lowest!', hint='Biggest string instrument.', points=15),
            Question(quiz_id=u6.id, text='Which brass instrument has a slide?', option_a='trumpet', option_b='trombone', option_c='french horn', option_d='tuba', correct_answer='B', explanation='The trombone uses a slide to change pitch!', hint='Push-pull.', points=15),
            Question(quiz_id=u6.id, text='Which woodwind uses a double reed?', option_a='flute', option_b='clarinet', option_c='oboe', option_d='saxophone', correct_answer='C', explanation='The oboe uses a double reed!', hint='Two reeds tied together.', points=15),
            Question(quiz_id=u6.id, text='Largest instrument in the orchestra?', option_a='tuba', option_b='double bass', option_c='harp', option_d='organ', correct_answer='D', explanation='The pipe organ is the largest!', hint='Uses pipes.', points=15),
            Question(quiz_id=u6.id, text='How many strings on a violin?', option_a='6', option_b='4', option_c='5', option_d='3', correct_answer='B', explanation='A violin has 4 strings!', hint='G, D, A, E.', points=15),
            Question(quiz_id=u6.id, text='Which percussion instrument has definite pitch?', option_a='snare drum', option_b='cymbals', option_c='xylophone', option_d='triangle', correct_answer='C', explanation='Xylophone has definite pitch (can play melodies)!', hint='Wooden bars.', points=15),
        ])

    # ========================
    # ABC - additional 40 questions
    # ========================
    abc4 = add_quiz_if_missing('Letters U-Z', 'ABC', 'easy', 'Last letters!')
    if abc4:
        add_questions_if_missing(abc4, [
            Question(quiz_id=abc4.id, text='What letter is "Umbrella" for?', option_a='U', option_b='V', option_c='W', option_d='X', correct_answer='A', explanation='Umbrella starts with U!', hint='☂️ u-mbrella.', points=5),
            Question(quiz_id=abc4.id, text='What letter is "Violin" for?', option_a='U', option_b='V', option_c='W', option_d='X', correct_answer='B', explanation='Violin starts with V!', hint='🎻 v-iolin.', points=5),
            Question(quiz_id=abc4.id, text='What letter is "Whale" for?', option_a='V', option_b='W', option_c='X', option_d='Y', correct_answer='B', explanation='Whale starts with W!', hint='🐳 w-hale.', points=5),
            Question(quiz_id=abc4.id, text='What letter is "X-ray" for?', option_a='W', option_b='X', option_c='Y', option_d='Z', correct_answer='B', explanation='X-ray starts with X!', hint='🩻 x-ray.', points=5),
            Question(quiz_id=abc4.id, text='What letter is "Yoghurt" for?', option_a='X', option_b='Y', option_c='Z', option_d='W', correct_answer='B', explanation='Yoghurt starts with Y!', hint='🥄 y-ogurt.', points=5),
            Question(quiz_id=abc4.id, text='What letter is "Zoo" for?', option_a='X', option_b='Y', option_c='Z', option_d='W', correct_answer='C', explanation='Zoo starts with Z!', hint='🦁 z-oo.', points=5),
            Question(quiz_id=abc4.id, text='What comes before U?', option_a='T', option_b='S', option_c='V', option_d='W', correct_answer='A', explanation='T comes before U!', hint='R, S, T, U, V.', points=5),
        ])

    abc5 = add_quiz_if_missing('Letter Matching', 'ABC', 'easy', 'Match uppercase and lowercase!')
    if abc5:
        add_questions_if_missing(abc5, [
            Question(quiz_id=abc5.id, text='Lowercase of A?', option_a='a', option_b='e', option_c='i', option_d='o', correct_answer='A', explanation='Lowercase A is "a"!', hint='Looks similar.', points=5),
            Question(quiz_id=abc5.id, text='Lowercase of B?', option_a='d', option_b='p', option_c='b', option_d='q', correct_answer='C', explanation='Lowercase B is "b"!', hint='Has a belly.', points=5),
            Question(quiz_id=abc5.id, text='Lowercase of D?', option_a='b', option_b='d', option_c='p', option_d='q', correct_answer='B', explanation='Lowercase D is "d"!', hint='Has a tail.', points=5),
            Question(quiz_id=abc5.id, text='Uppercase of "g"?', option_a='C', option_b='D', option_c='G', option_d='J', correct_answer='C', explanation='Uppercase of "g" is G!', hint='Capital letter.', points=5),
            Question(quiz_id=abc5.id, text='Uppercase of "m"?', option_a='N', option_b='W', option_c='M', option_d='V', correct_answer='C', explanation='Uppercase of "m" is M!', hint='Two humps.', points=5),
            Question(quiz_id=abc5.id, text='Lowercase of L?', option_a='I', option_b='l', option_c='1', option_d='|', correct_answer='B', explanation='Lowercase L is "l"!', hint='A straight line.', points=5),
            Question(quiz_id=abc5.id, text='Uppercase of "t"?', option_a='L', option_b='T', option_c='F', option_d='I', correct_answer='B', explanation='Uppercase of "t" is T!', hint='Cross on top.', points=5),
        ])

    abc6 = add_quiz_if_missing('Vowels & Consonants', 'ABC', 'medium', 'Vowels are special!')
    if abc6:
        add_questions_if_missing(abc6, [
            Question(quiz_id=abc6.id, text='Which is a vowel?', option_a='A', option_b='B', option_c='C', option_d='D', correct_answer='A', explanation='A is a vowel!', hint='A, E, I, O, U.', points=5),
            Question(quiz_id=abc6.id, text='How many vowels in English?', option_a='3', option_b='4', option_c='5', option_d='6', correct_answer='C', explanation='There are 5 vowels: A, E, I, O, U!', hint='A-E-I-O-U.', points=5),
            Question(quiz_id=abc6.id, text='Which word starts with a vowel?', option_a='Cat', option_b='Apple', option_c='Dog', option_d='Sun', correct_answer='B', explanation='Apple starts with vowel A!', hint='🍎', points=5),
            Question(quiz_id=abc6.id, text='Which word starts with a consonant?', option_a='Elephant', option_b='Umbrella', option_c='Octopus', option_d='House', correct_answer='D', explanation='House starts with H, a consonant!', hint='🏠 H is not A-E-I-O-U.', points=5),
            Question(quiz_id=abc6.id, text='What letter is sometimes a vowel?', option_a='B', option_c='Y', option_d='W', option_b='X', correct_answer='C', explanation='Y can sometimes be a vowel (as in "sky" or "gym")!', hint='Why?', points=5),
            Question(quiz_id=abc6.id, text='Which word has no vowels?', option_a='Fly', option_b='Sun', option_c='Cat', option_d='Pen', correct_answer='A', explanation='"Fly" has no vowels - Y acts as vowel!', hint='F-L-Y.', points=5),
            Question(quiz_id=abc6.id, text='Which word has 3 vowels?', option_a='Hello', option_b='Beautiful', option_c='Doggy', option_d='Bird', correct_answer='B', explanation='Beautiful has 3 vowels: e-a-i-u!', hint='Be-au-ti-ful.', points=5),
        ])

    abc7 = add_quiz_if_missing('ABC Order', 'ABC', 'medium', 'Alphabetical order!')
    if abc7:
        add_questions_if_missing(abc7, [
            Question(quiz_id=abc7.id, text='Which comes first: C or F?', option_a='C', option_b='F', option_c='D', option_d='E', correct_answer='A', explanation='C comes before F!', hint='A, B, C...', points=5),
            Question(quiz_id=abc7.id, text='Which comes last: X, W, Z?', option_a='X', option_b='W', option_c='Z', option_d='Y', correct_answer='C', explanation='Z is the last letter!', hint='End of alphabet.', points=5),
            Question(quiz_id=abc7.id, text='Sort: B, D, A. Which first?', option_a='A', option_b='B', option_c='D', option_d='C', correct_answer='A', explanation='A comes before B and D!', hint='A is first.', points=5),
            Question(quiz_id=abc7.id, text='Which letter is between B and D?', option_a='A', option_b='C', option_c='E', option_d='F', correct_answer='B', explanation='C is between B and D!', hint='B, ?, D.', points=5),
            Question(quiz_id=abc7.id, text='Which letter is between P and R?', option_a='S', option_b='O', option_c='Q', option_d='N', correct_answer='C', explanation='Q is between P and R!', hint='P, ?, R.', points=5),
            Question(quiz_id=abc7.id, text='Alphabet has how many letters?', option_a='24', option_b='25', option_c='26', option_d='27', correct_answer='C', explanation='Alphabet has 26 letters!', hint='A to Z.', points=5),
            Question(quiz_id=abc7.id, text='5th letter of alphabet?', option_a='D', option_b='E', option_c='F', option_d='G', correct_answer='B', explanation='E is the 5th letter!', hint='A=1, B=2, C=3, D=4, E=5.', points=5),
        ])

    # ========================
    # 123 - additional 40 questions
    # ========================
    num5 = add_quiz_if_missing('Addition Within 10', '123', 'easy', 'Add small numbers!')
    if num5:
        add_questions_if_missing(num5, [
            Question(quiz_id=num5.id, text='3 + 2 = ?', option_a='4', option_b='5', option_c='6', option_d='3', correct_answer='B', explanation='3 + 2 = 5!', hint='Count: 3, 4, 5.', points=5),
            Question(quiz_id=num5.id, text='4 + 4 = ?', option_a='6', option_b='7', option_c='8', option_d='9', correct_answer='C', explanation='4 + 4 = 8!', hint='Double 4.', points=5),
            Question(quiz_id=num5.id, text='2 + 7 = ?', option_a='8', option_b='10', option_c='7', option_d='9', correct_answer='D', explanation='2 + 7 = 9!', hint='Start at 2, count 7 more.', points=5),
            Question(quiz_id=num5.id, text='5 + 5 = ?', option_a='9', option_b='10', option_c='11', option_d='8', correct_answer='B', explanation='5 + 5 = 10!', hint='Double 5.', points=5),
            Question(quiz_id=num5.id, text='1 + 6 = ?', option_a='6', option_b='8', option_c='5', option_d='7', correct_answer='D', explanation='1 + 6 = 7!', hint='Count up from 1.', points=5),
            Question(quiz_id=num5.id, text='4 + 3 = ?', option_a='5', option_b='6', option_c='7', option_d='8', correct_answer='C', explanation='4 + 3 = 7!', hint='Count: 4, 5, 6, 7.', points=5),
            Question(quiz_id=num5.id, text='0 + 9 = ?', option_a='0', option_b='8', option_c='10', option_d='9', correct_answer='D', explanation='0 + 9 = 9!', hint='Adding 0 does nothing.', points=5),
        ])

    num6 = add_quiz_if_missing('Subtraction Within 10', '123', 'easy', 'Subtract small numbers!')
    if num6:
        add_questions_if_missing(num6, [
            Question(quiz_id=num6.id, text='7 - 3 = ?', option_a='3', option_b='5', option_c='4', option_d='6', correct_answer='C', explanation='7 - 3 = 4!', hint='Count back from 7.', points=5),
            Question(quiz_id=num6.id, text='9 - 5 = ?', option_a='3', option_b='5', option_c='4', option_d='6', correct_answer='C', explanation='9 - 5 = 4!', hint='9 minus 5.', points=5),
            Question(quiz_id=num6.id, text='6 - 6 = ?', option_a='0', option_b='1', option_c='6', option_d='12', correct_answer='A', explanation='6 - 6 = 0!', hint='Take away everything.', points=5),
            Question(quiz_id=num6.id, text='8 - 4 = ?', option_a='3', option_b='5', option_c='4', option_d='6', correct_answer='C', explanation='8 - 4 = 4!', hint='Half of 8.', points=5),
            Question(quiz_id=num6.id, text='10 - 3 = ?', option_a='5', option_b='6', option_c='7', option_d='8', correct_answer='C', explanation='10 - 3 = 7!', hint='Count back from 10.', points=5),
            Question(quiz_id=num6.id, text='5 - 2 = ?', option_a='2', option_b='4', option_c='5', option_d='3', correct_answer='D', explanation='5 - 2 = 3!', hint='Start at 5, back 2.', points=5),
            Question(quiz_id=num6.id, text='8 - 0 = ?', option_a='7', option_b='9', option_c='8', option_d='6', correct_answer='C', explanation='8 - 0 = 8!', hint='Taking nothing away.', points=5),
        ])

    num7 = add_quiz_if_missing('Skip Counting', '123', 'medium', 'Count by 2s, 5s, 10s!')
    if num7:
        add_questions_if_missing(num7, [
            Question(quiz_id=num7.id, text='Count by 2s: 2, 4, 6, __?', option_a='7', option_b='8', option_c='9', option_d='10', correct_answer='B', explanation='6 + 2 = 8!', hint='Two more each time.', points=10),
            Question(quiz_id=num7.id, text='Count by 5s: 5, 10, 15, __?', option_a='16', option_b='18', option_c='20', option_d='25', correct_answer='C', explanation='15 + 5 = 20!', hint='Five more each time.', points=10),
            Question(quiz_id=num7.id, text='Count by 10s: 10, 20, 30, __?', option_a='35', option_b='31', option_c='40', option_d='50', correct_answer='C', explanation='30 + 10 = 40!', hint='Ten more each time.', points=10),
            Question(quiz_id=num7.id, text='Count backwards: 10, 9, 8, __?', option_a='7', option_b='6', option_c='5', option_d='11', correct_answer='A', explanation='8 - 1 = 7!', hint='One less each time.', points=10),
            Question(quiz_id=num7.id, text='Skip count 3s: 3, 6, 9, __?', option_a='10', option_b='11', option_c='12', option_d='13', correct_answer='C', explanation='9 + 3 = 12!', hint='Three more each time.', points=10),
            Question(quiz_id=num7.id, text='Count backwards from 20 by 2s: 20, 18, 16, __?', option_a='15', option_b='12', option_c='14', option_d='13', correct_answer='C', explanation='16 - 2 = 14!', hint='Two less each time.', points=10),
            Question(quiz_id=num7.id, text='What comes after 7 in skip count? 1, 3, 5, 7, __?', option_a='8', option_b='9', option_c='10', option_d='11', correct_answer='B', explanation='7 + 2 = 9!', hint='Counting odd numbers.', points=10),
        ])

    num8 = add_quiz_if_missing('Comparing Numbers', '123', 'medium', 'Bigger and smaller!')
    if num8:
        add_questions_if_missing(num8, [
            Question(quiz_id=num8.id, text='Which is bigger: 15 or 9?', option_a='15', option_b='9', option_c='12', option_d='8', correct_answer='A', explanation='15 is bigger than 9!', hint='15 has more value.', points=5),
            Question(quiz_id=num8.id, text='Which is smaller: 23 or 32?', option_a='23', option_b='32', option_c='40', option_d='50', correct_answer='A', explanation='23 is smaller than 32!', hint='23 has fewer tens.', points=5),
            Question(quiz_id=num8.id, text='Which number is between 5 and 7?', option_a='4', option_b='6', option_c='8', option_d='9', correct_answer='B', explanation='6 is between 5 and 7!', hint='5, ?, 7.', points=5),
            Question(quiz_id=num8.id, text='What is 10 more than 25?', option_a='26', option_b='35', option_c='30', option_d='45', correct_answer='B', explanation='25 + 10 = 35!', hint='Add 10.', points=5),
            Question(quiz_id=num8.id, text='What is 10 less than 40?', option_a='20', option_b='25', option_c='30', option_d='50', correct_answer='C', explanation='40 - 10 = 30!', hint='Subtract 10.', points=5),
            Question(quiz_id=num8.id, text='Which number is odd?', option_a='10', option_b='12', option_c='13', option_d='14', correct_answer='C', explanation='13 is odd (can\'t be split evenly)!', hint='Ends in 1, 3, 5, 7, 9.', points=5),
            Question(quiz_id=num8.id, text='Which number is even?', option_a='11', option_b='15', option_c='18', option_d='21', correct_answer='C', explanation='18 is even (can be split in half)!', hint='Ends in 0, 2, 4, 6, 8.', points=5),
        ])

    num9 = add_quiz_if_missing('Shapes & Counting', '123', 'easy', 'Count shapes!')
    if num9:
        add_questions_if_missing(num9, [
            Question(quiz_id=num9.id, text='How many sides does a triangle have?', option_a='2', option_b='3', option_c='4', option_d='5', correct_answer='B', explanation='A triangle has 3 sides!', hint='Tri-angle.', points=5),
            Question(quiz_id=num9.id, text='How many sides does a square have?', option_a='3', option_b='4', option_c='5', option_d='6', correct_answer='B', explanation='A square has 4 equal sides!', hint='Four corners.', points=5),
            Question(quiz_id=num9.id, text='How many corners does a circle have?', option_a='0', option_b='1', option_c='2', option_d='4', correct_answer='A', explanation='A circle has 0 corners!', hint='Round and smooth.', points=5),
            Question(quiz_id=num9.id, text='How many eggs in a dozen?', option_a='10', option_b='11', option_c='12', option_d='13', correct_answer='C', explanation='A dozen is 12!', hint='One dozen.', points=5),
            Question(quiz_id=num9.id, text='How many wheels on a bicycle?', option_a='1', option_b='2', option_c='3', option_d='4', correct_answer='B', explanation='A bicycle has 2 wheels!', hint='Bi-cycle.', points=5),
            Question(quiz_id=num9.id, text='How many legs does a spider have?', option_a='6', option_b='8', option_c='10', option_d='4', correct_answer='B', explanation='A spider has 8 legs!', hint='More than insects.', points=5),
            Question(quiz_id=num9.id, text='How many months in a year?', option_a='10', option_b='11', option_c='12', option_d='13', correct_answer='C', explanation='There are 12 months in a year!', hint='One year.', points=5),
        ])

    num10 = add_quiz_if_missing('Tally & Place Value', '123', 'hard', 'Understanding numbers!')
    if num10:
        add_questions_if_missing(num10, [
            Question(quiz_id=num10.id, text='How many tens in 45?', option_a='4', option_b='5', option_c='45', option_d='9', correct_answer='A', explanation='45 has 4 tens and 5 ones!', hint='The tens digit.', points=10),
            Question(quiz_id=num10.id, text='How many ones in 38?', option_a='3', option_b='8', option_c='38', option_d='11', correct_answer='B', explanation='38 has 3 tens and 8 ones!', hint='The ones digit.', points=10),
            Question(quiz_id=num10.id, text='What is 6 tens + 3 ones?', option_a='36', option_b='63', option_c='60', option_d='30', correct_answer='B', explanation='6 tens = 60, 3 ones = 3, total 63!', hint='60 + 3 = ?', points=10),
            Question(quiz_id=num10.id, text='What is 100 - 1?', option_a='98', option_b='99', option_c='100', option_d='101', correct_answer='B', explanation='100 - 1 = 99!', hint='One less than 100.', points=10),
            Question(quiz_id=num10.id, text='Count: 96, 97, 98, __?', option_a='99', option_b='100', option_c='97', option_d='101', correct_answer='A', explanation='99 comes after 98!', hint='Before 100.', points=10),
            Question(quiz_id=num10.id, text='What is half of 20?', option_a='5', option_b='8', option_c='10', option_d='12', correct_answer='C', explanation='Half of 20 is 10!', hint='20 split into 2 groups.', points=10),
            Question(quiz_id=num10.id, text='How many days in a week?', option_a='5', option_b='6', option_c='7', option_d='8', correct_answer='C', explanation='There are 7 days in a week!', hint='Monday to Sunday.', points=5),
        ])

    print("  Additional questions seeded successfully!")
