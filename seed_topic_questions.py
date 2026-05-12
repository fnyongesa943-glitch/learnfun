"""Seed quizzes with questions linked to every CBC topic."""
from models import Subject, Topic, Quiz, Question, db


def seed_topic_questions():
    """Add quizzes with questions for every CBC subject topic."""

    def make_quiz(topic, title, diff, desc, questions):
        existing = Quiz.query.filter_by(title=title, topic_id=topic.id).first()
        if existing:
            return
        quiz = Quiz(
            title=title, subject_id=topic.subject_id,
            difficulty=diff, description=desc,
            topic_id=topic.id, grade_id=topic.grade_id
        )
        db.session.add(quiz)
        db.session.flush()
        for q in questions:
            db.session.add(Question(quiz_id=quiz.id, **q))
        db.session.commit()

    def q(text, a, b, c, d, correct, explanation='', hint='', points=10):
        return {'text': text, 'option_a': a, 'option_b': b, 'option_c': c, 'option_d': d,
                'correct_answer': correct, 'explanation': explanation, 'hint': hint, 'points': points}

    subjects = {s.name: s for s in Subject.query.all()}
    topics = Topic.query.all()
    topic_map = {(t.subject_id, t.title): t for t in topics}

    # ============================================================
    # MATHEMATICS
    # ============================================================
    if 'Mathematics' in subjects:
        m = subjects['Mathematics']

        # Number Recognition
        t = topic_map.get((m.id, 'Number Recognition'))
        if t:
            make_quiz(t, 'Numbers 1-10 Quiz', 'easy', 'Count and identify numbers 1 to 10', [
                q('How many apples are 2 + 1?', '2', '3', '4', '5', 'B', '2 + 1 = 3!', 'Count: 2, then 1 more.', 5),
                q('What number comes after 3?', '2', '4', '5', '6', 'B', '4 comes after 3!', '1,2,3,?', 5),
                q('How many fingers on one hand?', '4', '5', '6', '3', 'B', 'We have 5 fingers on one hand!', 'Count your fingers.', 5),
                q('What number is 2 + 2?', '3', '4', '5', '6', 'B', '2 + 2 = 4!', 'Double 2.', 5),
                q('What number comes before 5?', '3', '4', '6', '7', 'B', '4 comes before 5!', '?, 5.', 5),
                q('Count: 6, 7, 8, __?', '7', '8', '9', '10', 'C', '9 comes after 8!', '8, then?', 5),
                q('How many legs does a cat have?', '2', '3', '4', '5', 'C', 'A cat has 4 legs!', 'Count cat legs.', 5),
                q('What number is 5 + 0?', '0', '5', '10', '1', 'B', '5 + 0 = 5!', 'Adding zero changes nothing.', 5),
                q('What is the biggest number: 2, 5, 1?', '1', '2', '5', '3', 'C', '5 is the biggest!', 'Which is most?', 5),
                q('How many eyes do you have?', '1', '2', '3', '4', 'B', 'You have 2 eyes!', 'Look and see.', 5),
            ])

        # Addition and Subtraction
        t = topic_map.get((m.id, 'Addition and Subtraction'))
        if t:
            make_quiz(t, 'Add & Subtract', 'easy', 'Practice adding and taking away', [
                q('3 + 2 = ?', '4', '5', '6', '7', 'B', '3 + 2 = 5!', 'Count: 3,4,5.', 5),
                q('5 - 1 = ?', '3', '4', '5', '6', 'B', '5 - 1 = 4!', 'One less than 5.', 5),
                q('4 + 3 = ?', '6', '7', '8', '9', 'B', '4 + 3 = 7!', '4 and 3 more.', 5),
                q('6 - 2 = ?', '3', '4', '5', '2', 'B', '6 - 2 = 4!', 'Count back 2 from 6.', 5),
                q('2 + 5 = ?', '6', '7', '8', '9', 'B', '2 + 5 = 7!', 'Start at 2, add 5.', 5),
                q('8 - 3 = ?', '4', '5', '6', '7', 'B', '8 - 3 = 5!', '8 take away 3.', 5),
                q('1 + 1 = ?', '1', '2', '3', '4', 'B', '1 + 1 = 2!', 'One and one more.', 5),
                q('7 - 4 = ?', '2', '3', '4', '5', 'B', '7 - 4 = 3!', '4 less than 7.', 5),
                q('0 + 6 = ?', '0', '5', '6', '7', 'C', '0 + 6 = 6!', 'Adding zero.', 5),
                q('9 - 5 = ?', '3', '4', '5', '6', 'B', '9 - 5 = 4!', '5 from 9.', 5),
            ])

        # Numbers up to 100
        t = topic_map.get((m.id, 'Numbers up to 100'))
        if t:
            make_quiz(t, 'Numbers to 100', 'medium', 'Counting and place value up to 100', [
                q('What comes after 29?', '28', '30', '31', '20', 'B', '30 comes after 29!', 'Twenty-nine, then?', 5),
                q('How many tens in 54?', '4', '5', '54', '9', 'B', '54 has 5 tens!', 'The tens digit.', 10),
                q('What number is 7 tens and 3 ones?', '37', '73', '70', '30', 'B', '70 + 3 = 73!', '7 tens = 70.', 10),
                q('Count by 10s: 10, 20, 30, __?', '25', '35', '40', '50', 'C', '30 + 10 = 40!', 'Add 10.', 5),
                q('What comes before 50?', '48', '49', '51', '40', 'B', '49 comes before 50!', 'One less than 50.', 5),
                q('Which is bigger: 67 or 76?', '67', '76', 'Same', 'Neither', 'B', '76 is bigger than 67!', 'Compare tens digit.', 10),
                q('How many ones in 82?', '8', '2', '82', '80', 'B', '82 has 2 ones!', 'The ones digit.', 10),
                q('Count: 45, 50, 55, __?', '56', '60', '65', '70', 'B', '55 + 5 = 60!', 'Skip count by 5s.', 5),
                q('What number has 9 tens and 9 ones?', '90', '99', '19', '100', 'B', '99!', '9 tens = 90 + 9.', 10),
                q('Count backwards: 100, 99, 98, __?', '96', '97', '95', '100', 'B', '97 comes after 98!', 'One less.', 5),
            ])

        # Shapes and Patterns
        t = topic_map.get((m.id, 'Shapes and Patterns'))
        if t:
            make_quiz(t, 'Shapes & Patterns', 'easy', 'Identify shapes and make patterns', [
                q('How many sides does a square have?', '3', '4', '5', '6', 'B', 'A square has 4 sides!', 'Count the sides.', 5),
                q('How many sides does a triangle have?', '3', '4', '5', '6', 'A', 'A triangle has 3 sides!', 'Tri-angle.', 5),
                q('What shape has no corners?', 'square', 'triangle', 'circle', 'rectangle', 'C', 'A circle has no corners!', 'Round shape.', 5),
                q('Complete: ○□○□○__?', '○', '□', '△', '☆', 'B', 'The pattern is circle, square!', 'What comes next?', 10),
                q('How many corners does a rectangle have?', '3', '4', '5', '0', 'B', 'A rectangle has 4 corners!', 'Like a door.', 5),
                q('A pattern repeats. What comes next: ●○●○●?', '●', '○', '●○', '○●', 'B', 'The pattern is black, white!', 'Look at the repeat.', 10),
                q('What shape is like an egg?', 'circle', 'square', 'oval', 'triangle', 'C', 'An oval is like a stretched circle!', 'Not round.', 5),
                q('How many sides does a pentagon have?', '4', '5', '6', '3', 'B', 'A pentagon has 5 sides!', 'Penta = 5.', 10),
                q('What shape has 6 sides?', 'pentagon', 'hexagon', 'octagon', 'square', 'B', 'A hexagon has 6 sides!', 'Hexa = 6.', 10),
                q('Count the pattern: 1, 2, 1, 2, __?', '1', '2', '3', '0', 'A', 'The pattern is 1, 2, repeat!', '1, 2, then?', 5),
            ])

        # Multiplication Basics
        t = topic_map.get((m.id, 'Multiplication Basics'))
        if t:
            make_quiz(t, 'Multiplication', 'medium', 'Introduction to times tables', [
                q('2 × 3 = ?', '5', '6', '7', '8', 'B', '2 × 3 = 6 (2 groups of 3)!', '2 + 2 + 2 = 6.', 10),
                q('5 × 2 = ?', '7', '8', '10', '12', 'C', '5 × 2 = 10!', '5 + 5 = 10.', 10),
                q('4 × 1 = ?', '1', '4', '5', '8', 'B', 'Any number × 1 = itself!', '1 group of 4.', 5),
                q('10 × 3 = ?', '13', '30', '20', '33', 'B', '10 × 3 = 30!', '10 + 10 + 10 = 30.', 10),
                q('3 × 0 = ?', '3', '1', '0', '30', 'C', 'Any number × 0 = 0!', '0 groups of 3.', 5),
                q('2 × 5 = ?', '7', '8', '9', '10', 'D', '2 × 5 = 10!', 'Double 5.', 10),
                q('3 × 3 = ?', '6', '9', '12', '3', 'B', '3 × 3 = 9!', '3 groups of 3.', 10),
                q('4 × 2 = ?', '6', '8', '10', '12', 'B', '4 × 2 = 8!', '4 + 4 = 8.', 10),
                q('5 × 5 = ?', '10', '15', '20', '25', 'D', '5 × 5 = 25!', '5 groups of 5.', 10),
                q('2 × 10 = ?', '12', '20', '10', '22', 'B', '2 × 10 = 20!', 'Double 10.', 10),
            ])

        # Fractions
        t = topic_map.get((m.id, 'Fractions'))
        if t:
            make_quiz(t, 'Fractions', 'medium', 'Understanding parts of a whole', [
                q('Half of 8 is?', '3', '4', '5', '6', 'B', 'Half of 8 is 4!', '8 split into 2 groups.', 10),
                q('1/4 of 12 = ?', '2', '3', '4', '6', 'B', '1/4 of 12 = 3!', '12 ÷ 4 = ?', 10),
                q('Which is bigger: 1/2 or 1/3?', '1/2', '1/3', 'Same', 'Neither', 'A', '1/2 is bigger than 1/3!', 'Half is more than a third.', 10),
                q('How many quarters make a whole?', '2', '3', '4', '5', 'C', '4 quarters make a whole!', '4/4 = 1.', 10),
                q('2/4 is the same as?', '1/4', '1/3', '1/2', '2/3', 'C', '2/4 = 1/2!', 'Simplify by dividing by 2.', 10),
                q('What fraction is shaded if 3 of 4 parts are colored?', '1/4', '2/4', '3/4', '4/4', 'C', '3 out of 4 = 3/4!', 'Count colored parts.', 10),
                q('What is 1/2 of 10?', '3', '4', '5', '6', 'C', 'Half of 10 is 5!', '10 ÷ 2 = ?', 10),
                q('Which is smaller: 1/4 or 1/8?', '1/4', '1/8', 'Same', 'Neither', 'B', '1/8 is smaller than 1/4!', 'More pieces = smaller parts.', 10),
                q('How many halves in a whole?', '1', '2', '3', '4', 'B', 'There are 2 halves in a whole!', '1/2 + 1/2 = 1.', 10),
                q('1/10 of 20 = ?', '1', '2', '4', '10', 'B', '1/10 of 20 = 2!', '20 ÷ 10 = ?', 10),
            ])

    # ============================================================
    # ENGLISH
    # ============================================================
    if 'English' in subjects:
        e = subjects['English']

        t = topic_map.get((e.id, 'Alphabet and Phonics'))
        if t:
            make_quiz(t, 'Alphabet & Phonics', 'easy', 'Letters and their sounds', [
                q('How many letters in the English alphabet?', '24', '25', '26', '27', 'C', 'There are 26 letters!', 'A to Z.', 5),
                q('What letter comes after M?', 'L', 'N', 'O', 'K', 'B', 'N comes after M!', 'L, M, N.', 5),
                q('Which is a vowel?', 'B', 'C', 'E', 'F', 'C', 'E is a vowel!', 'A, E, I, O, U.', 5),
                q('What sound does B make?', '/k/', '/b/', '/d/', '/p/', 'B', 'B says /b/ like ball!', 'Ball starts with B.', 5),
                q('What letter comes before P?', 'O', 'Q', 'R', 'N', 'A', 'O comes before P!', 'N, O, P.', 5),
                q('How many vowels in English?', '3', '4', '5', '6', 'C', '5 vowels: A, E, I, O, U!', 'A-E-I-O-U.', 5),
                q('What is the first letter of "elephant"?', 'A', 'E', 'I', 'O', 'B', 'Elephant starts with E!', '🐘', 5),
                q('What is the last letter of the alphabet?', 'X', 'Y', 'Z', 'W', 'C', 'Z is the last letter!', '🦓.', 5),
                q('Which word starts with the same sound as "kite"?', 'cat', 'dog', 'sun', 'ball', 'A', 'Cat and kite both start with /k/!', 'C and K make same sound.', 5),
                q('How many letters in "sun"?', '2', '3', '4', '5', 'B', 'S-U-N = 3 letters!', 'Count the letters.', 5),
            ])

        t = topic_map.get((e.id, 'Simple Words and Sentences'))
        if t:
            make_quiz(t, 'Simple Words', 'easy', 'Read and write basic words', [
                q('Spell "cat":', 'c-a-t', 'c-o-t', 'k-a-t', 'c-u-t', 'A', 'C-A-T spells cat!', '🐱', 5),
                q('Which word is a color?', 'dog', 'red', 'run', 'big', 'B', 'Red is a color!', '🔴', 5),
                q('Read: d-o-g', 'cat', 'dog', 'dig', 'dug', 'B', 'd-o-g spells dog!', '🐕', 5),
                q('Which is a CVC word?', 'cat', 'cats', 'catch', 'cater', 'A', 'Cat is CVC (Consonant-Vowel-Consonant)!', '3 letters.', 5),
                q('What word does "h-e-n" make?', 'hen', 'men', 'pen', 'ten', 'A', 'h-e-n = hen!', '🐔', 5),
                q('What word is opposite of "hot"?', 'warm', 'cold', 'big', 'fast', 'B', 'Cold is opposite of hot!', 'Winter is ___.', 10),
                q('Which word has the short "a" sound?', 'cake', 'cat', 'cute', 'cold', 'B', 'Cat has the short a sound!', '/a/ as in apple.', 5),
                q('Complete: The ___ shines bright.', 'moon', 'star', 'sun', 'light', 'C', 'The sun shines bright!', '☀️', 5),
                q('Which is a sentence?', 'the dog', 'dog runs', 'The dog runs.', 'dog the', 'C', 'A sentence starts with capital and ends with period!', 'Complete thought.', 10),
                q('What does "b-e-d" spell?', 'bad', 'bed', 'bid', 'bud', 'B', 'b-e-d = bed!', '🛏️', 5),
            ])

        t = topic_map.get((e.id, 'Building Sentences'))
        if t:
            make_quiz(t, 'Building Sentences', 'easy', 'Writing complete sentences', [
                q('What must a sentence start with?', 'a number', 'capital letter', 'small letter', 'a symbol', 'B', 'A sentence starts with a capital letter!', 'Like "The".', 10),
                q('What comes at the end of a sentence?', 'comma', 'period', 'question mark', 'exclamation', 'B', 'A sentence ends with a period!', '.', 10),
                q('Find the noun: "The girl sings."', 'girl', 'sings', 'the', 'The', 'A', 'Girl is the noun (person)!', 'Who is doing?', 10),
                q('Find the verb: "Birds fly."', 'Birds', 'fly', 'Birds fly', 'none', 'B', 'Fly is the verb (action)!', 'What do birds do?', 10),
                q('Which is a complete sentence?', 'The boy', 'runs fast', 'The boy runs fast.', 'fast runs', 'C', 'It has a subject and verb!', 'Complete thought.', 10),
                q('Which word is a noun?', 'run', 'beautiful', 'cat', 'quickly', 'C', 'Cat is a noun (thing)!', '😺', 5),
                q('Which word is a verb?', 'table', 'happy', 'jump', 'blue', 'C', 'Jump is a verb (action)!', '🤾', 5),
                q('Make this a sentence: "the dog"', 'the dog.', 'the dog runs.', 'dog the', 'The dog is', 'B', 'Add a verb to complete it!', 'Subject + verb.', 10),
                q('Is "The cat sleeps" a sentence?', 'Yes', 'No', 'Maybe', 'Not sure', 'A', 'Yes - it has a noun and verb!', 'Complete thought.', 5),
                q('Nouns name:', 'actions', 'people/places/things', 'sounds', 'colors', 'B', 'Nouns name people, places, and things!', 'Person, place, thing.', 5),
            ])

    # ============================================================
    # KISWAHILI
    # ============================================================
    if 'Kiswahili' in subjects:
        k = subjects['Kiswahili']

        t = topic_map.get((k.id, 'Herufi za Alfabeti'))
        if t:
            make_quiz(t, 'Herufi za Alfabeti', 'easy', 'Kujifunza herufi za Kiswahili', [
                q('Kiswahili kina herufi ngapi?', '24', '25', '26', '27', 'C', 'Kiswahili kina herufi 26!', 'A-Z.', 5),
                q('Herufi ya kwanza ni?', 'A', 'B', 'C', 'D', 'A', 'Herufi A ndiyo ya kwanza!', 'Alfabeti huanza na A.', 5),
                q('Neno "Baba" linaanza na herufi gani?', 'A', 'B', 'C', 'D', 'B', 'Baba linaanza na B!', 'B-baba.', 5),
                q('Vokali za Kiswahili ni?', 'a,b,c,d', 'a,e,i,o,u', 'a,b,i,o,u', 'e,i,o,u,y', 'B', 'Vokali ni a,e,i,o,u!', 'Husaidia kutamka.', 5),
                q('Herufi gani inakuja baada ya L?', 'K', 'M', 'N', 'O', 'B', 'M inakuja baada ya L!', 'K, L, M.', 5),
                q('Neno "Nyumba" linaanza na herufi gani?', 'N', 'Ny', 'M', 'Y', 'B', 'Nyumba linaanza na herufi Ny!', 'Ny ni herufi moja.', 10),
                q('Herufi ya mwisho ya alfabeti ni?', 'X', 'Y', 'Z', 'W', 'C', 'Z ndiyo herufi ya mwisho!', 'Mwisho wa alfabeti.', 5),
                q('Neno "Mama" linaanza na herufi?', 'M', 'N', 'L', 'K', 'A', 'Mama linaanza na M!', 'Mama.', 5),
                q('Herufi gani ni vokali: ___, E, I, O, U?', 'A', 'B', 'C', 'D', 'A', 'A ni vokali!', 'Vokali za kwanza.', 5),
                q('Neno "Rafiki" linaanza na herufi?', 'R', 'F', 'K', 'D', 'A', 'Rafiki linaanza na R!', 'R ni herufi.', 5),
            ])

    # ============================================================
    # SCIENCE & TECHNOLOGY
    # ============================================================
    if 'Science & Technology' in subjects:
        st = subjects['Science & Technology']

        t = topic_map.get((st.id, 'Living and Non-Living Things'))
        if t:
            make_quiz(t, 'Living & Non-Living', 'easy', 'What is alive and what is not', [
                q('Which is a living thing?', 'rock', 'tree', 'water', 'chair', 'B', 'A tree is living - it grows!', '🌳', 5),
                q('Which is NOT a living thing?', 'dog', 'fish', 'table', 'flower', 'C', 'A table is non-living!', 'Does it grow?', 5),
                q('Living things need:', 'food and water', 'only food', 'only water', 'nothing', 'A', 'Living things need food and water!', 'Survival needs.', 10),
                q('Do plants grow?', 'Yes', 'No', 'Sometimes', 'Never', 'A', 'Yes! Plants grow from seeds!', '🌱', 5),
                q('A rock is:', 'living', 'non-living', 'once alive', 'growing', 'B', 'A rock is non-living!', 'Does it eat?', 5),
                q('Which animal lives in water?', 'lion', 'fish', 'bird', 'dog', 'B', 'Fish live in water!', '🐟', 5),
                q('All living things:', 'grow and change', 'stay the same', 'are big', 'are fast', 'A', 'Living things grow and change!', 'From baby to adult.', 10),
                q('Which is a non-living thing?', 'cat', 'butterfly', 'pencil', 'grass', 'C', 'A pencil is non-living!', '✏️', 5),
                q('Do all living things eat food?', 'Yes', 'No', 'Some', 'Never', 'A', 'Yes! All living things need food for energy!', 'Food = energy.', 5),
                q('Which is alive?', 'toy car', 'TV', 'apple tree', 'book', 'C', 'An apple tree is alive!', '🍎', 5),
            ])

        t = topic_map.get((st.id, 'The Human Body'))
        if t:
            make_quiz(t, 'The Human Body', 'medium', 'Our amazing body systems', [
                q('How many bones in an adult body?', '106', '206', '306', '156', 'B', '206 bones!', 'About 200.', 10),
                q('Which organ pumps blood?', 'brain', 'heart', 'lungs', 'liver', 'B', 'The heart pumps blood!', '❤️', 5),
                q('What do lungs help us do?', 'think', 'breathe', 'digest', 'move', 'B', 'Lungs help us breathe!', '💨', 5),
                q('Which system breaks down food?', 'skeletal', 'muscular', 'digestive', 'nervous', 'C', 'The digestive system breaks down food!', '🫃', 10),
                q('What protects our organs?', 'muscles', 'bones', 'skin', 'blood', 'B', 'Bones protect our organs!', '🦴', 10),
                q('The brain is part of which system?', 'skeletal', 'digestive', 'nervous', 'muscular', 'C', 'The brain is part of the nervous system!', '🧠', 10),
                q('How many muscles in the body?', '200+', '400+', '600+', '800+', 'C', 'Over 600 muscles!', '💪', 10),
                q('What does your heart do?', 'helps breathing', 'pumps blood', 'digests food', 'thinks', 'B', 'Your heart pumps blood all over your body!', 'Thump-thump.', 5),
                q('Which helps us move?', 'bones only', 'muscles only', 'muscles and bones', 'skin only', 'C', 'Muscles and bones work together to move!', '💪 + 🦴', 10),
                q('How many senses do humans have?', '3', '4', '5', '6', 'C', 'We have 5 senses!', 'See, hear, touch, taste, smell.', 10),
            ])

    # ============================================================
    # CRE
    # ============================================================
    if 'CRE' in subjects:
        cre = subjects['CRE']

        t = topic_map.get((cre.id, "God's Creation"))
        if t:
            make_quiz(t, "God's Creation", 'easy', 'Learning about God\'s wonderful world', [
                q('How many days did God take to create the world?', '5', '6', '7', '8', 'C', 'God created in 7 days and rested on the 7th!', 'Genesis.', 5),
                q('What did God make on day 1?', 'animals', 'light', 'plants', 'stars', 'B', 'God made light on day 1!', '🌞', 5),
                q('What did God make on day 4?', 'fish', 'land', 'sun, moon, stars', 'people', 'C', 'God made the sun, moon, and stars!', '🌟', 10),
                q('On which day did God make animals?', 'day 4', 'day 5', 'day 6', 'day 7', 'C', 'God made animals on day 6!', '🦁🐘🐒', 10),
                q('What did God do on day 7?', 'worked', 'rested', 'played', 'slept', 'B', 'God rested on the 7th day!', '😌', 5),
                q('Who did God make in His own image?', 'animals', 'angels', 'people', 'trees', 'C', 'God made people (Adam and Eve) in His image!', '👫', 10),
                q('What did God say about His creation?', 'it was okay', 'it was very good', 'it was bad', 'nothing', 'B', 'God said it was "very good"!', '😊', 5),
                q('Where is the creation story?', 'Exodus', 'Genesis', 'Psalms', 'Leviticus', 'B', 'The creation story is in Genesis!', 'First book of Bible.', 10),
                q('Who cares for God\'s creation?', 'only angels', 'everyone', 'only adults', 'no one', 'B', 'Everyone should care for God\'s creation!', 'We are stewards.', 5),
                q('How can we care for the earth?', 'litter', 'plant trees', 'waste water', 'cut trees', 'B', 'Planting trees helps care for the earth!', '🌳', 5),
            ])

        t = topic_map.get((cre.id, 'Moses and the Israelites'))
        if t:
            make_quiz(t, 'Moses & Israelites', 'medium', 'God leads His people', [
                q('Who was Moses\' sister?', 'Sarah', 'Miriam', 'Rebecca', 'Leah', 'B', 'Miriam was Moses\' sister!', 'She watched him.', 10),
                q('What was Moses put in as a baby?', 'boat', 'basket', 'box', 'bag', 'B', 'Moses was placed in a basket on the Nile!', '🚣', 5),
                q('Who found baby Moses?', 'Pharaoh', 'Pharaoh\'s daughter', 'a slave', 'a soldier', 'B', 'Pharaoh\'s daughter found him!', '👸', 5),
                q('How many plagues did God send?', '5', '7', '10', '12', 'C', 'God sent 10 plagues to Egypt!', '⚠️', 10),
                q('Who refused to let the Israelites go?', 'Moses', 'Pharaoh', 'Aaron', 'Joshua', 'B', 'Pharaoh refused!', 'King of Egypt.', 5),
                q('What was the last plague?', 'frogs', 'darkness', 'death of firstborn', 'locusts', 'C', 'The 10th plague was the worst!', '😢', 10),
                q('What is Passover?', 'a holiday', 'when God protected His people', 'a river', 'a mountain', 'B', 'Passover is when the angel passed over Israelite homes!', '🩸', 10),
                q('Where were the Israelites enslaved?', 'Canaan', 'Egypt', 'Babylon', 'Rome', 'B', 'The Israelites were slaves in Egypt!', '🇪🇬', 5),
                q('What did God use to free His people?', 'swords', 'plagues', 'fire', 'flood', 'B', 'God used 10 plagues!', 'Moses and Aaron.', 10),
                q('What does "Moses" mean?', 'savior', 'leader', 'drawn out of water', 'prophet', 'C', 'Moses means "drawn out of water"!', 'From the Nile.', 10),
            ])

    # ============================================================
    # HYGIENE & NUTRITION
    # ============================================================
    if 'Hygiene & Nutrition' in subjects:
        hn = subjects['Hygiene & Nutrition']

        t = topic_map.get((hn.id, 'Personal Hygiene'))
        if t:
            make_quiz(t, 'Personal Hygiene', 'easy', 'Keep your body clean and healthy', [
                q('How often should you wash your hands?', 'once a day', 'before eating and after toilet', 'once a week', 'never', 'B', 'Wash hands before eating and after toilet!', '🧼', 5),
                q('How long should you wash your hands?', '5 seconds', '10 seconds', '20 seconds', '1 minute', 'C', 'Wash for about 20 seconds!', 'Sing the ABC song once.', 10),
                q('Why do we use soap?', 'smells nice', 'removes germs', 'makes bubbles', 'colors skin', 'B', 'Soap removes germs from our hands!', '🧼', 5),
                q('How many times a day should you brush teeth?', 'once', 'twice', 'three times', 'once a week', 'B', 'Brush twice a day - morning and night!', '🪥', 5),
                q('How long should you brush your teeth?', '30 seconds', '1 minute', '2 minutes', '5 minutes', 'C', 'Brush for 2 minutes!', '🪥', 10),
                q('What prevents cavities?', 'eating candy', 'brushing teeth', 'not brushing', 'drinking soda', 'B', 'Brushing teeth prevents cavities!', '🦷', 5),
                q('When should you visit the dentist?', 'only when hurt', 'once a year', 'twice a year', 'never', 'C', 'Visit the dentist twice a year!', '🦷', 10),
                q('What size toothpaste should you use?', 'full brush', 'pea-sized', 'half brush', 'none', 'B', 'Use a pea-sized amount of toothpaste!', 'Small amount.', 10),
                q('What is hygiene?', 'being clean', 'being fast', 'being loud', 'being tall', 'A', 'Hygiene means keeping clean and healthy!', '🧼', 5),
                q('What kills germs on hands?', 'water only', 'soap and water', 'towel only', 'air only', 'B', 'Soap and water together kill germs!', '🧼 + 💧', 5),
            ])

        t = topic_map.get((hn.id, 'Healthy Eating'))
        if t:
            make_quiz(t, 'Healthy Eating', 'easy', 'Foods that make us strong', [
                q('How many food groups are there?', '3', '4', '5', '6', 'C', 'There are 5 main food groups!', '🥛🥩🍞🥗🥜', 10),
                q('Which food gives energy?', 'milk', 'rice (carbohydrates)', 'meat', 'fruit', 'B', 'Carbohydrates like rice give energy!', '🍚', 5),
                q('What is good for strong bones?', 'candy', 'milk (calcium)', 'soda', 'chips', 'B', 'Milk has calcium for strong bones!', '🥛', 5),
                q('How many glasses of water daily?', '2-3', '4-5', '6-8', '10+', 'C', 'Drink 6-8 glasses of water daily!', '💧', 10),
                q('What food group helps muscles grow?', 'fruits', 'proteins', 'fats', 'sweets', 'B', 'Proteins help muscles grow and repair!', '🥩', 10),
                q('Why eat breakfast?', 'skip lunch', 'gives energy for the day', 'eat less dinner', 'save time', 'B', 'Breakfast gives you energy for the day!', '🌅', 5),
                q('What should a healthy plate look like?', '½ veg, ¼ carbs, ¼ protein', 'all meat', 'all rice', 'all sweets', 'A', 'Half veg, quarter carbs, quarter protein!', '🥗🍚🥩', 10),
                q('Which is a healthy snack?', 'chips', 'fruit', 'candy', 'soda', 'B', 'Fruit is a healthy snack!', '🍎', 5),
                q('What does vitamin A help with?', 'bones', 'eyesight', 'muscles', 'skin', 'B', 'Vitamin A helps your eyes see well!', '🥕', 10),
                q('Why limit sweets?', 'they are expensive', 'bad for teeth and health', 'too sweet', 'not tasty', 'B', 'Too much sugar is bad for teeth and health!', '🚫🍬', 5),
            ])

    # ============================================================
    # ENVIRONMENTAL
    # ============================================================
    if 'Environmental' in subjects:
        env = subjects['Environmental']

        t = topic_map.get((env.id, 'Keeping Our Environment Clean'))
        if t:
            make_quiz(t, 'Clean Environment', 'easy', 'Take care of our surroundings', [
                q('What should we do with rubbish?', 'throw on ground', 'put in bin', 'burn it', 'leave it', 'B', 'Put rubbish in the bin!', '🗑️', 5),
                q('What are the 3 Rs?', 'Run, Rest, Repeat', 'Reduce, Reuse, Recycle', 'Read, Write, Repeat', 'Red, Blue, Green', 'B', 'Reduce, Reuse, Recycle!', '♻️', 10),
                q('Why keep environment clean?', 'looks nice', 'stays healthy', 'both', 'neither', 'C', 'Clean environment looks nice AND keeps us healthy!', '🌍', 5),
                q('What can you do with banana peels?', 'throw away', 'make compost', 'burn', 'eat', 'B', 'Banana peels can become compost!', '🌱', 10),
                q('How long does plastic take to break down?', '1 year', '10 years', '450 years', '10 days', 'C', 'Plastic takes about 450 years!', '🚯', 10),
                q('What does "recycle" mean?', 'use once', 'make into new things', 'throw away', 'burn', 'B', 'Recycle means making old things into new things!', '♻️', 5),
                q('Why is litter dangerous?', 'looks bad', 'germs and injuries', 'smells', 'all of above', 'D', 'Litter causes all these problems!', '🚯', 10),
                q('What can be recycled?', 'food scraps', 'paper and plastic', 'banana peels', 'all of above', 'B', 'Paper and plastic can be recycled!', '📄🥫', 5),
                q('What does "compost" mean?', 'buying food', 'decayed organic matter for soil', 'a type of plastic', 'cleaning', 'B', 'Compost is decayed organic matter that feeds soil!', '🌱', 10),
                q('Who should keep the environment clean?', 'only adults', 'only children', 'everyone', 'government only', 'C', 'Everyone should help keep the environment clean!', '🤝', 5),
            ])

    # ============================================================
    # SOCIAL STUDIES
    # ============================================================
    if 'Social Studies' in subjects:
        ss = subjects['Social Studies']

        t = topic_map.get((ss.id, 'Our Country Kenya'))
        if t:
            make_quiz(t, 'Our Country Kenya', 'medium', 'Learning about Kenya', [
                q('What is the capital of Kenya?', 'Mombasa', 'Nairobi', 'Kisumu', 'Nakuru', 'B', 'Nairobi is the capital of Kenya!', '🏙️', 5),
                q('What is Kenya\'s national animal?', 'elephant', 'lion', 'giraffe', 'zebra', 'B', 'The lion is Kenya\'s national animal!', '🦁', 5),
                q('When is Jamhuri Day?', 'June 1', 'October 20', 'December 12', 'August 8', 'C', 'Jamhuri Day is December 12!', 'Independence day.', 10),
                q('What is Kenya\'s motto?', 'Peace and Love', 'Harambee', 'Unity', 'Forward', 'B', 'Harambee means "Let\'s all pull together"!', '🤝', 10),
                q('How many counties does Kenya have?', '27', '37', '47', '57', 'C', 'Kenya has 47 counties!', 'Each has a governor.', 10),
                q('Which ocean borders Kenya?', 'Atlantic', 'Pacific', 'Indian', 'Arctic', 'C', 'The Indian Ocean borders Kenya!', '🌊', 5),
                q('What are Kenya\'s official languages?', 'English and French', 'English and Kiswahili', 'Kiswahili and Arabic', 'English and Kikuyu', 'B', 'English and Kiswahili are official!', '🗣️', 10),
                q('What is Kenya\'s currency?', 'Shilling', 'Dollar', 'Pound', 'Euro', 'A', 'Kenyan Shilling (KSh)!', '💰', 5),
                q('Which mountain is Kenya named after?', 'Mt Kilimanjaro', 'Mt Kenya', 'Mt Elgon', 'Mt Longonot', 'B', 'Kenya is named after Mt Kenya!', '⛰️', 10),
                q('What does the black color on the flag represent?', 'peace', 'the people of Kenya', 'land', 'blood', 'B', 'Black represents the people of Kenya!', '🏴󠁫󠁥󠁮󠁡󠁿', 10),
            ])

    # ============================================================
    # AGRICULTURE
    # ============================================================
    if 'Agriculture' in subjects:
        ag = subjects['Agriculture']

        t = topic_map.get((ag.id, 'Growing Food'))
        if t:
            make_quiz(t, 'Growing Food', 'medium', 'How food is grown', [
                q('What does a plant need most to grow?', 'sunlight, water, soil', 'only water', 'only soil', 'only sunlight', 'A', 'Plants need sunlight, water, and soil!', '🌞💧🌱', 5),
                q('What tool is used to dig soil?', 'hammer', 'jembe', 'saw', 'brush', 'B', 'A jembe (hoe) is used to dig soil!', '⛏️', 5),
                q('Why add manure to soil?', 'smells good', 'adds nutrients', 'colors soil', 'kills weeds', 'B', 'Manure adds nutrients to the soil!', '💩', 10),
                q('When should you water plants?', 'noon', 'morning or evening', 'midnight', 'anytime', 'B', 'Water in the morning or evening!', '💧', 5),
                q('What is mulching?', 'cutting plants', 'covering soil with dry grass/leaves', 'planting seeds', 'watering', 'B', 'Mulch helps keep moisture in soil!', '🍂', 10),
                q('Why remove weeds?', 'they look bad', 'they compete for nutrients', 'they smell', 'they are tall', 'B', 'Weeds compete with crops for nutrients and water!', '🌿', 10),
                q('What vegetable grows well in Kenya?', 'sukuma wiki', 'iceberg lettuce', 'broccoli', 'artichoke', 'A', 'Sukuma wiki (kale) grows very well in Kenya!', '🥬', 5),
                q('What is agriculture?', 'cooking food', 'growing crops and raising animals', 'selling food', 'eating food', 'B', 'Agriculture means growing crops and raising animals!', '🌱', 5),
                q('Why use natural pest control?', 'cheaper only', 'safer for environment', 'faster', 'easier', 'B', 'Natural pest control is safer for the environment!', '🐛', 10),
                q('What does a seed need to sprout?', 'water and warmth', 'only light', 'only soil', 'only air', 'A', 'Seeds need water and warmth to sprout!', '🌱', 5),
            ])

    # ============================================================
    # CODING BASICS
    # ============================================================
    if 'Coding Basics' in subjects:
        cb = subjects['Coding Basics']

        t = topic_map.get((cb.id, 'What is Coding?'))
        if t:
            make_quiz(t, 'What is Coding?', 'medium', 'Introduction to programming', [
                q('What is coding?', 'playing games', 'giving instructions to computers', 'watching videos', 'typing fast', 'B', 'Coding means giving step-by-step instructions to computers!', '💻', 5),
                q('What is an algorithm?', 'a math problem', 'a step-by-step plan', 'a computer part', 'a game', 'B', 'An algorithm is a step-by-step plan to solve a problem!', '🧩', 10),
                q('Why is order important in code?', 'does not matter', 'steps must be in right order', 'faster only', 'looks better', 'B', 'The order of steps matters a lot in coding!', '🔢', 5),
                q('What is a sequence?', 'a random list', 'steps in the correct order', 'a jump', 'a loop', 'B', 'A sequence is steps in the correct order!', '1️⃣2️⃣3️⃣', 10),
                q('Who was the first computer programmer?', 'Charles Babbage', 'Ada Lovelace', 'Alan Turing', 'Bill Gates', 'B', 'Ada Lovelace was the first!', '👩‍💻', 10),
                q('What do apps and games use?', 'magic', 'code', 'paint', 'paper', 'B', 'All apps, games, and websites use code!', '📱', 5),
                q('Coding is like:', 'a recipe', 'a painting', 'a song', 'a dance', 'A', 'Coding is like following a recipe - step by step!', '📝', 5),
                q('What does a computer need?', 'exact instructions', 'guesses', 'opinions', 'feelings', 'A', 'Computers need exact, clear instructions!', '🤖', 5),
                q('Can anyone learn to code?', 'Yes', 'No', 'Only adults', 'Only experts', 'A', 'Anyone can learn to code!', '💻', 5),
                q('What comes from the word "algorithm"?', 'Greek philosopher', 'Al-Khwarizmi', 'Albert Einstein', 'Ada Lovelace', 'B', 'From the Persian mathematician Al-Khwarizmi!', '📜', 10),
            ])

    # ============================================================
    # HEALTH EDUCATION
    # ============================================================
    if 'Health Education' in subjects:
        he = subjects['Health Education']

        t = topic_map.get((he.id, 'Staying Healthy'))
        if t:
            make_quiz(t, 'Staying Healthy', 'easy', 'Keep your body strong and well', [
                q('How much exercise do kids need daily?', '20 minutes', '30 minutes', '60 minutes', '120 minutes', 'C', 'Kids need at least 60 minutes of activity daily!', '🏃', 10),
                q('Which is a benefit of exercise?', 'sore muscles only', 'strong heart and body', 'less sleep', 'more tired', 'B', 'Exercise gives you a strong heart and body!', '❤️', 5),
                q('What type of activity counts as exercise?', 'playing outside', 'watching TV', 'sitting', 'reading', 'A', 'Playing outside counts as exercise!', '🤸', 5),
                q('Exercise helps you:', 'sleep better', 'think better', 'both', 'neither', 'C', 'Exercise helps you sleep AND think better!', '😴🧠', 10),
                q('How does exercise make you feel?', 'sad', 'happy', 'angry', 'tired always', 'B', 'Exercise makes you happy!', '😊', 5),
                q('Which is exercise?', 'running', 'dancing', 'jumping', 'all of above', 'D', 'Running, dancing, and jumping are all exercise!', '🏃💃🤸', 5),
                q('What strengthens from exercise?', 'only legs', 'muscles and bones', 'only arms', 'only heart', 'B', 'Exercise strengthens muscles AND bones!', '💪🦴', 10),
                q('When is a good time to play outside?', 'after school', 'during meals', 'midnight', 'during class', 'A', 'After school is a great time for active play!', '🌳', 5),
                q('What sport can you play with friends?', 'football', 'video games', 'watching TV', 'reading', 'A', 'Football is a great sport to play with friends!', '⚽', 5),
                q('What does exercise do for your brain?', 'nothing', 'helps you think better in school', 'makes you tired', 'distracts you', 'B', 'Exercise helps you think better and focus in school!', '🧠', 10),
            ])

    # ============================================================
    # LIFE SKILLS
    # ============================================================
    if 'Life Skills' in subjects:
        ls = subjects['Life Skills']

        t = topic_map.get((ls.id, 'Values and Respect'))
        if t:
            make_quiz(t, 'Values and Respect', 'easy', 'Learning important values', [
                q('What is respect?', 'treating others well', 'being loud', 'ignoring people', 'being first', 'A', 'Respect means treating others the way you want to be treated!', '🤝', 5),
                q('What is the Golden Rule?', 'treat others as you want to be treated', 'be first', 'win always', 'eat fast', 'A', 'Treat others as you want to be treated!', '🥇', 10),
                q('How do you greet elders?', 'ignore them', 'say "Good morning" politely', 'shout', 'run away', 'B', 'Greet elders politely with "Good morning"!', '👋', 5),
                q('What should you say when someone gives you something?', 'give me', 'thank you', 'no', 'maybe', 'B', 'Always say "thank you"!', '🙏', 5),
                q('How do you show respect in class?', 'talk loudly', 'raise hand to speak', 'walk around', 'eat in class', 'B', 'Raise your hand to show respect to the teacher!', '✋', 5),
                q('What should you do if you hurt someone\'s feelings?', 'ignore it', 'apologize', 'laugh', 'blame them', 'B', 'Apologize when you hurt someone\'s feelings!', '😔', 5),
                q('What is bullying?', 'being kind', 'teasing or hurting others', 'sharing', 'helping', 'B', 'Bullying is teasing or hurting others on purpose!', '🚫', 10),
                q('How can you show respect at home?', 'help with chores', 'ignore parents', 'make noise', 'leave mess', 'A', 'Help with chores to show respect at home!', '🧹', 5),
                q('What does "sharing" mean?', 'keeping everything', 'letting others use things too', 'taking things', 'hiding things', 'B', 'Sharing means letting others use things too!', '🤲', 5),
                q('Respecting yourself means:', 'taking care of your body', 'eating only candy', 'never exercising', 'ignoring hygiene', 'A', 'Respecting yourself means taking care of your body!', '💚', 10),
            ])

    # ============================================================
    # CREATIVE ARTS
    # ============================================================
    if 'Creative Arts' in subjects:
        ca = subjects['Creative Arts']

        t = topic_map.get((ca.id, 'Drawing and Coloring'))
        if t:
            make_quiz(t, 'Drawing & Coloring', 'easy', 'Express yourself through art', [
                q('What basic shapes can you draw?', 'circle, square, triangle', 'only circles', 'only squares', 'only lines', 'A', 'Start with circles, squares, and triangles!', '🔴⬛🔺', 5),
                q('What shapes make a house?', 'circle and oval', 'square and triangle', 'triangle and star', 'circle and square', 'B', 'A house uses a square and triangle!', '🏠', 5),
                q('What is the most famous painting?', 'Starry Night', 'Mona Lisa', 'The Scream', 'Sunflowers', 'B', 'The Mona Lisa by Leonardo da Vinci!', '🎨', 10),
                q('What colors make green?', 'red and blue', 'blue and yellow', 'red and yellow', 'blue and green', 'B', 'Blue + Yellow = Green!', '🟢', 10),
                q('What should you practice to get better at drawing?', 'nothing', 'practice every day', 'only watch videos', 'copy once', 'B', 'Practice every day to improve your drawing!', '✏️', 5),
                q('What is a self-portrait?', 'painting of nature', 'painting of yourself', 'painting of food', 'painting of house', 'B', 'A self-portrait is a painting of yourself!', '🖼️', 10),
                q('What does "imagination" mean in art?', 'copying others', 'creating your own ideas', 'using only one color', 'drawing fast', 'B', 'Use your imagination to create unique art!', '💭', 5),
                q('What tool do you use for coloring?', 'hammer', 'crayons or pencils', 'scissors', 'glue', 'B', 'Use crayons, colored pencils, or markers!', '🖍️', 5),
                q('What shape is a star?', 'round', 'five-pointed', 'square', 'oval', 'B', 'A star has five points!', '⭐', 5),
                q('What can you draw with a circle?', 'sun, ball, face', 'only ball', 'only sun', 'only face', 'A', 'A circle can become a sun, ball, or face!', '☀️⚽😊', 5),
            ])

    print("  Topic-linked quizzes seeded successfully!")
