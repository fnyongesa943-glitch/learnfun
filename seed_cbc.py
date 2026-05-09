"""
CBC Curriculum Seed Data - Comprehensive learning content for Kenyan CBC system.
Covers Pre-Primary through Junior Secondary across all subject areas.
"""
import json
from datetime import datetime


GRADES = [
    {'name': 'Pre-Primary 1', 'level_code': 'PP1', 'category': 'Pre-Primary', 'icon': '🧸', 'color': '#F59E0B', 'sort_order': 1},
    {'name': 'Pre-Primary 2', 'level_code': 'PP2', 'category': 'Pre-Primary', 'icon': '🎨', 'color': '#F97316', 'sort_order': 2},
    {'name': 'Grade 1', 'level_code': 'G1', 'category': 'Lower Primary', 'icon': '📗', 'color': '#10B981', 'sort_order': 3},
    {'name': 'Grade 2', 'level_code': 'G2', 'category': 'Lower Primary', 'icon': '📘', 'color': '#14B8A6', 'sort_order': 4},
    {'name': 'Grade 3', 'level_code': 'G3', 'category': 'Lower Primary', 'icon': '📙', 'color': '#6366F1', 'sort_order': 5},
    {'name': 'Grade 4', 'level_code': 'G4', 'category': 'Upper Primary', 'icon': '📕', 'color': '#8B5CF6', 'sort_order': 6},
    {'name': 'Grade 5', 'level_code': 'G5', 'category': 'Upper Primary', 'icon': '📚', 'color': '#EC4899', 'sort_order': 7},
    {'name': 'Grade 6', 'level_code': 'G6', 'category': 'Upper Primary', 'icon': '📓', 'color': '#EF4444', 'sort_order': 8},
    {'name': 'Grade 7', 'level_code': 'G7', 'category': 'Junior Secondary', 'icon': '📐', 'color': '#3B82F6', 'sort_order': 9},
    {'name': 'Grade 8', 'level_code': 'G8', 'category': 'Junior Secondary', 'icon': '🔬', 'color': '#06B6D4', 'sort_order': 10},
    {'name': 'Grade 9', 'level_code': 'G9', 'category': 'Junior Secondary', 'icon': '⚡', 'color': '#7C3AED', 'sort_order': 11},
]

SUBJECTS = [
    {'name': 'Mathematics', 'icon': '🔢', 'color': '#6366F1', 'description': 'Numbers, shapes, measurements and problem solving', 'category': 'Core'},
    {'name': 'English', 'icon': '📖', 'color': '#EC4899', 'description': 'Reading, writing, grammar and communication skills', 'category': 'Core'},
    {'name': 'Kiswahili', 'icon': '🗣️', 'color': '#14B8A6', 'description': 'Kusoma, kuandika na kuzungumza Kiswahili', 'category': 'Core'},
    {'name': 'Science & Technology', 'icon': '🔬', 'color': '#10B981', 'description': 'Scientific inquiry, technology and innovation', 'category': 'Core'},
    {'name': 'Social Studies', 'icon': '🌍', 'color': '#F59E0B', 'description': 'Community, environment and citizenship', 'category': 'Core'},
    {'name': 'CRE', 'icon': '⛪', 'color': '#8B5CF6', 'description': 'Christian Religious Education', 'category': 'Religious'},
    {'name': 'IRE', 'icon': '🕌', 'color': '#06B6D4', 'description': 'Islamic Religious Education', 'category': 'Religious'},
    {'name': 'Agriculture', 'icon': '🌱', 'color': '#84CC16', 'description': 'Farming, gardening and food production', 'category': 'Core'},
    {'name': 'Home Science', 'icon': '🍳', 'color': '#F97316', 'description': 'Cooking, sewing and home management', 'category': 'Core'},
    {'name': 'Creative Arts', 'icon': '🎨', 'color': '#EC4899', 'description': 'Art, music, drama and creative expression', 'category': 'Creative'},
    {'name': 'Music', 'icon': '🎵', 'color': '#F472B6', 'description': 'Singing, instruments and musical appreciation', 'category': 'Creative'},
    {'name': 'Hygiene & Nutrition', 'icon': '🧼', 'color': '#0EA5E9', 'description': 'Personal hygiene, healthy eating and wellness', 'category': 'Life Skills'},
    {'name': 'Environmental', 'icon': '🌿', 'color': '#22C55E', 'description': 'Environmental conservation and awareness', 'category': 'Life Skills'},
    {'name': 'Health Education', 'icon': '💪', 'color': '#EF4444', 'description': 'Physical health, safety and disease prevention', 'category': 'Life Skills'},
    {'name': 'Life Skills', 'icon': '🤝', 'color': '#A855F7', 'description': 'Social skills, values and personal development', 'category': 'Life Skills'},
    {'name': 'Coding Basics', 'icon': '💻', 'color': '#3B82F6', 'description': 'Introduction to programming and computational thinking', 'category': 'Creative'},
    {'name': 'Art & Craft', 'icon': '✂️', 'color': '#F43F5E', 'description': 'Drawing, painting, modeling and handwork', 'category': 'Creative'},
]


def seed_grades(db, Grade):
    for g in GRADES:
        if not Grade.query.filter_by(level_code=g['level_code']).first():
            db.session.add(Grade(**g))
    db.session.commit()
    return {g.level_code: g for g in Grade.query.all()}


def seed_subjects(db, Subject):
    for s in SUBJECTS:
        if not Subject.query.filter_by(name=s['name']).first():
            db.session.add(Subject(**s))
    db.session.commit()
    return {s.name: s for s in Subject.query.all()}


def seed_cbc_content(db, Grade, Subject, Topic, Lesson):
    grades = {g.level_code: g for g in Grade.query.all()}
    subjects = {s.name: s for s in Subject.query.all()}

    content = []

    # ============================================================
    # MATHEMATICS
    # ============================================================
    if 'Mathematics' in subjects:
        m = subjects['Mathematics']

        # Grade 1 Mathematics
        if 'G1' in grades:
            content.append({
                'subject': m, 'grade': grades['G1'],
                'topic_title': 'Number Recognition', 'topic_icon': '🔢', 'topic_subtitle': 'Learning numbers 1 to 50',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Numbers 1 to 10', 'emoji': '1️⃣', 'order': 1,
                     'content': '''Numbers help us count things. Today we will learn numbers from 1 to 10.

Let's count together:
1 - One  (🍎 one apple)
2 - Two  (🍎🍎 two apples)
3 - Three (🍎🍎🍎 three apples)
4 - Four
5 - Five
6 - Six
7 - Seven
8 - Eight
9 - Nine
10 - Ten

When you count, say each number in order. Practice counting objects around you!''',
                     'key_points': json.dumps([
                         'Numbers 1-10 help us count things',
                         'Each number represents a quantity',
                         'Count in order: 1,2,3,4,5,6,7,8,9,10',
                         'Practice counting every day'
                     ]),
                     'examples': json.dumps([
                         'Q: Count the stars: ⭐⭐⭐ How many? A: 3 stars',
                         'Q: Count your fingers on one hand. A: 5 fingers',
                         'Q: If you have 2 cookies and get 1 more, how many? A: 3 cookies'
                     ]),
                     'did_you_know': 'The word "mathematics" comes from an ancient Greek word meaning "to learn"!',
                     'definition': 'A number is a symbol that tells us how many or how much.'},

                    {'title': 'Numbers 11 to 20', 'emoji': '2️⃣', 'order': 2,
                     'content': '''Now let's learn numbers from 11 to 20!

11 - Eleven
12 - Twelve
13 - Thirteen
14 - Fourteen
15 - Fifteen
16 - Sixteen
17 - Seventeen
18 - Eighteen
19 - Nineteen
20 - Twenty

Notice that numbers 13 to 19 end with "teen". This means "ten" plus the number.
13 = three + ten = thirteen
14 = four + ten = fourteen

Numbers 11 and 12 are special - they have their own names!''',
                     'key_points': json.dumps([
                         'Numbers 11-20 come after 10',
                         '13-19 end with "-teen" (meaning + ten)',
                         '11 and 12 have special names',
                         'Practice counting from 1 to 20'
                     ]),
                     'examples': json.dumps([
                         'Q: What comes after 14? A: 15 (fifteen)',
                         'Q: Count 10 to 20. A: 10,11,12,13,14,15,16,17,18,19,20',
                         'Q: How many toes do you have? A: 20 toes'
                     ]),
                     'did_you_know': 'The number 12 is called a "dozen". A dozen eggs means 12 eggs!'}
                ]
            })

            content.append({
                'subject': m, 'grade': grades['G1'],
                'topic_title': 'Addition and Subtraction', 'topic_icon': '➕', 'topic_subtitle': 'Adding and taking away numbers',
                'difficulty': 'easy', 'order': 2, 'lessons': [
                    {'title': 'Adding Numbers (1-10)', 'emoji': '➕', 'order': 1,
                     'content': '''Addition means putting things together.

When we add, we find the TOTAL.
The + sign means "add" or "plus".
The = sign means "equals" or "is".

Example: 2 + 3 = 5
This means: 2 apples plus 3 apples equals 5 apples! 🍎🍎 + 🍎🍎🍎 = 🍎🍎🍎🍎🍎

Steps for addition:
1. Count the first group
2. Count the second group
3. Count ALL objects together
4. That's your answer!''',
                     'key_points': json.dumps([
                         'Addition means putting groups together',
                         'The + sign means add/plus',
                         'The = sign means equals',
                         'Add by counting all objects'
                     ]),
                     'examples': json.dumps([
                         'Q: 1 + 1 = ? A: 2',
                         'Q: 3 + 2 = ? A: 5',
                         'Q: 4 + 4 = ? A: 8',
                         'Q: 5 + 3 = ? A: 8'
                     ]),
                     'did_you_know': 'The plus sign (+) comes from the Latin word "et" meaning "and"!',
                     'definition': 'Addition is when you put two or more groups together to find the total.'},

                    {'title': 'Taking Away (Subtraction)', 'emoji': '➖', 'order': 2,
                     'content': '''Subtraction means taking away from a group.

When we subtract, we find WHAT'S LEFT.
The - sign means "subtract", "take away", or "minus".

Example: 5 - 2 = 3
This means: 5 cookies minus 2 cookies equals 3 cookies left! 🍪🍪🍪🍪🍪 - 🍪🍪 = 🍪🍪🍪

Steps for subtraction:
1. Count what you have
2. Take away the number
3. Count what's left
4. That's your answer!''',
                     'key_points': json.dumps([
                         'Subtraction means taking away',
                         'The - sign means subtract/take away',
                         'The answer is what is LEFT',
                         'Start with the bigger number'
                     ]),
                     'examples': json.dumps([
                         'Q: 3 - 1 = ? A: 2',
                         'Q: 5 - 2 = ? A: 3',
                         'Q: 7 - 3 = ? A: 4',
                         'Q: 10 - 5 = ? A: 5'
                     ]),
                     'did_you_know': 'The word "subtract" comes from Latin "subtrahere" meaning "to pull from under"!'}
                ]
            })

        # Grade 2 Mathematics
        if 'G2' in grades:
            content.append({
                'subject': m, 'grade': grades['G2'],
                'topic_title': 'Numbers up to 100', 'topic_icon': '🔢', 'topic_subtitle': 'Counting and place value to 100',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Counting to 100', 'emoji': '💯', 'order': 1,
                     'content': '''In Grade 2, we learn to count all the way to 100!

Numbers 1-10: one, two, three, four, five, six, seven, eight, nine, ten
Numbers 11-20: eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty
Numbers 21-30: twenty-one, twenty-two... thirty
Numbers 31-100: thirty-one... forty... fifty... sixty... seventy... eighty... ninety... one hundred!

Pattern: After 20, numbers follow a pattern.
21 = twenty + one = twenty-one
35 = thirty + five = thirty-five
47 = forty + seven = forty-seven

The pattern is: tens number + ones number!''',
                     'key_points': json.dumps([
                         'Numbers 1-100 follow patterns',
                         'Each number has tens and ones',
                         'Practice counting by 1s, 5s, and 10s',
                         'Use a 100 chart to help'
                     ]),
                     'examples': json.dumps([
                         'Q: Count by 10s: 10,20,30,?,50. A: 40',
                         'Q: What number is 3 tens and 4 ones? A: 34',
                         'Q: Count backwards from 20 to 10'
                     ]),
                     'did_you_know': 'The number 100 is called a "century" when talking about years!',
                     'definition': 'Place value tells us the value of a digit based on its position in a number.'},

                    {'title': 'Place Value: Tens and Ones', 'emoji': '🏗️', 'order': 2,
                     'content': '''Every number has place value. This means each digit has a value based on WHERE it sits.

In the number 53:
- The 5 is in the TENS place = 50
- The 3 is in the ONES place = 3
- So 53 = 5 tens + 3 ones = 50 + 3

In the number 68:
- The 6 is in the TENS place = 60
- The 8 is in the ONES place = 8
- So 68 = 6 tens + 8 ones = 60 + 8

Remember: TENS are on the LEFT, ONES are on the RIGHT!''',
                     'key_points': json.dumps([
                         'Tens place is on the left',
                         'Ones place is on the right',
                         'Each digit has a different value',
                         '53 = 50 + 3 (5 tens + 3 ones)'
                     ]),
                     'examples': json.dumps([
                         'Q: In 42, what is the tens digit? A: 4 (value = 40)',
                         'Q: In 79, what is the ones digit? A: 9 (value = 9)',
                         'Q: Write 36 as tens and ones. A: 3 tens + 6 ones'
                     ]),
                     'did_you_know': 'The number system we use is called the "decimal system" because it is based on 10!'}
                ]
            })

            content.append({
                'subject': m, 'grade': grades['G2'],
                'topic_title': 'Shapes and Patterns', 'topic_icon': '⬛', 'topic_subtitle': 'Identifying and creating patterns',
                'difficulty': 'easy', 'order': 2, 'lessons': [
                    {'title': '2D Shapes', 'emoji': '🔷', 'order': 1,
                     'content': '''Shapes are all around us! Let's learn about 2D (flat) shapes.

Circle ⭕ - Round and smooth, no corners (like a ball or clock)
Square ⬛ - Four equal sides, four corners (like a window)
Triangle 🔺 - Three sides, three corners (like a sandwich cut in half)
Rectangle ▬ - Four sides, opposite sides equal (like a door)
Diamond ◈ - Four sides, tilted square (like a kite)
Oval 🔵 - Like a stretched circle (like an egg)

Look around your home. How many shapes can you find?''',
                     'key_points': json.dumps([
                         'A circle has no corners - it is round',
                         'A square has 4 equal sides',
                         'A triangle has 3 sides and 3 corners',
                         'A rectangle has 4 sides (opposite sides equal)',
                         'Shapes are everywhere around us'
                     ]),
                     'examples': json.dumps([
                         'Q: What shape is a football? A: Circle (sphere in 3D)',
                         'Q: What shape has 3 sides? A: Triangle',
                         'Q: What is the difference between a square and a rectangle? A: A square has all equal sides, a rectangle has opposite sides equal'
                     ]),
                     'did_you_know': 'A circle has no sides! It is a continuous curved line.',
                     'definition': 'A 2D shape is a flat shape with only length and width.'},

                    {'title': 'Creating Patterns', 'emoji': '🎨', 'order': 2,
                     'content': '''A pattern is something that repeats over and over.

Patterns can be made with:
- Shapes: 🔵🔴🟡🔵🔴🟡 (circle, red, yellow, repeat)
- Colors: red, blue, red, blue, red, blue
- Numbers: 2,4,6,8,10 (add 2 each time)
- Objects: spoon, fork, spoon, fork, spoon, fork

To find a pattern: look for what REPEATS!''',
                     'key_points': json.dumps([
                         'A pattern repeats in a predictable way',
                         'Patterns can use shapes, colors, numbers or objects',
                         'Look for the "core" that repeats',
                         'You can create your own patterns'
                     ]),
                     'examples': json.dumps([
                         'Q: What comes next: 🟢🟡🔴🟢🟡? A: 🔴',
                         'Q: Complete: 2,4,6,8,? A: 10',
                         'Q: Make a pattern using triangle and circle'
                     ]),
                     'did_you_know': 'Nature is full of patterns - from honeycombs to butterfly wings!'}
                ]
            })

        # Grade 3 Mathematics
        if 'G3' in grades:
            content.append({
                'subject': m, 'grade': grades['G3'],
                'topic_title': 'Multiplication Basics', 'topic_icon': '✖️', 'topic_subtitle': 'Introduction to multiplication tables',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'What is Multiplication?', 'emoji': '✖️', 'order': 1,
                     'content': '''Multiplication is a fast way to ADD the SAME NUMBER many times.

Think of it as "groups of":
3 × 4 means "3 groups of 4"
🍎🍎🍎🍎 + 🍎🍎🍎🍎 + 🍎🍎🍎🍎 = 12 apples

Instead of adding 4+4+4, we can say 3 × 4 = 12!

The × sign means "multiply" or "times".
3 × 4 = 12 (three times four equals twelve)''',
                     'key_points': json.dumps([
                         'Multiplication is repeated addition',
                         '3 × 4 means 3 groups of 4',
                         'The × sign means multiply/times',
                         'Learn the times tables'
                     ]),
                     'examples': json.dumps([
                         'Q: 2 × 3 = ? A: 6 (2 groups of 3 = 3+3)',
                         'Q: 4 × 2 = ? A: 8 (4 groups of 2 = 2+2+2+2)',
                         'Q: 5 × 1 = ? A: 5 (any number × 1 = itself)'
                     ]),
                     'did_you_know': 'Multiplication was invented thousands of years ago by ancient Babylonians!',
                     'definition': 'Multiplication is repeated addition of the same number.'},

                    {'title': 'Times Tables: 2, 5 and 10', 'emoji': '📊', 'order': 2,
                     'content': '''Let's learn the most useful times tables!

2 Times Table (skip count by 2):
2, 4, 6, 8, 10, 12, 14, 16, 18, 20

5 Times Table (skip count by 5):
5, 10, 15, 20, 25, 30, 35, 40, 45, 50

10 Times Table (skip count by 10):
10, 20, 30, 40, 50, 60, 70, 80, 90, 100

Tip: Any number × 10 = the number with a zero at the end!
Example: 6 × 10 = 60, 9 × 10 = 90''',
                     'key_points': json.dumps([
                         '×2 means double the number',
                         '×5 ends in 0 or 5',
                         '×10 adds a zero at the end',
                         'Practice skip counting'
                     ]),
                     'examples': json.dumps([
                         'Q: 3 × 2 = ? A: 6 (double 3)',
                         'Q: 7 × 5 = ? A: 35',
                         'Q: 8 × 10 = ? A: 80',
                         'Q: 6 × 2 = ? A: 12'
                     ]),
                     'did_you_know': 'The word "multiplication" comes from Latin "multi" meaning many and "plicare" meaning to fold!'}
                ]
            })

        # Grade 4 Mathematics
        if 'G4' in grades:
            content.append({
                'subject': m, 'grade': grades['G4'],
                'topic_title': 'Fractions', 'topic_icon': '🍕', 'topic_subtitle': 'Understanding parts of a whole',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Introduction to Fractions', 'emoji': '🍕', 'order': 1,
                     'content': '''A fraction is a PART of a WHOLE.

Imagine a pizza cut into 4 equal pieces.
If you eat 1 piece, you have eaten 1/4 (one quarter) of the pizza.
If you eat 2 pieces, you have eaten 2/4 (two quarters = half) of the pizza.

Fraction parts:
- Top number = NUMERATOR (how many parts we have)
- Bottom number = DENOMINATOR (how many equal parts total)

1/2 means: 1 part out of 2 equal parts (HALF)
1/4 means: 1 part out of 4 equal parts (QUARTER)
1/3 means: 1 part out of 3 equal parts (THIRD)''',
                     'key_points': json.dumps([
                         'A fraction shows a part of a whole',
                         'Numerator = how many parts we have (top)',
                         'Denominator = total equal parts (bottom)',
                         'The whole must be divided equally'
                     ]),
                     'examples': json.dumps([
                         'Q: If a chocolate bar has 8 pieces and you eat 3, what fraction did you eat? A: 3/8',
                         'Q: What fraction is half? A: 1/2',
                         'Q: Which is bigger: 1/4 or 1/2? A: 1/2'
                     ]),
                     'did_you_know': 'The word "fraction" comes from Latin "fractus" meaning "broken"!',
                     'definition': 'A fraction represents a part of a whole, written as numerator/denominator.'}
                ]
            })

    # ============================================================
    # ENGLISH
    # ============================================================
    if 'English' in subjects:
        e = subjects['English']

        if 'G1' in grades:
            content.append({
                'subject': e, 'grade': grades['G1'],
                'topic_title': 'Alphabet and Phonics', 'topic_icon': '🔤', 'topic_subtitle': 'Learning letters and their sounds',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'The Alphabet: A to M', 'emoji': '🔤', 'order': 1,
                     'content': '''The English alphabet has 26 letters. Today we learn A to M!

A a - /a/ as in Apple 🍎
B b - /b/ as in Ball ⚽
C c - /k/ as in Cat 🐱
D d - /d/ as in Dog 🐶
E e - /e/ as in Elephant 🐘
F f - /f/ as in Fish 🐟
G g - /g/ as in Goat 🐐
H h - /h/ as in Hat 🎩
I i - /i/ as in Igloo 🏔️
J j - /j/ as in Juice 🧃
K k - /k/ as in Kite 🪁
L l - /l/ as in Lion 🦁
M m - /m/ as in Moon 🌙

Each letter has a capital (big) and small form.
Say each letter and its sound out loud!''',
                     'key_points': json.dumps([
                         'There are 26 letters in the English alphabet',
                         'Each letter has a name and a sound',
                         'Letters come in uppercase (capital) and lowercase',
                         'Practice saying each letter and its sound'
                     ]),
                     'examples': json.dumps([
                         'Q: What sound does B make? A: /b/ as in ball',
                         'Q: What letter comes after F? A: G',
                         'Q: Spell "cat". A: C-A-T'
                     ]),
                     'did_you_know': 'The word "alphabet" comes from the first two Greek letters: alpha and beta!',
                     'definition': 'A letter is a symbol that represents a sound in writing.'},

                    {'title': 'The Alphabet: N to Z', 'emoji': '🔤', 'order': 2,
                     'content': '''Now let's learn the rest of the alphabet!

N n - /n/ as in Nest 🪺
O o - /o/ as in Octopus 🐙
P p - /p/ as in Pig 🐷
Q q - /kw/ as in Queen 👸
R r - /r/ as in Rainbow 🌈
S s - /s/ as in Sun ☀️
T t - /t/ as in Tree 🌳
U u - /u/ as in Umbrella ☂️
V v - /v/ as in Violin 🎻
W w - /w/ as in Water 💧
X x - /ks/ as in Fox 🦊
Y y - /y/ as in Yellow 💛
Z z - /z/ as in Zebra 🦓

Great job! Now you know ALL 26 letters of the alphabet!
Try singing the alphabet song to remember them.''',
                     'key_points': json.dumps([
                         'N to Z completes the 26 letter alphabet',
                         'Q is almost always followed by U',
                         'X makes the /ks/ sound',
                         'Sing the alphabet song to remember'
                     ]),
                     'examples': json.dumps([
                         'Q: What is the last letter of the alphabet? A: Z',
                         'Q: What letter comes after T? A: U',
                         'Q: Spell "sun". A: S-U-N'
                     ]),
                     'did_you_know': 'The letter E is the most commonly used letter in English!'}
                ]
            })

            content.append({
                'subject': e, 'grade': grades['G1'],
                'topic_title': 'Simple Words and Sentences', 'topic_icon': '📝', 'topic_subtitle': 'Reading and writing basic words',
                'difficulty': 'easy', 'order': 2, 'lessons': [
                    {'title': 'Three-Letter Words', 'emoji': '📖', 'order': 1,
                     'content': '''Let's read three-letter words! These are called CVC words (Consonant-Vowel-Consonant).

Short a words: cat, hat, bat, mat, rat, fan, van
Short e words: hen, pen, ten, bed, red, leg
Short i words: pig, big, dig, sit, hit, lip
Short o words: dog, log, hot, pot, box, fox
Short u words: cup, bus, sun, run, fun, mud

Tips for reading:
1. Say each sound: c-a-t
2. Blend the sounds together: ccc-aaa-ttt
3. Say the word: CAT! 🐱

Practice every day!''',
                     'key_points': json.dumps([
                         'CVC words have consonant-vowel-consonant pattern',
                         'Blend sounds together to read words',
                         'Short vowels: a, e, i, o, u',
                         'Practice makes perfect!'
                     ]),
                     'examples': json.dumps([
                         'Read: c-a-t = cat',
                         'Read: d-o-g = dog',
                         'Read: s-u-n = sun'
                     ]),
                     'did_you_know': 'The shortest complete sentence in English is "I am"!',
                     'definition': 'A CVC word is a three-letter word with a consonant, vowel, and consonant.'}
                ]
            })

        if 'G2' in grades:
            content.append({
                'subject': e, 'grade': grades['G2'],
                'topic_title': 'Building Sentences', 'topic_icon': '📝', 'topic_subtitle': 'Writing complete sentences',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Parts of a Sentence', 'emoji': '📝', 'order': 1,
                     'content': '''A sentence is a group of words that tells a complete thought.

Every sentence needs:
1. A CAPITAL letter at the beginning
2. A period (.) at the end
3. A naming part (who or what)
4. A telling part (what happens)

Example: The cat sleeps.
- "The cat" = naming part (WHO?)
- "sleeps" = telling part (WHAT?)

Examples:
- The dog runs. 🐕
- My mom cooks. 👩
- I read books. 📚
- Birds fly high. 🕊️''',
                     'key_points': json.dumps([
                         'A sentence starts with a capital letter',
                         'A sentence ends with a period',
                         'Every sentence has a naming part and a telling part',
                         'A sentence tells a complete thought'
                     ]),
                     'examples': json.dumps([
                         'Q: Is "the cat" a sentence? A: No - it needs a telling part',
                         'Q: Is "The cat sleeps" a sentence? A: Yes!',
                         'Q: Fix this: "the dog runs" A: "The dog runs."'
                     ]),
                     'did_you_know': 'The longest sentence in English literature has over 4,000 words!',
                     'definition': 'A sentence is a group of words that expresses a complete thought.'},

                    {'title': 'Nouns and Verbs', 'emoji': '🏷️', 'order': 2,
                     'content': '''Words have different jobs in a sentence. Two important types are NOUNS and VERBS.

NOUNS are naming words. They name:
- People: boy, girl, teacher, mom, dad
- Places: school, home, park, Nairobi
- Things: book, ball, table, apple

VERBS are action words. They tell what someone or something DOES:
- run, jump, eat, sleep, read, write, play

In a sentence: "The boy runs."
- "boy" = noun (WHO?)
- "runs" = verb (WHAT does the boy do?)''',
                     'key_points': json.dumps([
                         'Nouns name people, places, or things',
                         'Verbs show action',
                         'A sentence needs both nouns and verbs',
                         'Find the noun first, then the verb'
                     ]),
                     'examples': json.dumps([
                         'Q: Find the noun: "The girl sings." A: girl',
                         'Q: Find the verb: "Birds fly." A: fly',
                         'Q: Is "happiness" a noun? A: Yes - it names a feeling'
                     ]),
                     'did_you_know': 'There are over 170,000 words in the English dictionary!'}
                ]
            })

    # ============================================================
    # SCIENCE & TECHNOLOGY
    # ============================================================
    if 'Science & Technology' in subjects:
        s = subjects['Science & Technology']

        if 'G1' in grades:
            content.append({
                'subject': s, 'grade': grades['G1'],
                'topic_title': 'Living and Non-Living Things', 'topic_icon': '🌿', 'topic_subtitle': 'What is alive and what is not',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Living Things', 'emoji': '🌱', 'order': 1,
                     'content': '''Living things are all around us! They are things that are ALIVE.

Living things:
- Grow 🌱
- Eat food 🍎
- Move 🏃
- Breathe air 💨
- Have babies/young 👶
- Change with time

Examples of living things:
- Plants (trees, flowers, grass)
- Animals (dogs, cats, birds, fish)
- People (you, your family, friends)
- Insects (butterflies, ants, bees)''',
                     'key_points': json.dumps([
                         'Living things grow, eat, move, breathe, and reproduce',
                         'Plants, animals, people and insects are living',
                         'All living things need food and water',
                         'Living things respond to their environment'
                     ]),
                     'examples': json.dumps([
                         'Q: Is a rock living? A: No - it does not grow or eat',
                         'Q: Is a tree living? A: Yes - it grows and needs water',
                         'Q: Name 3 living things you can see right now'
                     ]),
                     'did_you_know': 'The largest living thing on Earth is a giant sequoia tree named General Sherman!',
                     'definition': 'Living things are organisms that grow, need food, and can reproduce.'},

                    {'title': 'Non-Living Things', 'emoji': '🪨', 'order': 2,
                     'content': '''Non-living things are NOT alive. They do not grow, eat, or breathe.

Non-living things:
- Do NOT grow
- Do NOT need food
- Do NOT breathe
- Do NOT have babies
- Do NOT change by themselves

Examples of non-living things:
- Rocks and stones 🪨
- Water 💧
- Chair and table 🪑
- Toy car 🚗
- Book 📚
- Pencil ✏️

Some non-living things were once alive! A pencil is made from wood (from a tree). A paper book comes from trees too!''',
                     'key_points': json.dumps([
                         'Non-living things do not grow, eat, or breathe',
                         'Rocks, water, furniture, toys are non-living',
                         'Some non-living things come from living things',
                         'Living vs non-living is easy to tell'
                     ]),
                     'examples': json.dumps([
                         'Q: Is a table living or non-living? A: Non-living',
                         'Q: Is water living or non-living? A: Non-living',
                         'Q: A wooden spoon comes from a tree. Is it living? A: No - it is non-living now'
                     ]),
                     'did_you_know': 'A virus is tricky - scientists debate whether it is living or non-living!'}
                ]
            })

        if 'G4' in grades:
            content.append({
                'subject': s, 'grade': grades['G4'],
                'topic_title': 'The Human Body', 'topic_icon': '🧍', 'topic_subtitle': 'Understanding our body systems',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Body Systems', 'emoji': '🧠', 'order': 1,
                     'content': '''The human body is amazing! It has many systems that work together.

Skeletal System 🦴
- Made of 206 bones
- Gives our body shape
- Protects our organs
- Helps us move

Muscular System 💪
- Over 600 muscles
- Helps us move and lift
- Some muscles work automatically (heart!)

Digestive System 🫃
- Breaks down food
- Takes nutrients to our body
- Removes waste

Nervous System 🧠
- Brain, spinal cord, nerves
- Controls everything we do
- Helps us think, feel, and move''',
                     'key_points': json.dumps([
                         'The body has many systems working together',
                         'Bones provide structure and protection',
                         'Muscles help us move',
                         'The brain controls all body systems',
                         'Each system has an important job'
                     ]),
                     'examples': json.dumps([
                         'Q: How many bones does an adult have? A: 206',
                         'Q: Which system helps you think? A: Nervous system',
                         'Q: What does the digestive system do? A: Breaks down food'
                     ]),
                     'did_you_know': 'Your nose can remember 50,000 different scents!',
                     'definition': 'A body system is a group of organs that work together to perform a function.'}
                ]
            })

    # ============================================================
    # CRE (Christian Religious Education)
    # ============================================================
    if 'CRE' in subjects:
        cre = subjects['CRE']

        if 'G1' in grades:
            content.append({
                'subject': cre, 'grade': grades['G1'],
                'topic_title': 'God\'s Creation', 'topic_icon': '🌍', 'topic_subtitle': 'Learning about God\'s wonderful world',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'The World God Made', 'emoji': '🌍', 'order': 1,
                     'content': '''God made the whole world! The Bible tells us that God created everything in 7 days.

Day 1: God made light 🌞 - He called light "day" and darkness "night"
Day 2: God made the sky ☁️ and the waters
Day 3: God made land, seas, and plants 🌿🌺🌳
Day 4: God made the sun, moon, and stars 🌟
Day 5: God made fish 🐟 and birds 🐦
Day 6: God made animals 🐘🦁🐒 AND people (Adam and Eve)
Day 7: God rested - He made this day holy

God looked at everything He made and said it was "VERY GOOD!" 💚''',
                     'key_points': json.dumps([
                         'God created the whole world in 7 days',
                         'Everything God made is good',
                         'God made people on day 6 - special!',
                         'God rested on day 7 (Sunday)',
                         'We should take care of God\'s creation'
                     ]),
                     'examples': json.dumps([
                         'Q: What did God make on day 1? A: Light (day and night)',
                         'Q: What did God make on day 4? A: Sun, moon, and stars',
                         'Q: On which day did God make people? A: Day 6'
                     ]),
                     'did_you_know': 'The story of creation is found in the first book of the Bible called Genesis!',
                     'definition': 'Creation means everything that God made - the whole universe and everything in it.'},

                    {'title': 'Caring for God\'s Creation', 'emoji': '🌿', 'order': 2,
                     'content': '''God made the world and asked us to take CARE of it. This is called stewardship.

How can we care for God's creation?

🌳 Plant trees - trees give us clean air and shade
💧 Save water - don't leave the tap running
🗑️ Don't litter - put rubbish in the bin
🐦 Feed birds - help the animals around us
🌺 Water plants - help flowers and trees grow
♻️ Recycle - use things again instead of throwing away

The Bible says: "The earth is the Lord's, and everything in it." (Psalm 24:1)''',
                     'key_points': json.dumps([
                         'God wants us to take care of the world',
                         'We can plant trees and water plants',
                         'We should keep our environment clean',
                         'Every small action helps',
                         'We are caretakers of God\'s creation'
                     ]),
                     'examples': json.dumps([
                         'Q: Who should take care of the earth? A: Everyone! (especially us)',
                         'Q: Name one way to care for creation. A: Plant a tree',
                         'Q: Why is water important? A: All living things need water'
                     ]),
                     'did_you_know': 'Psalm 24:1 says "The earth is the Lord\'s, and everything in it!"'}
                ]
            })

        if 'G4' in grades:
            content.append({
                'subject': cre, 'grade': grades['G4'],
                'topic_title': 'Moses and the Israelites', 'topic_icon': '🏔️', 'topic_subtitle': 'God leads His people to freedom',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Baby Moses', 'emoji': '👶', 'order': 1,
                     'content': '''The story of Moses begins with a brave baby and a faithful family.

Long ago, the Israelites (God's people) were slaves in Egypt. The king of Egypt, called Pharaoh, was afraid of the Israelites. He made a terrible law: all baby Hebrew boys must be thrown into the Nile River.

When Moses was born, his mother saw he was a beautiful baby. She hid him for 3 months! When she could not hide him anymore, she made a basket (called an ark) from papyrus reeds. She put Moses in the basket and placed it among the reeds of the Nile River.

Moses' sister Miriam watched from far away. Pharaoh's daughter came to bathe in the river. She found the basket and felt sorry for the crying baby. Miriam bravely asked: "Shall I get a Hebrew woman to nurse the baby for you?" She brought Moses' own mother!

Moses grew up in the palace of Pharaoh, but he never forgot that he was an Israelite.''',
                     'key_points': json.dumps([
                         'Moses was born a Hebrew slave in Egypt',
                         'His mother hid him to save his life',
                         'Pharaoh\'s daughter found and adopted him',
                         'God had a special plan for Moses',
                         'Miriam showed courage by helping her brother'
                     ]),
                     'examples': json.dumps([
                         'Q: Why did Moses\' mother hide him? A: To save him from Pharaoh\'s order',
                         'Q: Who found Moses in the river? A: Pharaoh\'s daughter',
                         'Q: What did Miriam do? A: She watched over Moses and got their mother'
                     ]),
                     'did_you_know': 'The name "Moses" means "drawn out of the water" in Hebrew!',
                     'definition': 'The Israelites were God\'s chosen people, descendants of Abraham, Isaac, and Jacob.'},

                    {'title': 'The Ten Plagues', 'emoji': '⚠️', 'order': 2,
                     'content': '''God sent Moses and his brother Aaron to tell Pharaoh: "Let my people go!" But Pharaoh refused.

God sent ten plagues to show His power:

1. Water turned to blood 💧➡️🩸
2. Frogs everywhere 🐸
3. Gnats (tiny biting insects) 🦟
4. Flies
5. Livestock got sick 🐄
6. Boils (painful sores on skin)
7. Hail and fire from the sky ⛈️🔥
8. Locusts (grasshoppers that ate all crops) 🦗
9. Darkness for 3 days 🌑
10. Death of firstborn (the most terrible)

After the tenth plague, Pharaoh finally told Moses to take the Israelites and leave Egypt! God protected His people by telling them to mark their doors with lamb's blood - the angel of death "passed over" their homes. This is called the Passover.

God is powerful and He always keeps His promises!''',
                     'key_points': json.dumps([
                         'Pharaoh refused to free the Israelites',
                         'God sent 10 plagues to show His power',
                         'The 10th plague was the worst - death of firstborn',
                         'God protected the Israelites during Passover',
                         'Pharaoh finally let God\'s people go'
                     ]),
                     'examples': json.dumps([
                         'Q: How many plagues did God send? A: 10',
                         'Q: What was the last plague? A: Death of the firstborn',
                         'Q: What is Passover? A: When God\'s people were saved from the last plague'
                     ]),
                     'did_you_know': 'The Jewish holiday of Passover is still celebrated today to remember when God freed His people!'}
                ]
            })

    # ============================================================
    # HYGIENE & NUTRITION
    # ============================================================
    if 'Hygiene & Nutrition' in subjects:
        hn = subjects['Hygiene & Nutrition']

        if 'G1' in grades:
            content.append({
                'subject': hn, 'grade': grades['G1'],
                'topic_title': 'Personal Hygiene', 'topic_icon': '🧼', 'topic_subtitle': 'Keeping our bodies clean and healthy',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Washing Your Hands', 'emoji': '🧼', 'order': 1,
                     'content': '''Hand washing is the most important thing you can do to stay healthy!

When to wash hands:
- Before eating 🍽️
- After using the toilet 🚽
- After playing outside 🌳
- After touching animals 🐕
- After coughing or sneezing 🤧
- When hands look dirty

Steps for proper hand washing (sing the ABC song while doing it!):

1. Wet hands with clean water 💧
2. Apply soap 🧼
3. Rub hands together - palm to palm
4. Rub between fingers
5. Rub back of hands
6. Rub thumbs
7. Rub fingertips on palms
8. Rinse with clean water
9. Dry with a clean towel or air dry

Washing hands removes germs that can make us sick!''',
                     'key_points': json.dumps([
                         'Wash hands before eating and after toilet',
                         'Use soap and clean water',
                         'Wash for at least 20 seconds',
                         'Rub all parts of your hands',
                         'Clean hands keep you healthy'
                     ]),
                     'examples': json.dumps([
                         'Q: When should you wash your hands? A: Before eating, after toilet, after playing',
                         'Q: How long should you wash? A: About 20 seconds (ABC song once)',
                         'Q: Why do we use soap? A: Soap removes germs'
                     ]),
                     'did_you_know': 'Germs are so tiny that millions can fit on the head of a pin!',
                     'definition': 'Hygiene means keeping yourself and your surroundings clean to stay healthy.'},

                    {'title': 'Brushing Your Teeth', 'emoji': '🪥', 'order': 2,
                     'content': '''Your teeth help you eat, smile, and speak! Keep them healthy by brushing.

Why brush your teeth?
- Removes food particles left after eating
- Prevents cavities (holes in teeth)
- Keeps breath fresh
- Prevents gum disease
- Gives you a bright smile! 😁

How to brush properly:
1. Use a pea-sized amount of toothpaste
2. Brush in small circles
3. Brush front, back, and top of every tooth
4. Brush for 2 minutes (morning and night)
5. Don't forget your tongue!
6. Spit, don't swallow the toothpaste
7. Rinse your toothbrush

Visit the dentist twice a year to check your teeth! 🦷''',
                     'key_points': json.dumps([
                         'Brush teeth twice a day - morning and night',
                         'Brush for 2 minutes each time',
                         'Use a pea-sized amount of toothpaste',
                         'Brush all surfaces of every tooth',
                         'Visit the dentist regularly'
                     ]),
                     'examples': json.dumps([
                         'Q: How many times a day should you brush? A: Twice (morning and night)',
                         'Q: How long should you brush? A: 2 minutes',
                         'Q: Why do we brush our teeth? A: To remove food and prevent cavities'
                     ]),
                     'did_you_know': 'The toothbrush was invented over 5,000 years ago! People used twigs with frayed ends.'}
                ]
            })

        if 'G3' in grades:
            content.append({
                'subject': hn, 'grade': grades['G3'],
                'topic_title': 'Healthy Eating', 'topic_icon': '🥗', 'topic_subtitle': 'Eating foods that make us strong',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Food Groups', 'emoji': '🍎', 'order': 1,
                     'content': '''Food gives us energy and helps us grow! Different foods do different jobs.

The main food groups:

🥛 Milk and Dairy (calcium for strong bones)
- Milk, yogurt, cheese
- Good for bones and teeth

🥩 Proteins (building blocks for the body)
- Meat, fish, eggs, beans, lentils
- Helps muscles grow and repair

🍞 Carbohydrates (energy foods)
- Ugali, rice, bread, chapati, potatoes
- Gives us energy to play and learn

🥗 Fruits and Vegetables (vitamins and minerals)
- Sukuma wiki, cabbage, carrots, oranges, mangoes
- Keeps us healthy and fights sickness

🥜 Fats and Oils (in small amounts)
- Cooking oil, butter, avocado
- Stored energy for the body

Eat different foods from each group every day!''',
                     'key_points': json.dumps([
                         'There are 5 food groups',
                         'Each food group has different benefits',
                         'Eat a variety of foods every day',
                         'Fruits and vegetables keep us healthy',
                         'Proteins help us grow strong'
                     ]),
                     'examples': json.dumps([
                         'Q: Which food group gives energy? A: Carbohydrates (ugali, rice)',
                         'Q: What food is good for bones? A: Milk and dairy (calcium)',
                         'Q: Name a fruit that grows in Kenya. A: Mango, orange, banana, pawpaw'
                     ]),
                     'did_you_know': 'Kenya produces some of the best avocados in the world!',
                     'definition': 'Nutrition means getting the right foods for your body to grow and stay healthy.'},

                    {'title': 'Healthy Eating Habits', 'emoji': '🍽️', 'order': 2,
                     'content': '''Eating healthy is about more than just WHAT you eat. It is also about HOW you eat!

Tips for healthy eating:

1. Eat breakfast every day 🌅
   - Breakfast gives you energy for school
   - Try porridge, bread, or fruit

2. Eat 3 main meals + 2 healthy snacks
   - Breakfast, lunch, supper
   - Snacks: fruit, nuts, yogurt

3. Drink plenty of water 💧
   - Drink at least 6-8 glasses a day
   - Water helps your body work properly

4. Eat your vegetables! 🥬
   - Sukuma wiki (kale) is very healthy
   - Carrots help your eyes see well

5. Limit sweets and soda 🚫
   - Too much sugar is bad for teeth and health
   - Save sweets for special treats

6. Wash all fruits before eating 🍎
   - Removes dirt and chemicals

A healthy plate should have: ½ vegetables, ¼ carbohydrates, ¼ protein!''',
                     'key_points': json.dumps([
                         'Always eat breakfast for energy',
                         'Eat a variety of colorful foods',
                         'Drink plenty of water daily',
                         'Limit sweets and sugary drinks',
                         'Wash fruits and vegetables before eating'
                     ]),
                     'examples': json.dumps([
                         'Q: Why is breakfast important? A: It gives energy for the day',
                         'Q: How much water should you drink daily? A: 6-8 glasses',
                         'Q: What should a healthy plate have? A: ½ vegetables, ¼ carbs, ¼ protein'
                     ]),
                     'did_you_know': 'Sukuma wiki (kale) has more iron than beef! It is a superfood!'}
                ]
            })

    # ============================================================
    # ENVIRONMENTAL
    # ============================================================
    if 'Environmental' in subjects:
        env = subjects['Environmental']

        if 'G2' in grades:
            content.append({
                'subject': env, 'grade': grades['G2'],
                'topic_title': 'Keeping Our Environment Clean', 'topic_icon': '🧹', 'topic_subtitle': 'Taking care of our surroundings',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Why Clean Environment Matters', 'emoji': '🌍', 'order': 1,
                     'content': '''Keeping our environment clean is very important for health and happiness.

A clean environment means:
- No litter on the ground 🚯
- Clean water in rivers and wells 💧
- Fresh, clean air to breathe 🌬️
- Beautiful surroundings to enjoy 🌺

Why it matters:
1. Health - Germs breed in dirty places, causing sickness
2. Beauty - Clean places look nice and make us happy
3. Safety - No sharp objects or trash to hurt us
4. Animals - Clean environments help animals thrive

The Bible says we should be good stewards of the earth. Taking care of our environment is our responsibility!''',
                     'key_points': json.dumps([
                         'A clean environment keeps us healthy',
                         'Litter and dirt can cause diseases',
                         'We should all help keep our area clean',
                         'Clean surroundings look beautiful',
                         'It is our responsibility to care for the earth'
                     ]),
                     'examples': json.dumps([
                         'Q: What happens if we litter? A: The environment gets dirty, germs spread',
                         'Q: Why should we clean our classroom? A: To stay healthy and learn better',
                         'Q: Name one way to keep the environment clean. A: Put rubbish in the bin'
                     ]),
                     'did_you_know': 'Plastic takes 450 years to break down in the environment! Always dispose of it properly.',
                     'definition': 'Environment means everything around us - the air, water, land, plants, and animals.'},

                    {'title': 'Waste Disposal', 'emoji': '🗑️', 'order': 2,
                     'content': '''Waste is anything we throw away. How we dispose of waste matters!

Types of waste:
🗑️ Organic waste - food scraps, banana peels (can make compost)
📄 Paper waste - old books, newspapers (can be recycled)
🥫 Plastic waste - bottles, bags (can be recycled or reused)
🪴 Garden waste - leaves, grass (can make compost)

How to dispose of waste properly:

1. Sort your waste - separate different types
2. Use the correct bin for each type
3. Compost organic waste to make fertilizer
4. Recycle paper, plastic, and metal
5. Reuse containers and bags when possible

The 3 Rs: Reduce, Reuse, Recycle!

REDUCE - use less
REUSE - use again
RECYCLE - make into new things''',
                     'key_points': json.dumps([
                         'Sort waste into different types',
                         'Organic waste can become compost',
                         'Follow the 3 Rs: Reduce, Reuse, Recycle',
                         'Never burn plastic - it pollutes the air',
                         'Proper waste disposal keeps the environment clean'
                     ]),
                     'examples': json.dumps([
                         'Q: What can you do with banana peels? A: Make compost',
                         'Q: What are the 3 Rs? A: Reduce, Reuse, Recycle',
                         'Q: Why should we recycle paper? A: To save trees'
                     ]),
                     'did_you_know': 'One ton of recycled paper saves about 17 trees!'}
                ]
            })

    # ============================================================
    # SOCIAL STUDIES
    # ============================================================
    if 'Social Studies' in subjects:
        ss = subjects['Social Studies']

        if 'G4' in grades:
            content.append({
                'subject': ss, 'grade': grades['G4'],
                'topic_title': 'Our Country Kenya', 'topic_icon': '🇰🇪', 'topic_subtitle': 'Learning about Kenya - our beloved nation',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Kenya: Land and People', 'emoji': '🌍', 'order': 1,
                     'content': '''Kenya is our beautiful country in East Africa! Let's learn about it.

Kenya Facts:
- Capital city: Nairobi 🏙️
- Population: Over 50 million people
- Official languages: English and Kiswahili 🗣️
- Currency: Kenyan Shilling (KSh) 💰
- Independence: December 12, 1963 (Jamhuri Day) 🎉

Our National Symbols:
- Flag: Black, red, green and white 🏴󠁫󠁥󠁮󠁡󠁿
- National anthem: "Ee Mungu Nguvu Yetu" 🎵
- National animal: Lion 🦁
- National flower: Orchid 🌸
- National bird: Lilac-breasted Roller 🐦
- Motto: "Harambee" (Let's all pull together)

Kenya has 47 counties, each with its own unique culture and attractions!''',
                     'key_points': json.dumps([
                         'Kenya is in East Africa',
                         'Nairobi is the capital city',
                         'We got independence on December 12, 1963',
                         'Our national motto is "Harambee"',
                         'Kenya has 47 counties'
                     ]),
                     'examples': json.dumps([
                         'Q: What is the capital of Kenya? A: Nairobi',
                         'Q: When is Jamhuri Day? A: December 12',
                         'Q: What does "Harambee" mean? A: Let\'s all pull together'
                     ]),
                     'did_you_know': 'Kenya is named after Mount Kenya, the highest mountain in the country!',
                     'definition': 'A country is a nation with its own government, borders, and identity.'},

                    {'title': 'Our Cultural Heritage', 'emoji': '🎭', 'order': 2,
                     'content': '''Kenya has over 40 ethnic communities, each with unique traditions!

Major communities:
- Kikuyu 🏔️ (Central Kenya)
- Luhya 🌄 (Western Kenya)
- Luo 🎣 (Lake Victoria region)
- Kalenjin 🏃 (Rift Valley)
- Kamba 🏹 (Eastern Kenya)
- Maasai 🐄 (Rift Valley - famous warriors)
- Swahili 🏖️ (Coast region)
- Kisii ⛰️ (Western Kenya)
- Mijikenda 🌴 (Coast region)
- Meru 🍵 (Eastern Kenya)

Each community has:
- Unique language and dialects
- Traditional foods (Ugali, Githeri, Mukimo, Pilau)
- Music and dance styles
- Traditional clothing
- Customs and ceremonies

We celebrate our diversity while being one nation!''',
                     'key_points': json.dumps([
                         'Kenya has over 40 ethnic communities',
                         'Each community has unique traditions',
                         'We speak different languages but are one nation',
                         'Respect all cultures and traditions',
                         'Diversity makes Kenya beautiful'
                     ]),
                     'examples': json.dumps([
                         'Q: Name one Kenyan community. A: Maasai, Kikuyu, Luo, etc.',
                         'Q: What is a traditional Kenyan food? A: Ugali, Githeri, Pilau',
                         'Q: Why is cultural diversity important? A: It makes our country rich and vibrant'
                     ]),
                     'did_you_know': 'The Maasai people are known worldwide for their jumping dance called "Adumu"!'}
                ]
            })

    # ============================================================
    # AGRICULTURE
    # ============================================================
    if 'Agriculture' in subjects:
        ag = subjects['Agriculture']

        if 'G4' in grades:
            content.append({
                'subject': ag, 'grade': grades['G4'],
                'topic_title': 'Growing Food', 'topic_icon': '🌱', 'topic_subtitle': 'How food is grown on farms and gardens',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Preparing a Garden', 'emoji': '🌱', 'order': 1,
                     'content': '''Growing your own food is fun and rewarding! Let's learn how to prepare a garden.

Steps to prepare a garden:

1. Choose a good location 🌞
   - Needs sunlight (at least 6 hours a day)
   - Near water source
   - Flat area with good soil

2. Clear the land 🧹
   - Remove weeds, grass, and stones
   - Dig out unwanted plants

3. Dig the soil ⛏️
   - Loosen the soil using a jembe or fork
   - Dig about 30cm deep
   - Break large clumps of soil

4. Add manure or compost 💩
   - Mix in animal manure or compost
   - This adds nutrients to the soil

5. Make planting rows or beds
   - Raised beds work well
   - Make rows for planting seeds

6. Water the soil before planting 💧

In Kenya, we can grow: maize, beans, kale (sukuma wiki), tomatoes, onions, spinach, and many more!''',
                     'key_points': json.dumps([
                         'Choose a sunny location for your garden',
                         'Clear weeds and dig the soil well',
                         'Add manure or compost for nutrients',
                         'Water the soil before planting',
                         'Many vegetables grow well in Kenya'
                     ]),
                     'examples': json.dumps([
                         'Q: Why do plants need sunlight? A: To make food through photosynthesis',
                         'Q: What is compost? A: Decayed organic matter that feeds the soil',
                         'Q: Name a vegetable that grows well in Kenya. A: Sukuma wiki, spinach, tomatoes'
                     ]),
                     'did_you_know': 'A single maize plant can produce 1-2 cobs, each with about 400-600 kernels!',
                     'definition': 'Agriculture is the practice of growing crops and raising animals for food.'},

                    {'title': 'Caring for Crops', 'emoji': '🌿', 'order': 2,
                     'content': '''After planting, crops need care to grow well. Here is how to care for them.

Watering 💧
- Water in the morning or evening (not noon - sun will burn wet leaves)
- Give enough water but not too much
- Young plants need more frequent watering

Weeding 🌿
- Remove weeds regularly (weeds compete for nutrients)
- Pull them out by the roots
- Weed at least once a week

Mulching 🍂
- Cover soil around plants with dry grass or leaves
- Helps keep moisture in the soil
- Prevents weeds from growing
- Adds nutrients as it decomposes

Pest control 🐛
- Some insects eat crops
- Use natural methods: neem spray, soap water
- Attract helpful insects and birds
- Ask an adult before using any chemicals

Staking 🌿
- Some plants like tomatoes need support
- Use sticks to keep them upright

Watch your garden grow and enjoy the harvest! 🥬🍅🧅''',
                     'key_points': json.dumps([
                         'Water plants in the morning or evening',
                         'Remove weeds regularly',
                         'Mulch helps retain moisture and block weeds',
                         'Use natural methods for pest control',
                         'Patient care leads to a good harvest'
                     ]),
                     'examples': json.dumps([
                         'Q: When is the best time to water plants? A: Morning or evening',
                         'Q: Why do we remove weeds? A: They compete with crops for nutrients and water',
                         'Q: What is mulching? A: Covering soil with dry grass or leaves'
                     ]),
                     'did_you_know': 'Kenya is one of the world\'s largest exporters of tea and cut flowers!'}
                ]
            })

    # ============================================================
    # KISWAHILI
    # ============================================================
    if 'Kiswahili' in subjects:
        k = subjects['Kiswahili']

        if 'G1' in grades:
            content.append({
                'subject': k, 'grade': grades['G1'],
                'topic_title': 'Herufi za Alfabeti', 'topic_icon': '🔤', 'topic_subtitle': 'Kujifunza herufi za Kiswahili',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Herufi A hadi M', 'emoji': '📖', 'order': 1,
                     'content': '''Alfabeti ya Kiswahili ina herufi 26. Hebu tujifunze!

A a - /a/ kama katika "A" - A aa 🍊
B b - /ba/ kama katika "Baba"
C c - /ch/ kama katika "Chai" 🍵
D d - /da/ kama katika "Dada"
E e - /e/ kama katika "Embe" 🥭
F f - /fa/ kama katika "Faru" 🦏
G g - /ga/ kama katika "Gari" 🚗
H h - /ha/ kama katika "Hati" 📄
I i - /i/ kama katika "Ivi"
J j - /ja/ kama katika "Jambo" 👋
K k - /ka/ kama katika "Kuku" 🐔
L l - /la/ kama katika "Lala" 🛏️
M m - /ma/ kama katika "Mama" 👩

Sema kila herufi kwa sauti!''',
                     'key_points': json.dumps([
                         'Kiswahili kina herufi 26',
                         'Kila herufi ina sauti yake',
                         'Vokali: a, e, i, o, u',
                         'Sema herufi kwa sauti kila siku'
                     ]),
                     'examples': json.dumps([
                         'Sema: A kama Aa (chungwa)',
                         'Sema: B kama Baba',
                         'Sema: M kama Mama'
                     ]),
                     'did_you_know': '"Kiswahili" ina maana "lugha ya watu wa pwani"!',
                     'definition': 'Herufi ni alama zinazowakilisha sauti katika lugha.'},

                    {'title': 'Herufi N hadi Z', 'emoji': '📖', 'order': 2,
                     'content': '''Hebu tujifunze herufi N hadi Z!

N n - /na/ kama katika "Nyumba" 🏠
O o - /o/ kama katika "Oga" 🚿
P p - /pa/ kama katika "Paka" 🐱
Q q - /qu/ kama katika "Qatar"
R r - /ra/ kama katika "Rafiki" 🤝
S s - /sa/ kama katika "Saa" ⏰
T t - /ta/ kama katika "Taa" 💡
U u - /u/ kama katika "Ua" 🌺
V v - /va/ kama katika "Viatu" 👟
W w - /wa/ kama katika "Watu" 👥
X x - /ks/ kama katika "Xbox"
Y y - /ya/ kama katika "Yai" 🥚
Z z - /za/ kama katika "Zebra" 🦓

Hongera! Sasa unajua herufi zote!''',
                     'key_points': json.dumps([
                         'Herufi N hadi Z zinakamilisha alfabeti',
                         'Kiswahili hutumia herufi sawa na Kiingereza',
                         'Sauti za Kiswahili ni rahisi kujifunza',
                         'Fanya mazoezi kila siku'
                     ]),
                     'examples': json.dumps([
                         'Sema: N kama Nyumba',
                         'Sema: R kama Rafiki',
                         'Sema: W kama Watu'
                     ]),
                     'did_you_know': 'Kiswahili kinaongezwa na zaidi ya watu milioni 200 duniani kote!'}
                ]
            })

    # ============================================================
    # CODING BASICS
    # ============================================================
    if 'Coding Basics' in subjects:
        cb = subjects['Coding Basics']

        if 'G4' in grades:
            content.append({
                'subject': cb, 'grade': grades['G4'],
                'topic_title': 'What is Coding?', 'topic_icon': '💻', 'topic_subtitle': 'Introduction to computer programming',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Computers and Code', 'emoji': '💻', 'order': 1,
                     'content': '''Coding means giving instructions to a computer. Computers follow our instructions exactly!

What is a computer?
- A machine that follows instructions
- It processes information very fast
- It can do math, show pictures, play games

What is code?
- Code is a set of instructions
- Written in a language computers understand
- Like a recipe for a computer to follow

Think of code like giving directions:
"Walk straight, turn left, go to the big tree."

In coding:
"Move forward, turn right, move forward, collect coin."

Every app, game, and website is made with code!''',
                     'key_points': json.dumps([
                         'Coding means giving instructions to computers',
                         'Computers follow instructions exactly',
                         'Code is a set of step-by-step instructions',
                         'All apps, games, and websites use code',
                         'Anyone can learn to code!'
                     ]),
                     'examples': json.dumps([
                         'Q: What is code? A: Instructions for a computer',
                         'Q: Is coding like following a recipe? A: Yes - step by step instructions',
                         'Q: Can you give an example of a simple instruction? A: "Move forward 3 steps"'
                     ]),
                     'did_you_know': 'The first computer programmer was a woman named Ada Lovelace, in 1843!',
                     'definition': 'Coding is the process of writing instructions for computers to follow.'},

                    {'title': 'Sequences and Algorithms', 'emoji': '🧩', 'order': 2,
                     'content': '''An algorithm is a step-by-step plan for solving a problem.

Think about brushing your teeth:
1. Pick up your toothbrush
2. Put toothpaste on it
3. Brush your teeth for 2 minutes
4. Spit out the toothpaste
5. Rinse your mouth
6. Clean your toothbrush

That is an ALGORITHM! A list of steps in order.

In coding, the order matters a LOT!
If you brush before putting toothpaste, that would not work!

A sequence is steps in the right order.

Try writing an algorithm for:
- Making a cup of tea
- Tying your shoes
- Getting ready for school

Each step must be clear and in the right order!''',
                     'key_points': json.dumps([
                         'An algorithm is a step-by-step plan',
                         'The order of steps matters',
                         'Computers need exact, clear instructions',
                         'Think of coding like giving a recipe',
                         'Practice making algorithms for everyday tasks'
                     ]),
                     'examples': json.dumps([
                         'Q: What is an algorithm? A: Step-by-step plan to solve a problem',
                         'Q: What happens if steps are in the wrong order? A: The result may be wrong',
                         'Q: Make an algorithm for making tea. A: 1. Boil water 2. Put tea bag 3. Pour water 4. Add sugar/milk'
                     ]),
                     'did_you_know': 'The word "algorithm" comes from the name of a Persian mathematician, Al-Khwarizmi!'}
                ]
            })

    # ============================================================
    # HEALTH EDUCATION
    # ============================================================
    if 'Health Education' in subjects:
        he = subjects['Health Education']

        if 'G3' in grades:
            content.append({
                'subject': he, 'grade': grades['G3'],
                'topic_title': 'Staying Healthy', 'topic_icon': '💪', 'topic_subtitle': 'Keeping our bodies strong and well',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Why We Need Exercise', 'emoji': '🏃', 'order': 1,
                     'content': '''Exercise makes our bodies strong and healthy! It is very important for kids.

Benefits of exercise:
💪 Strong muscles and bones
❤️ Healthy heart
🏃 More energy
😊 Makes us happy
😴 Better sleep
🧠 Helps us think better in school

Types of exercise:
- Running 🏃
- Jumping 🤸
- Swimming 🏊
- Football ⚽
- Dancing 💃
- Skipping rope
- Riding a bike 🚲

How much exercise?
- Kids need at least 60 minutes every day!
- Play outside with friends
- Join sports at school

Remember: Move your body every day!''',
                     'key_points': json.dumps([
                         'Exercise makes your body strong',
                         'Kids need 60 minutes of activity daily',
                         'Exercise helps you sleep and think better',
                         'Playing outside counts as exercise',
                         'Find activities you enjoy'
                     ]),
                     'examples': json.dumps([
                         'Q: How much exercise do kids need? A: At least 60 minutes daily',
                         'Q: Name one benefit of exercise. A: Strong muscles, better sleep, more energy',
                         'Q: What exercise do you enjoy doing? A: (Any answer is good!)'
                     ]),
                     'did_you_know': 'Laughter is also exercise! Laughing 15 minutes a day burns about 40 calories!',
                     'definition': 'Exercise is any physical activity that keeps your body fit and healthy.'}
                ]
            })

    # ============================================================
    # LIFE SKILLS
    # ============================================================
    if 'Life Skills' in subjects:
        ls = subjects['Life Skills']

        if 'G3' in grades:
            content.append({
                'subject': ls, 'grade': grades['G3'],
                'topic_title': 'Values and Respect', 'topic_icon': '🤝', 'topic_subtitle': 'Learning important values for life',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Showing Respect', 'emoji': '🙏', 'order': 1,
                     'content': '''Respect means treating others the way you want to be treated.

How to show respect:

To parents and elders 👴👵
- Greet them politely: "Good morning, Mum!"
- Listen when they speak
- Help with chores
- Say "please" and "thank you"

To teachers 👩‍🏫
- Greet them at the door
- Listen in class
- Do your homework
- Raise your hand to speak

To friends and classmates 👫
- Share with others
- Do not bully or tease
- Be kind and helpful
- Apologize when wrong

To yourself 💚
- Take care of your body
- Do your best
- Believe in yourself
- Stay clean and neat

The Golden Rule: "Treat others as you want to be treated."''',
                     'key_points': json.dumps([
                         'Respect means treating others well',
                         'Greet elders and teachers politely',
                         'Share with friends and be kind',
                         'Respect yourself by doing your best',
                         'The Golden Rule: treat others how you want to be treated'
                     ]),
                     'examples': json.dumps([
                         'Q: How do you show respect to a teacher? A: Greet them, listen, raise hand',
                         'Q: What is the Golden Rule? A: Treat others as you want to be treated',
                         'Q: Why is saying "please" important? A: It shows politeness and respect'
                     ]),
                     'did_you_know': 'In many Kenyan cultures, children greet elders by bowing or kneeling as a sign of respect!',
                     'definition': 'Respect is treating others with kindness, consideration, and honor.'}
                ]
            })

    # ============================================================
    # CREATIVE ARTS
    # ============================================================
    if 'Creative Arts' in subjects:
        ca = subjects['Creative Arts']

        if 'G2' in grades:
            content.append({
                'subject': ca, 'grade': grades['G2'],
                'topic_title': 'Drawing and Coloring', 'topic_icon': '🎨', 'topic_subtitle': 'Expressing ourselves through art',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Basic Drawing Skills', 'emoji': '✏️', 'order': 1,
                     'content': '''Drawing is fun! Everyone can draw - you just need to practice!

Basic shapes to practice:
🔴 Circle - round like a ball
⬛ Square - four equal sides
🔺 Triangle - three sides
⭐ Star - five points

How to draw simple things:

A tree 🌳
1. Draw a brown rectangle (trunk)
2. Draw a green circle on top (leaves)
3. Add some details

A house 🏠
1. Draw a square (walls)
2. Draw a triangle on top (roof)
3. Draw a small square (door)
4. Draw two small squares (windows)

A flower 🌸
1. Draw a circle (center)
2. Draw petals around it
3. Draw a line down (stem)
4. Add leaves

Remember: Practice makes progress, not perfection!''',
                     'key_points': json.dumps([
                         'Start with basic shapes',
                         'Simple drawings start with circles, squares, triangles',
                         'Practice every day to improve',
                         'There is no "wrong" in art - be creative!',
                         'Use your imagination'
                     ]),
                     'examples': json.dumps([
                         'Q: What shapes do you need to draw a house? A: Square and triangle',
                         'Q: What colors are a tree? A: Brown trunk, green leaves',
                         'Q: What can you draw? A: (Encourage creativity!)'
                     ]),
                     'did_you_know': 'The world\'s most famous painting, the Mona Lisa, is kept behind bulletproof glass in France!'}
                ]
            })

    # Now write all content to database
    print('Seeding CBC content...')
    created_count = 0
    for item in content:
        subj = item['subject']
        grade = item['grade']

        existing_topic = Topic.query.filter_by(
            subject_id=subj.id, grade_id=grade.id,
            title=item['topic_title']
        ).first()
        if existing_topic:
            continue

        topic = Topic(
            subject_id=subj.id, grade_id=grade.id,
            title=item['topic_title'], icon=item['topic_icon'],
            subtitle=item['topic_subtitle'],
            difficulty=item.get('difficulty', 'easy'),
            order_number=item['order']
        )
        db.session.add(topic)
        db.session.flush()

        for lesson_data in item['lessons']:
            lesson = Lesson(
                topic_id=topic.id,
                title=lesson_data['title'],
                content=lesson_data['content'],
                key_points=lesson_data.get('key_points', '[]'),
                examples=lesson_data.get('examples', '[]'),
                did_you_know=lesson_data.get('did_you_know', ''),
                definition=lesson_data.get('definition', ''),
                image_emoji=lesson_data.get('emoji', '📖'),
                order_number=lesson_data['order'],
                points_earned=lesson_data.get('points_earned', 15)
            )
            db.session.add(lesson)
            created_count += 1

    db.session.commit()
    print(f'  Created {created_count} lessons across {len(content)} topics')
    return created_count
