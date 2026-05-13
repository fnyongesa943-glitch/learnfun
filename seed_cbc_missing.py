"""
Seed CBC content for grades that currently have no topics/lessons:
PP1, PP2, G5, G6, G7, G8, G9
"""
import json


def seed_missing_content(db, Grade, Subject, Topic, Lesson):
    grades = {g.level_code: g for g in Grade.query.all()}
    subjects = {s.name: s for s in Subject.query.all()}
    content = []

    # ============================================================
    # PRE-PRIMARY 1 (PP1) - ~age 4
    # ============================================================

    if 'PP1' in grades:
        g = grades['PP1']

        if 'Mathematics' in subjects:
            s = subjects['Mathematics']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Counting 1 to 10', 'topic_icon': '🔢',
                'topic_subtitle': 'Learning to count from 1 to 10',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Numbers 1 to 5', 'emoji': '1️⃣', 'order': 1,
                     'content': 'Let us learn to count from 1 to 5!\n\n1 - One 🖐️ (one finger)\n2 - Two 🖐️🖐️ (two fingers)\n3 - Three\n4 - Four\n5 - Five\n\nCount your fingers: 1, 2, 3, 4, 5!\n\nPractice counting toys, spoons, or anything around you.',
                     'key_points': json.dumps(['Numbers 1 to 5 help us count', 'Use your fingers to count', 'Practice every day']),
                     'examples': json.dumps(['Q: Count 1,2,? A: 3', 'Q: How many eyes do you have? A: 2', 'Q: Count your fingers on one hand. A: 5']),
                     'did_you_know': 'Your fingers are the best counting tools!', 'definition': 'Counting means saying numbers in order.'},
                    {'title': 'Numbers 6 to 10', 'emoji': '🔢', 'order': 2,
                     'content': 'Now let us count from 6 to 10!\n\n6 - Six\n7 - Seven\n8 - Eight\n9 - Nine\n10 - Ten\n\nCount with both hands: 6, 7, 8, 9, 10!\n\nPractice counting your toes too. You have 10 toes!',
                     'key_points': json.dumps(['6 to 10 come after 5', 'Use both hands to count to 10', 'Practice counting every day']),
                     'examples': json.dumps(['Q: What comes after 5? A: 6', 'Q: How many fingers on two hands? A: 10', 'Q: Count from 1 to 10']),
                     'did_you_know': 'A group of 10 is called a "ten"!', 'definition': 'Ten is the number of fingers on two hands.'}
                ]
            })

        if 'English' in subjects:
            s = subjects['English']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'First Words', 'topic_icon': '🔤',
                'topic_subtitle': 'Simple words and sounds for beginners',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Greetings', 'emoji': '👋', 'order': 1,
                     'content': 'Let us learn greeting words!\n\nHello! 👋 - Say this when you meet someone\nGoodbye! 🖐️ - Say this when you leave\nThank you! 🙏 - Say this when someone helps you\nPlease - Say this when you ask for something\nSorry - Say this when you make a mistake\n\nPractice: "Hello, my name is..."',
                     'key_points': json.dumps(['Hello means hi', 'Goodbye means bye', 'Thank you shows gratitude', 'Please shows manners']),
                     'examples': json.dumps(['Q: What do you say when you meet someone? A: Hello', 'Q: What do you say when leaving? A: Goodbye', 'Q: When do you say thank you? A: When someone helps you']),
                     'did_you_know': 'Saying please and thank you makes people happy!', 'definition': 'Greetings are words we use to be friendly.'},
                    {'title': 'Colors', 'emoji': '🌈', 'order': 2,
                     'content': 'Let us learn colors!\n\nRed 🔴 - like an apple\nBlue 🔵 - like the sky\nYellow 🟡 - like the sun\nGreen 🟢 - like grass\nBlack ⚫ - like night\nWhite ⚪ - like clouds\n\nLook around and name the colors you see!',
                     'key_points': json.dumps(['Red, blue, yellow, green are colors', 'Colors make our world beautiful', 'Point to things and say their color']),
                     'examples': json.dumps(['Q: What color is the sky? A: Blue', 'Q: What color is grass? A: Green', 'Q: What color is an apple? A: Red or green']),
                     'did_you_know': 'Rainbow has 7 colors: red, orange, yellow, green, blue, indigo, violet!', 'definition': 'A color is what we see when light hits an object.'}
                ]
            })

        if 'Science & Technology' in subjects:
            s = subjects['Science & Technology']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Exploring My World', 'topic_icon': '🌍',
                'topic_subtitle': 'Learning about things around us',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'My Body', 'emoji': '🧍', 'order': 1,
                     'content': 'Your body is amazing! Let us learn its parts.\n\nHead 🧠 - where your brain is\nEyes 👀 - for seeing\nEars 👂 - for hearing\nNose 👃 - for smelling\nMouth 👄 - for eating and speaking\nHands ✋ - for touching and holding\nFeet 🦶 - for walking and running\n\nTouch each part as you say its name!',
                     'key_points': json.dumps(['We have many body parts', 'Each body part has a job', 'Keep your body clean and healthy']),
                     'examples': json.dumps(['Q: What do you use to see? A: Eyes', 'Q: What do you use to hear? A: Ears', 'Q: What do you use to walk? A: Feet']),
                     'did_you_know': 'Your nose can smell over 1 trillion different scents!', 'definition': 'The body is made of many parts that work together.'},
                    {'title': 'The Five Senses', 'emoji': '🧠', 'order': 2,
                     'content': 'We have five senses that help us explore the world!\n\n👁️ Sight (eyes) - we see colors, shapes, and light\n👂 Hearing (ears) - we hear sounds and music\n👃 Smell (nose) - we smell flowers and food\n👅 Taste (tongue) - we taste sweet, sour, salty\n✋ Touch (skin) - we feel hot, cold, soft, hard\n\nTry using all your senses today!',
                     'key_points': json.dumps(['We have 5 senses', 'Senses help us learn about the world', 'Each sense uses a different body part']),
                     'examples': json.dumps(['Q: Which sense do you use to smell? A: Nose', 'Q: Which sense do you use to see? A: Eyes', 'Q: How do you know if food is sweet? A: Taste']),
                     'did_you_know': 'Your tongue has about 10,000 taste buds!', 'definition': 'Senses are how we experience the world around us.'}
                ]
            })

        if 'Hygiene & Nutrition' in subjects:
            s = subjects['Hygiene & Nutrition']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Keeping Clean', 'topic_icon': '🧼',
                'topic_subtitle': 'Simple hygiene for little learners',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Washing Hands', 'emoji': '🧼', 'order': 1,
                     'content': 'Washing hands keeps germs away!\n\nWhen to wash hands:\n- Before eating 🍽️\n- After toilet 🚽\n- After playing 🎮\n- When dirty 🖐️\n\nSteps:\n1. Wet hands\n2. Use soap\n3. Rub together\n4. Rinse clean\n5. Dry with towel\n\nSing a song while washing!',
                     'key_points': json.dumps(['Wash hands before eating', 'Use soap and water', 'Wash for 20 seconds', 'Dry hands well']),
                     'examples': json.dumps(['Q: When do you wash hands? A: Before eating, after toilet', 'Q: What do you use with water? A: Soap', 'Q: Why do we wash hands? A: To remove germs']),
                     'did_you_know': 'Germs are so tiny you cannot see them but they are everywhere!', 'definition': 'Hygiene means keeping your body clean.'},
                    {'title': 'Bathing and Teeth', 'emoji': '🛁', 'order': 2,
                     'content': 'Keeping your body clean every day!\n\nBathing 🛁\n- Bathe every day\n- Use soap and water\n- Wash your whole body\n- Wear clean clothes after\n\nBrushing teeth 🪥\n- Brush in the morning\n- Brush at night\n- Use a little toothpaste\n- Brush all your teeth\n\nClean body = healthy and happy!',
                     'key_points': json.dumps(['Bathe every day', 'Brush teeth twice a day', 'Wear clean clothes', 'Being clean feels good']),
                     'examples': json.dumps(['Q: How often should you bathe? A: Every day', 'Q: When do you brush teeth? A: Morning and night', 'Q: Why do we wear clean clothes? A: To stay clean and fresh']),
                     'did_you_know': 'Your toothbrush should be changed every 3 months!', 'definition': 'Cleanliness keeps us healthy and happy.'}
                ]
            })

    # ============================================================
    # PRE-PRIMARY 2 (PP2) - ~age 5
    # ============================================================

    if 'PP2' in grades:
        g = grades['PP2']

        if 'Mathematics' in subjects:
            s = subjects['Mathematics']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Numbers up to 20', 'topic_icon': '🔢',
                'topic_subtitle': 'Counting and writing numbers to 20',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Counting 1 to 20', 'emoji': '🔢', 'order': 1,
                     'content': 'Let us count all the way to 20!\n\n1 to 10: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10\n11 to 20: 11, 12, 13, 14, 15, 16, 17, 18, 19, 20\n\nPractice:\n- Count your toys\n- Count steps as you walk\n- Count claps with a friend\n- Write numbers in sand or with chalk\n\nYou can do it!',
                     'key_points': json.dumps(['Count from 1 to 20 in order', 'Write numbers 1 to 20', 'Count objects around you']),
                     'examples': json.dumps(['Q: What comes after 10? A: 11', 'Q: Count from 1 to 10', 'Q: How many toes do you have? A: 20']),
                     'did_you_know': 'Twenty is the same as two groups of ten!', 'definition': 'Numbers help us know how many there are.'},
                    {'title': 'Simple Addition', 'emoji': '➕', 'order': 2,
                     'content': 'Addition means putting things together!\n\n1 + 1 = 2 (one apple plus one apple equals two apples) 🍎🍎\n2 + 1 = 3\n2 + 2 = 4\n3 + 1 = 4\n\nUse your fingers to add:\nPut up 2 fingers, then 1 more. How many? 3!\n\nAdding is fun!',
                     'key_points': json.dumps(['Addition means putting together', 'Use fingers to help add', 'Start with small numbers']),
                     'examples': json.dumps(['Q: 1 + 1 = ? A: 2', 'Q: 2 + 2 = ? A: 4', 'Q: 3 + 1 = ? A: 4']),
                     'did_you_know': 'The + sign means "put together"!', 'definition': 'Addition is putting groups together to find the total.'}
                ]
            })

        if 'English' in subjects:
            s = subjects['English']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Letters and Sounds', 'topic_icon': '🔤',
                'topic_subtitle': 'Learning the alphabet and phonics',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Letter A to L', 'emoji': '📖', 'order': 1,
                     'content': 'Learn the first letters of the alphabet!\n\nA a - /a/ Apple 🍎\nB b - /b/ Ball ⚽\nC c - /k/ Cat 🐱\nD d - /d/ Dog 🐶\nE e - /e/ Egg 🥚\nF f - /f/ Fish 🐟\nG g - /g/ Goat 🐐\nH h - /h/ Hat 🎩\nI i - /i/ Ink 🖊️\nJ j - /j/ Jug 🧃\nK k - /k/ Kite 🪁\nL l - /l/ Lion 🦁\n\nSay each sound out loud!',
                     'key_points': json.dumps(['A to L are the first 12 letters', 'Each letter makes a sound', 'Practice saying letter sounds']),
                     'examples': json.dumps(['Q: What sound does B make? A: /b/', 'Q: What letter starts "cat"? A: C', 'Q: What comes after D? A: E']),
                     'did_you_know': 'The word "alphabet" comes from the first two Greek letters: alpha and beta!', 'definition': 'A letter is a symbol that stands for a sound.'},
                    {'title': 'Letter M to Z', 'emoji': '📖', 'order': 2,
                     'content': 'Now learn the rest of the alphabet!\n\nM m - /m/ Moon 🌙\nN n - /n/ Nest 🪺\nO o - /o/ Orange 🍊\nP p - /p/ Pig 🐷\nQ q - /kw/ Queen 👑\nR r - /r/ Rainbow 🌈\nS s - /s/ Sun ☀️\nT t - /t/ Tree 🌳\nU u - /u/ Umbrella ☂️\nV v - /v/ Van 🚐\nW w - /w/ Water 💧\nX x - /ks/ Fox 🦊\nY y - /y/ Yellow 💛\nZ z - /z/ Zebra 🦓\n\nGreat job! You know all 26 letters!',
                     'key_points': json.dumps(['M to Z complete the alphabet', 'There are 26 letters total', 'Sing the alphabet song to remember']),
                     'examples': json.dumps(['Q: What is the last letter? A: Z', 'Q: What comes after T? A: U', 'Q: What letter starts "sun"? A: S']),
                     'did_you_know': 'The letter E is used the most in English!', 'definition': 'The alphabet has 26 letters from A to Z.'}
                ]
            })

        if 'Hygiene & Nutrition' in subjects:
            s = subjects['Hygiene & Nutrition']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Healthy Habits', 'topic_icon': '🍎',
                'topic_subtitle': 'Eating well and staying healthy',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Healthy Foods', 'emoji': '🍎', 'order': 1,
                     'content': 'Food gives us energy to play and learn!\n\nHealthy foods:\n🍎 Fruits - apples, bananas, oranges, mangoes\n🥬 Vegetables - sukuma wiki, carrots, spinach\n🥛 Milk - for strong bones\n🥚 Eggs - for strong muscles\n🍚 Ugali and rice - for energy\n\nTry to eat fruits and vegetables every day!',
                     'key_points': json.dumps(['Fruits and vegetables are healthy', 'Milk makes bones strong', 'Food gives us energy', 'Eat different foods every day']),
                     'examples': json.dumps(['Q: Name a healthy fruit. A: Apple, banana, mango', 'Q: What food gives energy? A: Ugali, rice, bread', 'Q: Why do we eat vegetables? A: To stay healthy and strong']),
                     'did_you_know': 'Carrots help you see better at night!', 'definition': 'Healthy food helps our bodies grow and stay strong.'},
                    {'title': 'Drinking Water', 'emoji': '💧', 'order': 2,
                     'content': 'Water is very important for our bodies!\n\nWhy drink water?\n💧 Keeps us from getting thirsty\n💧 Helps our body work well\n💧 Gives us energy\n💧 Keeps our skin healthy\n💧 Helps us think better\n\nDrink water:\n- When you wake up\n- During play time\n- With meals\n- When you feel hot\n- When you are thirsty\n\nDrink at least 6 glasses of water every day!',
                     'key_points': json.dumps(['Drink water every day', 'Water keeps us healthy', 'Drink when you are thirsty', 'Water has no sugar - it is the best drink']),
                     'examples': json.dumps(['Q: Why should you drink water? A: To stay healthy', 'Q: When should you drink water? A: When thirsty, after playing', 'Q: How much water should you drink? A: At least 6 glasses daily']),
                     'did_you_know': 'Your body is about 60% water!', 'definition': 'Water is a clear liquid that all living things need.'}
                ]
            })

        if 'Environmental' in subjects:
            s = subjects['Environmental']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Our Environment', 'topic_icon': '🌿',
                'topic_subtitle': 'Taking care of our surroundings',
                'difficulty': 'easy', 'order': 1, 'lessons': [
                    {'title': 'Plants Around Us', 'emoji': '🌱', 'order': 1,
                     'content': 'Plants are living things that grow all around us!\n\nParts of a plant:\n🌱 Roots - hold the plant in the soil\n🌿 Stem - carries water up the plant\n🍃 Leaves - make food for the plant\n🌸 Flowers - make seeds for new plants\n🍎 Fruits - protect the seeds\n\nWhat plants need to grow:\n☀️ Sunlight\n💧 Water\n🌍 Soil\n🌬️ Air\n\nPlants give us food, medicine, and clean air!',
                     'key_points': json.dumps(['Plants have roots, stem, leaves, flowers', 'Plants need sun, water, soil, air', 'Plants give us food and oxygen', 'We should take care of plants']),
                     'examples': json.dumps(['Q: What do plants need to grow? A: Sun, water, soil, air', 'Q: What part is under the soil? A: Roots', 'Q: Name a plant you can eat. A: Sukuma wiki, spinach, maize']),
                     'did_you_know': 'Trees can live for hundreds of years! The oldest tree is over 5,000 years old.', 'definition': 'A plant is a living thing that grows in soil and makes its own food.'},
                    {'title': 'Caring for Animals', 'emoji': '🐕', 'order': 2,
                     'content': 'Animals are living things too! We should care for them.\n\nPets at home:\n🐕 Dogs - give them food and water, take them for walks\n🐱 Cats - feed them, give them a warm place to sleep\n🐦 Birds - clean their cage, give them seeds\n🐟 Fish - clean their tank, feed them daily\n\nFarm animals:\n🐄 Cows - give us milk\n🐔 Chickens - give us eggs\n🐐 Goats - give us meat and milk\n\nAlways be kind to animals!',
                     'key_points': json.dumps(['Animals need food and water', 'Pets need love and care', 'Farm animals give us food', 'Be kind to all animals']),
                     'examples': json.dumps(['Q: What do pets need? A: Food, water, love, shelter', 'Q: What does a cow give us? A: Milk', 'Q: How should we treat animals? A: With kindness']),
                     'did_you_know': 'Dogs can understand up to 250 words and gestures!', 'definition': 'Animals are living creatures that need care and respect.'}
                ]
            })

    # ============================================================
    # GRADE 5 - Upper Primary ~age 10
    # ============================================================

    if 'G5' in grades:
        g = grades['G5']

        if 'Mathematics' in subjects:
            s = subjects['Mathematics']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Decimals and Percentages', 'topic_icon': '💯',
                'topic_subtitle': 'Understanding tenths, hundredths and percentages',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Introduction to Decimals', 'emoji': '🔢', 'order': 1,
                     'content': 'Decimals are another way to write fractions!\n\nA decimal has a decimal point (.) that separates whole numbers from parts.\n\n0.5 means half (1/2)\n0.25 means one quarter (1/4)\n0.75 means three quarters (3/4)\n0.1 means one tenth (1/10)\n\nExamples:\n- 1.5 = 1 whole and 5 tenths\n- 2.75 = 2 wholes and 75 hundredths\n- 0.33 = 33 hundredths\n\nWhen you see money in Kenya Shillings, you are using decimals!\nKSh 50.50 means 50 shillings and 50 cents.',
                     'key_points': json.dumps(['Decimals use a decimal point', '0.5 is the same as 1/2', 'Decimals show parts of a whole', 'Money uses decimals']),
                     'examples': json.dumps(['Q: What is 0.5 as a fraction? A: 1/2', 'Q: Write one quarter as a decimal. A: 0.25', 'Q: What is larger: 0.5 or 0.25? A: 0.5']),
                     'did_you_know': 'The decimal system was invented by Simon Stevin in 1585!', 'definition': 'A decimal is a number with a decimal point showing parts of a whole.'},
                    {'title': 'Percentages', 'emoji': '📊', 'order': 2,
                     'content': 'Percent (%) means "out of 100".\n\n100% = the whole thing\n50% = half (50 out of 100)\n25% = one quarter (25 out of 100)\n75% = three quarters (75 out of 100)\n10% = one tenth (10 out of 100)\n\nConverting:\n50% = 0.5 = 1/2\n25% = 0.25 = 1/4\n75% = 0.75 = 3/4\n100% = 1.0 = whole\n\nIf you score 80 out of 100 on a test, you scored 80%!',
                     'key_points': json.dumps(['Percent means out of 100', '% symbol means percent', '100% is the whole thing', 'Percentages are used everywhere']),
                     'examples': json.dumps(['Q: What does 50% mean? A: 50 out of 100, or half', 'Q: Convert 25% to a decimal. A: 0.25', 'Q: If you get 90/100, what percent is that? A: 90%']),
                     'did_you_know': 'The % symbol came from the Italian word "per cento" meaning "per hundred"!', 'definition': 'A percentage is a number or ratio expressed as a fraction of 100.'}
                ]
            })

        if 'English' in subjects:
            s = subjects['English']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Grammar and Composition', 'topic_icon': '📝',
                'topic_subtitle': 'Improving writing and grammar skills',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Parts of Speech', 'emoji': '📚', 'order': 1,
                     'content': 'Words have different jobs in sentences. These are called parts of speech.\n\nNouns - naming words (boy, Nairobi, book, happiness)\nPronouns - replace nouns (he, she, it, they, we)\nVerbs - action words (run, eat, sleep, think)\nAdjectives - describe nouns (big, red, beautiful, tall)\nAdverbs - describe verbs (quickly, softly, well)\nPrepositions - show position (in, on, under, between)\nConjunctions - join words (and, but, or)\n\nIn a sentence: "The tall boy quickly ran to school."\n- "boy" = noun\n- "tall" = adjective\n- "quickly" = adverb\n- "ran" = verb\n- "to" = preposition',
                     'key_points': json.dumps(['Nouns name people, places, things', 'Verbs show action', 'Adjectives describe nouns', 'Adverbs describe verbs', 'Every word has a job']),
                     'examples': json.dumps(['Q: Find the noun: "The dog barks." A: dog', 'Q: Find the verb: "She sings." A: sings', 'Q: Find the adjective: "A red ball." A: red']),
                     'did_you_know': 'There are 8 main parts of speech in English grammar!', 'definition': 'Parts of speech are categories of words based on their function.'},
                    {'title': 'Writing a Paragraph', 'emoji': '✏️', 'order': 2,
                     'content': 'A paragraph is a group of sentences about one idea.\n\nStructure of a paragraph:\n1. Topic sentence - tells what the paragraph is about\n2. Supporting sentences - give details and examples\n3. Concluding sentence - wraps up the idea\n\nExample paragraph:\n"My favourite animal is the elephant. Elephants are the largest land animals on Earth. They have long trunks that they use to eat and drink. Elephants are very intelligent and can remember things for many years. I think elephants are amazing creatures."\n\nTips:\n- Indent the first line\n- Stay on topic\n- Use complete sentences\n- End with punctuation',
                     'key_points': json.dumps(['A paragraph is about one idea', 'Begin with a topic sentence', 'Add supporting details', 'End with a concluding sentence']),
                     'examples': json.dumps(['Q: What is a topic sentence? A: The sentence that tells the main idea', 'Q: How many ideas in one paragraph? A: One main idea', 'Q: Write a topic sentence about your pet.']),
                     'did_you_know': 'The shortest paragraph ever written was just one word: "Go!"', 'definition': 'A paragraph is a group of sentences about a single topic.'}
                ]
            })

        if 'Science & Technology' in subjects:
            s = subjects['Science & Technology']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Energy and Forces', 'topic_icon': '⚡',
                'topic_subtitle': 'Understanding energy types and forces',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Types of Energy', 'emoji': '💡', 'order': 1,
                     'content': 'Energy makes things happen! Without energy, nothing would work.\n\nTypes of energy:\n☀️ Light energy - from the sun, bulbs, fire\n🔊 Sound energy - from voices, music, animals\n🔥 Heat energy - from fire, sun, friction\n⚡ Electrical energy - from batteries, power lines\n💪 Kinetic energy - energy of movement\n🌀 Wind energy - moving air turns turbines\n\nEnergy can change from one form to another!\n- A radio changes electrical energy to sound energy\n- A light bulb changes electrical energy to light\n- Firewood changes chemical energy to heat',
                     'key_points': json.dumps(['Energy makes things happen', 'Energy comes in many forms', 'Energy can change form', 'The sun is our main energy source']),
                     'examples': json.dumps(['Q: Name one type of energy. A: Light, sound, heat, electrical', 'Q: What gives us light energy? A: Sun, light bulbs', 'Q: What does a radio do? A: Changes electrical to sound energy']),
                     'did_you_know': 'The sun gives us more energy in one hour than the world uses in a whole year!', 'definition': 'Energy is the ability to do work or cause change.'},
                    {'title': 'Forces and Motion', 'emoji': '🏋️', 'order': 2,
                     'content': 'A force is a push or a pull that makes things move, stop, or change direction.\n\nTypes of forces:\n- Gravity - pulls things down toward Earth 🍎\n- Friction - slows things down (rubbing) 🛑\n- Magnetic force - attracts or repels magnets 🧲\n- Buoyancy - pushes things up in water 🚤\n\nNewton\'s Laws:\n1. Things keep moving unless a force stops them\n2. Force = mass x acceleration\n3. Every action has an equal reaction\n\nExamples of forces in daily life:\n- Pushing a door open\n- A ball falling down (gravity)\n- A car stopping (friction from brakes)\n- A magnet picking up a nail',
                     'key_points': json.dumps(['A force is a push or pull', 'Gravity pulls things down', 'Friction slows things down', 'Forces make things move, stop, or change']),
                     'examples': json.dumps(['Q: What force pulls things to the ground? A: Gravity', 'Q: What makes it hard to slide on carpet? A: Friction', 'Q: What does a magnet do? A: Attracts metal objects']),
                     'did_you_know': 'Astronauts float in space because there is very little gravity!', 'definition': 'A force is a push or pull that can change an object\'s motion.'}
                ]
            })

        if 'Social Studies' in subjects:
            s = subjects['Social Studies']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Governance in Kenya', 'topic_icon': '🏛️',
                'topic_subtitle': 'How Kenya is governed',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'The Government of Kenya', 'emoji': '🏛️', 'order': 1,
                     'content': 'Kenya has a government that leads and takes care of the country.\n\nThree arms of government:\n\n1. Legislature (Parliament) 📜\n   - Makes laws for the country\n   - Has two houses: National Assembly and Senate\n   - Members are elected by citizens\n\n2. Executive (President and Cabinet) 👔\n   - Implements laws\n   - Headed by the President\n   - Includes Cabinet Secretaries\n\n3. Judiciary (Courts) ⚖️\n   - Interprets laws\n   - Headed by the Chief Justice\n   - Ensures justice for all\n\nKenya has 47 counties, each with its own county government led by a Governor.',
                     'key_points': json.dumps(['Kenya has three arms of government', 'Legislature makes laws', 'Executive implements laws', 'Judiciary interprets laws', 'Kenya has 47 counties']),
                     'examples': json.dumps(['Q: Who heads the Executive? A: The President', 'Q: What does Parliament do? A: Makes laws', 'Q: How many counties does Kenya have? A: 47']),
                     'did_you_know': 'Kenya\'s Constitution was promulgated on August 27, 2010!', 'definition': 'Government is a group of people who run a country.'},
                    {'title': 'Citizenship and Rights', 'emoji': '🤝', 'order': 2,
                     'content': 'Being a Kenyan citizen comes with rights and responsibilities.\n\nRights of citizens:\n- Right to education 📚\n- Right to healthcare 🏥\n- Right to vote 🗳️\n- Right to clean water 💧\n- Right to food 🍎\n- Right to protection 👮\n- Freedom of speech 🗣️\n\nResponsibilities:\n- Obey the law ⚖️\n- Pay taxes 💰\n- Vote in elections\n- Keep the environment clean 🧹\n- Help others 🤝\n- Respect other people\'s rights\n\nGood citizens make a great country!',
                     'key_points': json.dumps(['Citizens have rights and responsibilities', 'Every child has a right to education', 'We must obey the law', 'Good citizens help their community']),
                     'examples': json.dumps(['Q: Name one right of a citizen. A: Education, healthcare, voting', 'Q: Name one responsibility. A: Obey the law, keep clean', 'Q: Why is voting important? A: It lets citizens choose their leaders']),
                     'did_you_know': 'The Kenyan flag has four colors: black, red, green and white!', 'definition': 'A citizen is a person who belongs to a country and has rights and duties.'}
                ]
            })

        if 'CRE' in subjects:
            s = subjects['CRE']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'The Life of Jesus', 'topic_icon': '✝️',
                'topic_subtitle': 'Learning about the life and teachings of Jesus',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'The Birth of Jesus', 'emoji': '🌟', 'order': 1,
                     'content': 'The story of Jesus begins with a miraculous birth.\n\nMary, a young woman from Nazareth, was visited by the angel Gabriel. The angel told her she would give birth to God\'s son. Mary was afraid but trusted God.\n\nJoseph, Mary\'s husband, also had a dream where an angel told him to take Mary as his wife. The baby would be named Jesus, meaning "God saves."\n\nWhen it was time for the baby to be born, Mary and Joseph travelled to Bethlehem for a census. There was no room in the inn, so Jesus was born in a stable and laid in a manger (animal feeding trough).\n\nShepherds in the fields saw a bright star and angels singing "Glory to God in the highest!" They came to worship the baby Jesus.\n\nWise men from the East followed the star and brought gifts: gold, frankincense, and myrrh.',
                     'key_points': json.dumps(['Jesus was born in Bethlehem', 'Mary was Jesus\' mother', 'Joseph was Jesus\' earthly father', 'Angels announced Jesus\' birth', 'Shepherds and wise men visited']),
                     'examples': json.dumps(['Q: Where was Jesus born? A: Bethlehem', 'Q: What gifts did the wise men bring? A: Gold, frankincense, myrrh', 'Q: What does the name Jesus mean? A: God saves']),
                     'did_you_know': 'Christmas (December 25) is celebrated as Jesus\' birthday!', 'definition': 'Jesus is the Son of God in Christian belief.'},
                    {'title': 'Jesus\' Teachings: Parables', 'emoji': '📖', 'order': 2,
                     'content': 'Jesus taught using stories called parables. These stories have important lessons.\n\nThe Parable of the Good Samaritan:\nA man was attacked by robbers and left hurt on the road. A priest and a Levite passed by without helping. But a Samaritan (someone from a different group) stopped and helped the man, took him to an inn, and paid for his care.\n\nLesson: Love your neighbor as yourself. Everyone is your neighbor, even people different from you.\n\nThe Parable of the Prodigal Son:\nA son asked his father for his share of money and left home. He wasted all the money. When he returned home ashamed, his father ran to welcome him and threw a big party.\n\nLesson: God always welcomes us back when we are sorry for our mistakes.',
                     'key_points': json.dumps(['Jesus taught using parables (stories)', 'The Good Samaritan teaches us to help everyone', 'The Prodigal Son shows God\'s forgiveness', 'Parables have deep meanings']),
                     'examples': json.dumps(['Q: Why did Jesus use parables? A: To teach lessons through stories', 'Q: What does the Good Samaritan teach? A: Help everyone, even strangers', 'Q: What does the Prodigal Son teach? A: God always forgives us']),
                     'did_you_know': 'Jesus told at least 30 parables recorded in the Bible!', 'definition': 'A parable is a simple story used to teach a moral or spiritual lesson.'}
                ]
            })

    # ============================================================
    # GRADE 6 - Upper Primary ~age 11
    # ============================================================

    if 'G6' in grades:
        g = grades['G6']

        if 'Mathematics' in subjects:
            s = subjects['Mathematics']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Ratios and Proportions', 'topic_icon': '⚖️',
                'topic_subtitle': 'Comparing quantities using ratios',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Understanding Ratios', 'emoji': '📊', 'order': 1,
                     'content': 'A ratio compares two quantities. It shows how much of one thing there is compared to another.\n\nWriting ratios:\n- Using a colon: 3:2 (read as "three to two")\n- As a fraction: 3/2\n- Using words: "3 to 2"\n\nExamples:\n- If there are 4 apples and 2 oranges, the ratio of apples to oranges is 4:2 or 2:1\n- In a class of 30 students with 18 girls and 12 boys, the ratio of girls to boys is 18:12 or 3:2\n- A recipe uses 2 cups of flour to 1 cup of sugar (ratio 2:1)\n\nRatios can be simplified just like fractions!',
                     'key_points': json.dumps(['A ratio compares two quantities', 'Ratios can be written with : or as fractions', 'Ratios can be simplified', 'Ratios are used in recipes and everyday life']),
                     'examples': json.dumps(['Q: Write the ratio of 4 to 8 simplified. A: 1:2', 'Q: If there are 6 boys and 4 girls, what is the ratio? A: 6:4 or 3:2', 'Q: A recipe needs 3 eggs and 1 cup milk. What is the ratio? A: 3:1']),
                     'did_you_know': 'The word "ratio" comes from the Latin word "ratio" meaning "reason" or "calculation"!', 'definition': 'A ratio is a comparison of two quantities.'},
                    {'title': 'Proportions', 'emoji': '⚖️', 'order': 2,
                     'content': 'A proportion says that two ratios are equal.\n\nIf two ratios are equal, they form a proportion.\n\nExample: 1:2 = 2:4 = 3:6\nAll these ratios show the same relationship - half.\n\nSolving proportions:\nIf 2 apples cost KSh 40, how much do 5 apples cost?\n2:40 = 5:x\n2/40 = 5/x\nCross multiply: 2x = 200\nx = 100\nSo 5 apples cost KSh 100.\n\nProportions are used in:\n- Cooking (scaling recipes up or down)\n- Maps (scale shows proportion)\n- Shopping (unit prices)\n- Drawing (scale drawings)',
                     'key_points': json.dumps(['A proportion shows equal ratios', 'Cross multiply to solve proportions', 'Proportions are used in real life', 'Scaling up or down uses proportions']),
                     'examples': json.dumps(['Q: Are 1:3 and 2:6 in proportion? A: Yes', 'Q: If 3 pens cost 60, how much for 6 pens? A: 120', 'Q: A map scale 1cm:1km. How many km for 5cm? A: 5km']),
                     'did_you_know': 'The Golden Ratio (about 1.618) is found in art, architecture, and nature!', 'definition': 'A proportion is an equation showing two equal ratios.'}
                ]
            })

        if 'English' in subjects:
            s = subjects['English']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Reading Comprehension', 'topic_icon': '📖',
                'topic_subtitle': 'Understanding and analyzing texts',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Main Idea and Details', 'emoji': '📖', 'order': 1,
                     'content': 'Every text has a main idea - the most important point the author wants to share.\n\nFinding the main idea:\n- What is the text mostly about?\n- What is the author\'s message?\n- Look at the title and first sentence\n\nSupporting details:\n- Facts that explain the main idea\n- Examples that show the main idea\n- Reasons that prove the main idea\n\nExample:\n"Kenya has many national parks. The Maasai Mara is famous for the Great Migration. Amboseli has large elephant herds. Tsavo is the largest park. These parks protect our wildlife."\n\nMain idea: Kenya has many national parks that protect wildlife.\nDetails: Maasai Mara has migration, Amboseli has elephants, Tsavo is largest.',
                     'key_points': json.dumps(['The main idea is the most important point', 'Supporting details explain the main idea', 'Look at the title for clues', 'Ask yourself: what is this about?']),
                     'examples': json.dumps(['Q: What is a main idea? A: The most important point in a text', 'Q: What are supporting details? A: Facts that explain the main idea', 'Q: Find the main idea: "Birds have wings to fly." A: Birds are adapted for flight']),
                     'did_you_know': 'The main idea is sometimes called the "topic sentence" in a paragraph!', 'definition': 'The main idea is the central point or message of a text.'},
                    {'title': 'Inference and Prediction', 'emoji': '🔍', 'order': 2,
                     'content': 'Inference means reading "between the lines" - figuring out what the author does not say directly.\n\nMaking inferences:\n- Use clues from the text + your own knowledge\n- Ask: "What does this mean?"\n- Look for hints the author gives\n\nExample:\nText: "She grabbed her umbrella and raincoat before heading out."\nInference: It is raining or going to rain outside.\n\nMaking predictions:\n- Guess what will happen next\n- Use story clues and patterns\n- Check if your prediction was correct\n\nExample:\nText: "The boy put a seed in the soil and watered it every day."\nPrediction: A plant will grow from the seed.',
                     'key_points': json.dumps(['Inference means reading between the lines', 'Use text clues + your own knowledge', 'Predictions are educated guesses', 'Good readers infer and predict']),
                     'examples': json.dumps(['Q: What is an inference? A: Figuring out what is not directly stated', 'Q: Make an inference: "She put on warm boots and a scarf." A: It is cold outside', 'Q: What is a prediction? A: A guess about what will happen next']),
                     'did_you_know': 'Your brain makes thousands of inferences every day without you realizing it!', 'definition': 'An inference is a conclusion reached using evidence and reasoning.'}
                ]
            })

        if 'Science & Technology' in subjects:
            s = subjects['Science & Technology']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'The Solar System', 'topic_icon': '🌌',
                'topic_subtitle': 'Exploring planets, stars and space',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'The Planets', 'emoji': '🪐', 'order': 1,
                     'content': 'Our solar system has 8 planets orbiting the Sun.\n\nOrder from the Sun:\n1. Mercury ☿️ - smallest, closest to Sun, very hot\n2. Venus ♀️ - hottest planet, covered in clouds\n3. Earth 🌍 - our home, has water and life\n4. Mars ♂️ - the Red Planet\n5. Jupiter ♃ - largest planet, has a Great Red Spot\n6. Saturn ♄ - has beautiful rings\n7. Uranus ⛢ - rotates on its side\n8. Neptune ♆ - farthest, very cold and windy\n\nFun facts:\n- Jupiter is so large that 1,300 Earths could fit inside!\n- A day on Venus is longer than its year\n- Saturn\'s rings are made of ice and rock\n- Mars has the tallest mountain in the solar system (Olympus Mons)',
                     'key_points': json.dumps(['There are 8 planets in our solar system', 'Earth is the only known planet with life', 'Planets orbit the Sun', 'Each planet is unique']),
                     'examples': json.dumps(['Q: Which planet is closest to the Sun? A: Mercury', 'Q: Which planet has rings? A: Saturn', 'Q: Which planet is called the Red Planet? A: Mars']),
                     'did_you_know': 'A year on Jupiter is almost 12 Earth years long!', 'definition': 'A solar system is a star and all the planets and objects that orbit it.'},
                    {'title': 'The Sun, Moon and Stars', 'emoji': '☀️', 'order': 2,
                     'content': 'The Sun, Moon, and stars are amazing objects in our sky.\n\nThe Sun ☀️\n- A star at the center of our solar system\n- Made of hot gases (mostly hydrogen and helium)\n- Gives us light and heat\n- All planets orbit around it\n- Diameter: 109 times wider than Earth\n\nThe Moon 🌙\n- Earth\'s only natural satellite\n- Orbits Earth every 27.3 days\n- Has no atmosphere or water\n- Causes tides in the oceans\n- First visited by astronauts in 1969\n\nStars ✨\n- Huge balls of hot gas like our Sun\n- Look tiny because they are very far away\n- Billions of stars in our galaxy (Milky Way)\n- Some stars are much bigger than our Sun',
                     'key_points': json.dumps(['The Sun is a star at the center of our solar system', 'The Moon orbits Earth', 'Stars are suns very far away', 'The Sun gives us light and heat']),
                     'examples': json.dumps(['Q: What is the Sun? A: A star', 'Q: How often does the Moon orbit Earth? A: About 27 days', 'Q: Why do stars look tiny? A: They are very far away']),
                     'did_you_know': 'The Sun is so big that 1.3 million Earths could fit inside it!', 'definition': 'A star is a huge ball of hot gas that produces light and heat.'}
                ]
            })

        if 'Agriculture' in subjects:
            s = subjects['Agriculture']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Farm Animals', 'topic_icon': '🐄',
                'topic_subtitle': 'Raising and caring for livestock',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Common Farm Animals', 'emoji': '🐄', 'order': 1,
                     'content': 'Farm animals (livestock) are raised for food, milk, wool, and other products.\n\nCommon farm animals in Kenya:\n\n🐄 Cattle (cows)\n- Give us milk (dairy) and meat (beef)\n- Breeds: Friesian, Ayrshire, Zebu, Boran\n- Need good pasture, water, and shelter\n\n🐐 Goats\n- Give milk, meat, and skin/leather\n- Breeds: Galla, Toggenburg, Small East African\n- Can survive in dry areas\n\n🐑 Sheep\n- Give meat (mutton) and wool\n- Breeds: Dorper, Red Maasai, Merino\n- Good for small farms\n\n🐔 Chickens\n- Give eggs and meat\n- Breeds: Layers (for eggs), Broilers (for meat), Kienyeji (local)\n- Need a safe coop and proper feeding',
                     'key_points': json.dumps(['Cattle give milk and meat', 'Goats are hardy and give milk', 'Sheep give wool and meat', 'Chickens give eggs and meat']),
                     'examples': json.dumps(['Q: What product do cows give? A: Milk and meat', 'Q: What chicken breeds do you know? A: Layers, Broilers, Kienyeji', 'Q: Why are goats good for dry areas? A: They can survive with less water']),
                     'did_you_know': 'A cow can produce up to 30 liters of milk per day!', 'definition': 'Livestock are domestic animals raised on a farm for products.'},
                    {'title': 'Caring for Farm Animals', 'emoji': '🧑‍🌾', 'order': 2,
                     'content': 'Farm animals need proper care to stay healthy and productive.\n\nShelter 🏠\n- Protection from sun, rain, and cold\n- Clean and dry sleeping area\n- Good ventilation\n- Enough space for each animal\n\nFeeding 🍽️\n- Fresh water every day\n- Balanced diet (grass, hay, supplements)\n- Feed at regular times\n- Salt licks for minerals\n\nHealth 🩺\n- Vaccinations on schedule\n- Clean living area to prevent disease\n- Check for ticks and treat them\n- Call a vet when animals are sick\n- Deworm regularly\n\nA happy animal is a healthy and productive animal!',
                     'key_points': json.dumps(['Animals need clean shelter', 'Fresh water and good food are essential', 'Vaccinations prevent diseases', 'Clean housing keeps animals healthy']),
                     'examples': json.dumps(['Q: What do farm animals need daily? A: Fresh water and food', 'Q: Why vaccinate animals? A: To prevent diseases', 'Q: What is a zero-grazing unit? A: A fenced area where cows are kept for feeding']),
                     'did_you_know': 'Chickens can recognize over 100 different faces of their flock members!', 'definition': 'Animal husbandry is the care and breeding of farm animals.'}
                ]
            })

    # ============================================================
    # GRADE 7 - Junior Secondary ~age 12
    # ============================================================

    if 'G7' in grades:
        g = grades['G7']

        if 'Mathematics' in subjects:
            s = subjects['Mathematics']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Algebraic Expressions', 'topic_icon': '✖️',
                'topic_subtitle': 'Introduction to algebra and equations',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Variables and Expressions', 'emoji': '🔤', 'order': 1,
                     'content': 'Algebra uses letters to represent unknown numbers. These letters are called variables.\n\nExamples:\n- x + 3 = 7 (x is the variable, we need to find its value)\n- 2y = 10 (y is the variable)\n- a + b = c (a, b, c are all variables)\n\nAn algebraic expression combines numbers, variables, and operations.\n\nExpressions vs Equations:\n- Expression: 3x + 2 (no equals sign)\n- Equation: 3x + 2 = 11 (has an equals sign)\n\nEvaluating expressions:\nIf x = 5, what is 3x + 2?\n3(5) + 2 = 15 + 2 = 17\n\nSimplifying:\n- Like terms can be combined\n- 2x + 3x = 5x\n- 4y + 2 - y + 3 = 3y + 5',
                     'key_points': json.dumps(['Variables are letters that stand for numbers', 'An expression has no equals sign', 'An equation has an equals sign', 'Combine like terms to simplify']),
                     'examples': json.dumps(['Q: What is a variable? A: A letter representing an unknown number', 'Q: Simplify 2x + 3x. A: 5x', 'Q: Evaluate 2x + 1 when x = 4. A: 9']),
                     'did_you_know': 'The word "algebra" comes from the Arabic word "al-jabr" meaning "restoration"!', 'definition': 'Algebra is a branch of mathematics that uses letters to represent numbers.'},
                    {'title': 'Solving Equations', 'emoji': '⚖️', 'order': 2,
                     'content': 'Solving an equation means finding the value of the variable that makes the equation true.\n\nThink of an equation like a balance scale. Both sides must stay equal.\n\nTo solve x + 5 = 12:\n1. Get x alone on one side\n2. Subtract 5 from both sides\n3. x + 5 - 5 = 12 - 5\n4. x = 7\n\nTo solve 3x = 18:\n1. Divide both sides by 3\n2. 3x/3 = 18/3\n3. x = 6\n\nTwo-step equations:\n2x + 3 = 11\n1. Subtract 3: 2x = 8\n2. Divide by 2: x = 4\n\nCheck your answer: 2(4) + 3 = 8 + 3 = 11 ✓',
                     'key_points': json.dumps(['An equation is like a balance scale', 'Do the same operation on both sides', 'To isolate the variable, undo operations', 'Always check your answer']),
                     'examples': json.dumps(['Q: Solve x + 7 = 15. A: x = 8', 'Q: Solve 4x = 20. A: x = 5', 'Q: Solve 3x + 1 = 10. A: x = 3']),
                     'did_you_know': 'The equals sign (=) was invented by Robert Recorde in 1557!', 'definition': 'Solving an equation means finding the value that makes it true.'}
                ]
            })

        if 'English' in subjects:
            s = subjects['English']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Essay Writing', 'topic_icon': '✍️',
                'topic_subtitle': 'Structuring and writing essays',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Essay Structure', 'emoji': '📝', 'order': 1,
                     'content': 'An essay is a longer piece of writing on a specific topic.\n\nParts of an essay:\n\n1. Introduction 📌\n   - Hook the reader\'s attention\n   - Introduce the topic\n   - State your thesis (main argument)\n\n2. Body Paragraphs 📄\n   - Usually 3 paragraphs\n   - Each paragraph covers one main point\n   - Start with a topic sentence\n   - Give evidence and examples\n\n3. Conclusion 🔚\n   - Restate the thesis in different words\n   - Summarize main points\n   - Leave the reader with a final thought\n\nExample essay outline:\nTopic: "The Importance of Reading"\nIntroduction: Reading opens up new worlds and builds knowledge\nBody 1: Reading improves vocabulary and writing skills\nBody 2: Reading teaches us about different cultures\nBody 3: Reading reduces stress and improves focus\nConclusion: Everyone should make reading a daily habit',
                     'key_points': json.dumps(['An essay has three parts: intro, body, conclusion', 'The introduction hooks the reader', 'Each body paragraph covers one point', 'The conclusion summarizes the essay']),
                     'examples': json.dumps(['Q: What are the three parts of an essay? A: Introduction, body, conclusion', 'Q: What is a thesis? A: The main argument of the essay', 'Q: How many body paragraphs should an essay have? A: At least 3']),
                     'did_you_know': 'The word "essay" comes from the French word "essayer" meaning "to try"!', 'definition': 'An essay is a short piece of writing on a particular subject.'},
                    {'title': 'Persuasive Writing', 'emoji': '🎯', 'order': 2,
                     'content': 'Persuasive writing tries to convince the reader to agree with your point of view.\n\nTechniques of persuasion:\n\n1. Use strong arguments 🎯\n   - Give logical reasons\n   - Use facts and evidence\n   - Provide examples\n\n2. Appeal to emotions 💚\n   - Use emotional language\n   - Tell stories that connect\n   - Make the reader care\n\n3. Address counter-arguments 🔄\n   - Acknowledge other viewpoints\n   - Explain why your view is stronger\n\n4. Use rhetorical questions ❓\n   - "Don\'t we all want a better future?"\n   - "Isn\'t it time for change?"\n\n5. Call to action 📢\n   - Tell the reader what to do\n   - "Join us in making a difference!"',
                     'key_points': json.dumps(['Persuasive writing aims to convince', 'Use logical arguments and facts', 'Appeal to emotions', 'Address counter-arguments', 'End with a call to action']),
                     'examples': json.dumps(['Q: What is persuasive writing? A: Writing that aims to convince', 'Q: Name one persuasion technique. A: Emotional appeal, rhetorical questions', 'Q: What is a call to action? A: Telling the reader what to do']),
                     'did_you_know': 'The most persuasive speeches use a mix of logic, emotion, and credibility (ethos, pathos, logos)!', 'definition': 'Persuasion is the art of convincing others to agree with your viewpoint.'}
                ]
            })

        if 'Science & Technology' in subjects:
            s = subjects['Science & Technology']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Cells and Living Things', 'topic_icon': '🔬',
                'topic_subtitle': 'The building blocks of life',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Animal and Plant Cells', 'emoji': '🧬', 'order': 1,
                     'content': 'All living things are made of cells. Cells are the basic building blocks of life.\n\nParts of a cell (organelles):\n\nCell Membrane 🧱 - outer layer that controls what enters and leaves\nNucleus 🎯 - the control center, contains DNA\nCytoplasm 💧 - jelly-like substance where reactions happen\nMitochondria ⚡ - the power house, produces energy\nRibosomes 🔧 - make proteins\n\nPlant cells have extra parts:\nCell Wall 🧱 - rigid outer layer for support\nChloroplasts 🟢 - make food using sunlight (photosynthesis)\nVacuole 💧 - large storage for water\n\nDifferences between plant and animal cells:\n- Plant cells have cell wall, chloroplasts, large vacuole\n- Animal cells are usually rounder, plant cells are rectangular',
                     'key_points': json.dumps(['Cells are the basic unit of life', 'All living things are made of cells', 'Plant and animal cells have differences', 'The nucleus controls the cell']),
                     'examples': json.dumps(['Q: What is the control center of a cell? A: The nucleus', 'Q: What do chloroplasts do? A: Make food through photosynthesis', 'Q: Name one difference between plant and animal cells. A: Plant cells have a cell wall']),
                     'did_you_know': 'The human body has about 37 trillion cells!', 'definition': 'A cell is the smallest unit of a living organism.'},
                    {'title': 'Classification of Living Things', 'emoji': '🏷️', 'order': 2,
                     'content': 'Scientists classify (group) living things based on their characteristics.\n\nThe five kingdoms:\n\n1. Animalia (Animals) 🐘\n   - Can move, eat food, respond to environment\n   - Examples: mammals, birds, fish, insects\n\n2. Plantae (Plants) 🌿\n   - Make their own food (photosynthesis)\n   - Cannot move from place to place\n   - Examples: trees, flowers, grasses\n\n3. Fungi 🍄\n   - Absorb nutrients from surroundings\n   - Examples: mushrooms, mould, yeast\n\n4. Protista 🔬\n   - Mostly single-celled organisms\n   - Examples: amoeba, paramecium, algae\n\n5. Monera (Bacteria) 🦠\n   - Single-celled, no nucleus\n   - Found everywhere - soil, water, our bodies\n\nBinomial nomenclature: Each species has a two-part scientific name (e.g., Homo sapiens for humans)',
                     'key_points': json.dumps(['Living things are classified into 5 kingdoms', 'Animals cannot make their own food', 'Plants make food through photosynthesis', 'Fungi absorb nutrients', 'Bacteria are single-celled']),
                     'examples': json.dumps(['Q: How many kingdoms of living things? A: 5', 'Q: Which kingdom makes its own food? A: Plantae (plants)', 'Q: What kingdom do mushrooms belong to? A: Fungi']),
                     'did_you_know': 'There are about 8.7 million species on Earth, but only 1.2 million have been identified!', 'definition': 'Classification is the process of grouping living things by shared characteristics.'}
                ]
            })

        if 'Kiswahili' in subjects:
            s = subjects['Kiswahili']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Sarufi na Matumizi', 'topic_icon': '📝',
                'topic_subtitle': 'Kujifunza sarufi ya Kiswahili',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Ngeli za Kiswahili', 'emoji': '📚', 'order': 1,
                     'content': 'Kiswahili kina ngeli za nomino (noun classes). Kuna ngeli 8 kuu.\n\nNgeli za Kiswahili:\n\nM-WA (ngeli ya watu) 👥\n- Mtu / Watu (person/people)\n- Mtoto / Watoto (child/children)\n- Mwalimu / Walimu (teacher/teachers)\n\nM-MI 🏔️\n- Mti / Miti (tree/trees)\n- Mkate / Mikate (bread/breads)\n\nKI-VI 📦\n- Kitabu / Vitabu (book/books)\n- Kiti / Viti (chair/chairs)\n\nN-N 🐘\n- Nyumba / Nyumba (house/houses)\n- Ndizi / Ndizi (banana/bananas)\n\nJI-MA 🍊\n- Jina / Majina (name/names)\n- Jambo / Mambo (matter/matters)\n\nU-N 🔤\n- Uso / Nyuso (face/faces)\n\nPA (mahali) 📍\n- Hapa, Pale, Kule (here, there, over there)\n\nKU 🔄\n- Kuimba, Kucheza, Kula (to sing, to play, to eat)\n\nViwakilishi (prefixes) hubadilika kulingana na ngeli!',
                     'key_points': json.dumps(['Kiswahili kina ngeli 8 kuu', 'Ngeli huathiri viambishi awali', 'M-WA ni ngeli ya watu', 'KI-VI ni ngeli ya vitu vidogo']),
                     'examples': json.dumps(['Q: Mtoto wingi wake ni nini? A: Watoto', 'Q: Kitabu wingi wake ni nini? A: Vitabu', 'Q: Mti wingi wake ni nini? A: Miti']),
                     'did_you_know': 'Ngeli za Kiswahili ni tofauti na lugha nyingine za Kibantu!', 'definition': 'Ngeli ni makundi ya nomino katika Kiswahili.'},
                    {'title': 'Nyakati za Vitendo', 'emoji': '⏰', 'order': 2,
                     'content': 'Vitendo (verbs) hubadilika kulingana na wakati (tense).\n\nWakati uliopita (Past tense) - li-\n- Niliomba (I asked)\n- Alisoma (He/she read)\n- Tulicheza (We played)\n\nWakati uliopo (Present tense) - na-\n- Ninaomba (I ask)\n- Anasoma (He/she reads)\n- Tunacheza (We play)\n\nWakati ujao (Future tense) - ta-\n- Nitaomba (I will ask)\n- Atasoma (He/she will read)\n- Tutacheza (We will play)\n\nViambishi vya nafsi (Subject prefixes):\nNi- (I), U- (you), A- (he/she)\nTu- (we), M- (you pl), Wa- (they)\n\nMfano: Ni + na + som = Ninasoma (I am reading)',
                     'key_points': json.dumps(['Kiswahili kina nyakati tatu: lipo, liopo, lija', 'Ulipita = li-, Ulipo = na-, Ujao = ta-', 'Viambishi vya nafsi hubadilika']),
                     'examples': json.dumps(['Q: Nina soma ni wakati gani? A: Uliopo (present)', 'Q: Nilisoma ni wakati gani? A: Uliopita (past)', 'Q: Nitasoma ni wakati gani? A: Ujao (future)']),
                     'did_you_know': 'Kiswahili kina zaidi ya wakati 14 tofauti!', 'definition': 'Wakati unaonesha muda wa kitendo kutendeka.'}
                ]
            })

    # ============================================================
    # GRADE 8 - Junior Secondary ~age 13
    # ============================================================

    if 'G8' in grades:
        g = grades['G8']

        if 'Mathematics' in subjects:
            s = subjects['Mathematics']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Geometry and Measurement', 'topic_icon': '📐',
                'topic_subtitle': 'Angles, area, volume and measurement',
                'difficulty': 'hard', 'order': 1, 'lessons': [
                    {'title': 'Angles and Polygons', 'emoji': '📐', 'order': 1,
                     'content': 'An angle is formed when two lines meet at a point.\n\nTypes of angles:\n- Acute angle: less than 90° (sharp) 📐\n- Right angle: exactly 90° (L-shape) 📏\n- Obtuse angle: between 90° and 180° 📐\n- Straight angle: exactly 180° (straight line) 📏\n- Reflex angle: more than 180° 🔄\n\nTypes of polygons (many-sided shapes):\n- Triangle: 3 sides, angles add to 180°\n- Quadrilateral: 4 sides, angles add to 360°\n- Pentagon: 5 sides\n- Hexagon: 6 sides\n- Heptagon: 7 sides\n- Octagon: 8 sides\n- Nonagon: 9 sides\n- Decagon: 10 sides\n\nAngles in a triangle add up to 180°. Angles in a quadrilateral add up to 360°.',
                     'key_points': json.dumps(['Angles are measured in degrees', 'Angles can be acute, right, obtuse, straight, reflex', 'Polygons are named by their number of sides', 'Triangle angles sum to 180°']),
                     'examples': json.dumps(['Q: What angle is 90°? A: Right angle', 'Q: How many sides does a hexagon have? A: 6', 'Q: What is the sum of angles in any triangle? A: 180°']),
                     'did_you_know': 'The Pentagon building in the USA is shaped like a pentagon!', 'definition': 'Geometry is the study of shapes, sizes, and properties of space.'},
                    {'title': 'Area and Volume', 'emoji': '📦', 'order': 2,
                     'content': 'Area measures the surface of a 2D shape. Volume measures the space inside a 3D object.\n\nFormulas for area:\n- Square: A = s² (side × side)\n- Rectangle: A = l × w (length × width)\n- Triangle: A = ½ × b × h (base × height)\n- Circle: A = πr² (π × radius²)\n- Parallelogram: A = b × h\n- Trapezium: A = ½(a + b)h\n\nFormulas for volume:\n- Cube: V = s³\n- Cuboid: V = l × w × h\n- Cylinder: V = πr²h\n- Cone: V = ⅓πr²h\n- Sphere: V = ⁴⁄₃πr³\n\nSurface area is the total area of all the faces of a 3D object.',
                     'key_points': json.dumps(['Area measures 2D surfaces', 'Volume measures 3D space', 'Each shape has its own formula', 'Use the correct units (cm², m², cm³, m³)']),
                     'examples': json.dumps(['Q: What is the area of a 4cm square? A: 16cm²', 'Q: Formula for volume of a cuboid? A: l × w × h', 'Q: What units for volume? A: Cubic units (cm³, m³)']),
                     'did_you_know': 'The word "geometry" comes from Greek meaning "earth measurement"!', 'definition': 'Area is the amount of space inside a 2D shape. Volume is the space inside a 3D object.'}
                ]
            })

        if 'English' in subjects:
            s = subjects['English']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Literature Analysis', 'topic_icon': '📚',
                'topic_subtitle': 'Analyzing novels, poems and plays',
                'difficulty': 'hard', 'order': 1, 'lessons': [
                    {'title': 'Elements of a Story', 'emoji': '📖', 'order': 1,
                     'content': 'Every story has key elements that work together.\n\nPlot 📊 - the sequence of events\n- Exposition (introduction)\n- Rising action (conflict builds)\n- Climax (turning point)\n- Falling action (events after climax)\n- Resolution (ending)\n\nCharacters 👥\n- Protagonist (main character)\n- Antagonist (opposes the protagonist)\n- Supporting characters\n- Static vs dynamic characters\n\nSetting 📍\n- Time (when the story happens)\n- Place (where the story happens)\n- Atmosphere (mood or feeling)\n\nTheme 💭\n- Central message or lesson\n- Examples: love, courage, friendship, justice\n\nPoint of View 👁️\n- First person (I, we)\n- Third person (he, she, they)\n- Omniscient (all-knowing narrator)',
                     'key_points': json.dumps(['Plot is the sequence of events', 'Characters drive the story', 'Setting is when and where', 'Theme is the central message', 'Point of view affects how we experience the story']),
                     'examples': json.dumps(['Q: What is the climax? A: The turning point of the story', 'Q: What is theme? A: The central message or lesson', 'Q: What is first person narration? A: Story told using "I" or "we"']),
                     'did_you_know': 'The shortest story ever written is: "For sale: baby shoes, never worn." - attributed to Hemingway!', 'definition': 'Literature is written work valued for its artistic merit.'},
                    {'title': 'Poetry Analysis', 'emoji': '🎭', 'order': 2,
                     'content': 'Poetry uses language in special ways to express ideas and feelings.\n\nPoetic devices:\n\nRhyme 🎵 - words that sound alike at the end\n- "The cat in the hat sat on a mat"\n\nRhythm 🥁 - the beat or pattern of sounds\n- Like a song, poetry has a rhythm\n\nAlliteration 🔄 - repeating the same starting sound\n- "Peter Piper picked a peck of pickled peppers"\n\nSimile 🔍 - comparing using "like" or "as"\n- "Her smile was as bright as the sun"\n\nMetaphor 🔍 - direct comparison\n- "Life is a journey"\n\nPersonification 🎭 - giving human qualities to objects\n- "The wind whispered through the trees"\n\nImagery 🖼️ - words that create mental pictures\n- "Golden sunsets over the vast savannah"\n\nOnomatopoeia 🔊 - words that sound like their meaning\n- Buzz, hiss, boom, splash, meow',
                     'key_points': json.dumps(['Poetry uses special language devices', 'Rhyme and rhythm give poetry musical quality', 'Similes and metaphors make comparisons', 'Imagery creates mental pictures']),
                     'examples': json.dumps(['Q: What is a simile? A: Comparison using like or as', 'Q: "The sun smiled down" is an example of? A: Personification', 'Q: What is alliteration? A: Repetition of starting sounds']),
                     'did_you_know': 'The longest poem ever written is the "Mahabharata" with about 200,000 lines!', 'definition': 'Poetry is a form of literature that uses aesthetic and rhythmic qualities of language.'}
                ]
            })

        if 'Science & Technology' in subjects:
            s = subjects['Science & Technology']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Chemistry Basics', 'topic_icon': '🧪',
                'topic_subtitle': 'Introduction to matter and chemical reactions',
                'difficulty': 'hard', 'order': 1, 'lessons': [
                    {'title': 'States of Matter', 'emoji': '💧', 'order': 1,
                     'content': 'Matter is anything that has mass and takes up space. Everything around you is matter!\n\nThree states of matter:\n\nSolid 🧊\n- Has a fixed shape and volume\n- Particles are tightly packed\n- Examples: ice, rock, wood, metal\n\nLiquid 💧\n- Has a fixed volume but takes the shape of its container\n- Particles are loosely packed\n- Examples: water, milk, oil, juice\n\nGas 💨\n- Has no fixed shape or volume\n- Particles are far apart and move freely\n- Examples: oxygen, carbon dioxide, steam\n\nChanges of state:\n- Melting: solid → liquid (ice melts)\n- Freezing: liquid → solid (water freezes)\n- Evaporation: liquid → gas (water dries up)\n- Condensation: gas → liquid (dew on grass)\n- Sublimation: solid → gas (dry ice)',
                     'key_points': json.dumps(['Matter has mass and takes up space', 'Three states: solid, liquid, gas', 'Temperature affects state changes', 'The particles in matter are always moving']),
                     'examples': json.dumps(['Q: What are the three states of matter? A: Solid, liquid, gas', 'Q: What happens when ice melts? A: It changes from solid to liquid', 'Q: What is condensation? A: Gas changing to liquid']),
                     'did_you_know': 'There is a fourth state of matter called plasma - found in stars and lightning!', 'definition': 'Matter is anything that has mass and occupies space.'},
                    {'title': 'Elements and Compounds', 'emoji': '⚗️', 'order': 2,
                     'content': 'Everything in the universe is made from elements.\n\nElement 🔤\n- A pure substance made of only one kind of atom\n- Cannot be broken down into simpler substances\n- 118 known elements (92 natural)\n- Each has a symbol (H for hydrogen, O for oxygen)\n- Examples: Gold (Au), Iron (Fe), Carbon (C)\n\nCompound 🔗\n- Two or more elements chemically combined\n- Has different properties from its elements\n- Examples: H₂O (water), NaCl (salt), CO₂ (carbon dioxide)\n\nMixture 🥗\n- Two or more substances mixed but not chemically combined\n- Can be separated by physical methods\n- Examples: air, soil, sea water\n\nThe Periodic Table organizes all elements by their properties.',
                     'key_points': json.dumps(['Elements are pure substances with one type of atom', 'Compounds are elements joined chemically', 'Mixtures can be separated easily', 'There are 118 known elements']),
                     'examples': json.dumps(['Q: What is H₂O? A: Water (hydrogen and oxygen compound)', 'Q: What is NaCl? A: Salt (sodium chloride)', 'Q: Is air an element, compound, or mixture? A: Mixture']),
                     'did_you_know': 'Hydrogen is the most abundant element in the universe!', 'definition': 'An element is a pure substance that cannot be broken down chemically.'}
                ]
            })

        if 'Home Science' in subjects:
            s = subjects['Home Science']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Food and Nutrition', 'topic_icon': '🍳',
                'topic_subtitle': 'Cooking skills and nutrition knowledge',
                'difficulty': 'medium', 'order': 1, 'lessons': [
                    {'title': 'Cooking Methods', 'emoji': '🍳', 'order': 1,
                     'content': 'Different cooking methods change the taste, texture, and nutrition of food.\n\nBoiling 🫕\n- Cooking food in hot water (100°C)\n- Good for: ugali, rice, eggs, vegetables\n- Preserves nutrients if using little water\n\nFrying 🍳\n- Cooking in oil or fat\n- Deep frying: food is fully submerged in oil (chips, mandazi)\n- Shallow frying: food is cooked in a little oil (eggs, fish)\n\nRoasting 🔥\n- Cooking with dry heat in an oven or over fire\n- Good for: meat, maize, potatoes\n- Gives a nice brown color and flavor\n\nSteaming ♨️\n- Cooking with steam from boiling water\n- Good for: vegetables, fish, mandazi\n- Preserves nutrients well\n\nBaking 🥖\n- Cooking in an oven using dry heat\n- Good for: bread, cakes, cookies\n\nStewing 🥘\n- Cooking slowly in liquid\n- Good for: meat, vegetables, beans',
                     'key_points': json.dumps(['Different methods give different results', 'Steaming preserves the most nutrients', 'Frying adds more fat to food', 'Choose the right method for each food']),
                     'examples': json.dumps(['Q: What cooking method preserves most nutrients? A: Steaming', 'Q: What temperature does water boil at? A: 100°C', 'Q: What is the difference between boiling and steaming? A: Boiling uses water, steaming uses steam']),
                     'did_you_know': 'The oldest known cooking method is roasting over a fire, used for over a million years!', 'definition': 'Cooking methods are different ways to prepare food using heat.'},
                    {'title': 'Kitchen Hygiene and Safety', 'emoji': '🧹', 'order': 2,
                     'content': 'A clean and safe kitchen prevents accidents and food poisoning.\n\nKitchen hygiene 🧼\n- Wash hands before handling food\n- Clean all surfaces before and after cooking\n- Wash fruits and vegetables thoroughly\n- Keep raw meat separate from other foods\n- Use separate chopping boards for meat and vegetables\n- Store food at correct temperatures\n- Check expiry dates\n\nKitchen safety ⚠️\n- Never leave cooking food unattended\n- Turn pot handles inward to avoid knocking\n- Use oven mitts for hot items\n- Keep knives and sharp objects out of reach of children\n- Clean up spills immediately\n- Keep fire extinguisher in kitchen\n- Know basic first aid for burns and cuts\n\nFirst aid for burns: cool under running water for 10 minutes\nFirst aid for cuts: clean wound, apply pressure, cover with bandage',
                     'key_points': json.dumps(['Wash hands and surfaces before cooking', 'Keep raw and cooked foods separate', 'Store food at correct temperatures', 'Be careful with hot items and knives', 'Know basic first aid']),
                     'examples': json.dumps(['Q: How long should you cool a burn? A: 10 minutes under cool water', 'Q: Should you use the same cutting board for meat and vegetables? A: No', 'Q: Why should pot handles face inward? A: To avoid knocking them']),
                     'did_you_know': 'The refrigerator was invented in 1834 and changed how we store food forever!', 'definition': 'Food hygiene is the practice of handling food safely to prevent illness.'}
                ]
            })

    # ============================================================
    # GRADE 9 - Junior Secondary ~age 14
    # ============================================================

    if 'G9' in grades:
        g = grades['G9']

        if 'Mathematics' in subjects:
            s = subjects['Mathematics']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Statistics and Probability', 'topic_icon': '📊',
                'topic_subtitle': 'Data analysis and chance',
                'difficulty': 'hard', 'order': 1, 'lessons': [
                    {'title': 'Data Collection and Presentation', 'emoji': '📊', 'order': 1,
                     'content': 'Statistics is about collecting, organizing, and interpreting data.\n\nTypes of data:\n- Primary data: collected directly by you (surveys, experiments)\n- Secondary data: collected by others (books, internet)\n\nMethods of collecting data:\n- Surveys and questionnaires 📋\n- Interviews 🗣️\n- Observations 👀\n- Experiments 🔬\n\nPresenting data:\n\nBar graph 📊\n- Uses bars to compare categories\n- Bars can be vertical or horizontal\n\nPie chart 🥧\n- Shows parts of a whole\n- Each slice represents a percentage\n\nLine graph 📈\n- Shows trends over time\n- Points connected by lines\n\nFrequency table 📋\n- Shows how often each value occurs\n\nTally marks use groups of 5 (|||| = 4, |||| = 5)',
                     'key_points': json.dumps(['Statistics deals with data', 'Data can be primary or secondary', 'Different graphs show data differently', 'Choose the right graph for your data']),
                     'examples': json.dumps(['Q: What graph is best for showing trends over time? A: Line graph', 'Q: What graph shows parts of a whole? A: Pie chart', 'Q: What is primary data? A: Data you collect yourself']),
                     'did_you_know': 'The word "statistics" comes from the Latin word "status" meaning "state"!', 'definition': 'Statistics is the collection, analysis, and interpretation of data.'},
                    {'title': 'Probability', 'emoji': '🎲', 'order': 2,
                     'content': 'Probability tells us how likely something is to happen.\n\nProbability scale (0 to 1):\n0 = impossible (will not happen)\n1 = certain (will definitely happen)\n0.5 = equally likely (50% chance)\n\nFormula: Probability = (Favorable outcomes) / (Total possible outcomes)\n\nExamples:\n- Tossing a coin: P(heads) = 1/2 = 0.5\n- Rolling a die and getting a 4: P(4) = 1/6 ≈ 0.167\n- Picking a red card from a deck: P(red) = 26/52 = 0.5\n\nTypes of events:\n- Independent: one event does not affect another (coin tosses)\n- Dependent: one event affects another (picking cards without replacing)\n- Mutually exclusive: cannot happen together (heads/tails)\n\nExperimental probability: based on actual experiments\nTheoretical probability: based on mathematical reasoning',
                     'key_points': json.dumps(['Probability ranges from 0 to 1', '0 = impossible, 1 = certain', 'Probability = favorable/total', 'More trials give more reliable results']),
                     'examples': json.dumps(['Q: What is the probability of rolling a 6 on a die? A: 1/6', 'Q: What is the probability of the sun rising tomorrow? A: 1 (certain)', 'Q: If you flip a coin, what is P(tails)? A: 1/2']),
                     'did_you_know': 'The mathematics of probability was developed by Blaise Pascal in the 1600s to solve gambling problems!', 'definition': 'Probability is the measure of how likely an event is to occur.'}
                ]
            })

        if 'English' in subjects:
            s = subjects['English']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Advanced Communication', 'topic_icon': '🎯',
                'topic_subtitle': 'Public speaking and advanced writing',
                'difficulty': 'hard', 'order': 1, 'lessons': [
                    {'title': 'Public Speaking and Debates', 'emoji': '🎤', 'order': 1,
                     'content': 'Public speaking is communicating with an audience. It is an important skill!\n\nTips for public speaking:\n\nPreparation 📝\n- Know your topic well\n- Research both sides of an argument\n- Write key points on cards\n- Practice in front of a mirror\n\nDelivery 🎤\n- Speak clearly and slowly\n- Make eye contact with the audience\n- Use hand gestures naturally\n- Stand up straight and confident\n- Vary your voice (not monotone)\n\nStructure of a speech:\n1. Introduction - greet the audience, state your topic\n2. Body - present your main points with evidence\n3. Conclusion - summarize and end with a strong statement\n\nDebate structure:\n- Motion: the topic being debated\n- Proposition: team arguing FOR the motion\n- Opposition: team arguing AGAINST the motion\n- Each speaker has 3-5 minutes\n- Rebuttals: respond to the other side\'s arguments',
                     'key_points': json.dumps(['Prepare your speech well', 'Speak clearly and make eye contact', 'Structure: intro, body, conclusion', 'In debates, support your arguments with evidence']),
                     'examples': json.dumps(['Q: What is the first step in public speaking? A: Preparation', 'Q: Why is eye contact important? A: It engages the audience', 'Q: What is a rebuttal in debate? A: Responding to the other side\'s arguments']),
                     'did_you_know': 'The fear of public speaking (glossophobia) is more common than the fear of death!', 'definition': 'Public speaking is the act of giving a speech to a live audience.'},
                    {'title': 'Report and Article Writing', 'emoji': '📰', 'order': 2,
                     'content': 'Reports and articles are formal types of writing used to inform or persuade.\n\nReport Writing 📋\nA report presents information in a clear, organized way.\n\nStructure:\n1. Title - clear and descriptive\n2. Introduction - what the report is about\n3. Findings/body - organized information\n4. Conclusion - summary of findings\n5. Recommendations - suggestions for action\n\nLanguage features:\n- Formal language\n- Third person (the researcher found...)\n- Facts and evidence\n- Headings and subheadings\n\nArticle Writing 📰\nFor a school magazine or newspaper.\n\nStructure:\n1. Catchy headline\n2. Byline (writer\'s name)\n3. Introduction - hook the reader\n4. Body - detailed information\n5. Conclusion - final thought\n\nLanguage features:\n- Engaging and interesting\n- Can use first person\n- Mix of facts and opinions\n- Suitable for the target audience',
                     'key_points': json.dumps(['Reports present factual information', 'Articles are for magazines and newspapers', 'Use headings to organize content', 'Consider your audience when writing']),
                     'examples': json.dumps(['Q: What is included in a report? A: Title, intro, findings, conclusion, recommendations', 'Q: What is a byline? A: The writer\'s name in an article', 'Q: How does language differ between report and article? A: Reports are more formal']),
                     'did_you_know': 'The first newspaper was published in 1605 in Germany!', 'definition': 'A report presents structured information. An article informs or persuades readers.'}
                ]
            })

        if 'Science & Technology' in subjects:
            s = subjects['Science & Technology']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Ecology and Environment', 'topic_icon': '🌍',
                'topic_subtitle': 'Understanding ecosystems and environmental issues',
                'difficulty': 'hard', 'order': 1, 'lessons': [
                    {'title': 'Ecosystems and Food Chains', 'emoji': '🌿', 'order': 1,
                     'content': 'An ecosystem is a community of living things interacting with their environment.\n\nComponents of an ecosystem:\n\nBiotic (living) 🐾\n- Producers (plants - make their own food)\n- Consumers (animals - eat other organisms)\n- Decomposers (bacteria, fungi - break down dead matter)\n\nAbiotic (non-living) 🌍\n- Sunlight ☀️\n- Water 💧\n- Soil 🌱\n- Air 🌬️\n- Temperature 🌡️\n\nFood chain: shows who eats whom\nSun → Grass → Zebra → Lion\n\nEnergy flows from producers to consumers.\n\nFood web: interconnected food chains\n\nTrophic levels:\n1st: Producers (plants)\n2nd: Primary consumers (herbivores)\n3rd: Secondary consumers (carnivores)\n4th: Tertiary consumers (top predators)\n\nOnly about 10% of energy passes from one level to the next!',
                     'key_points': json.dumps(['An ecosystem includes living and non-living things', 'Producers make their own food', 'Consumers eat other organisms', 'Decomposers break down dead matter', 'Energy decreases up the food chain']),
                     'examples': json.dumps(['Q: What are producers? A: Plants that make their own food', 'Q: Give a simple food chain. A: Sun → Grass → Cow → Human', 'Q: What do decomposers do? A: Break down dead organisms']),
                     'did_you_know': 'The Amazon rainforest produces 20% of the world\'s oxygen!', 'definition': 'An ecosystem is a community of living organisms interacting with their environment.'},
                    {'title': 'Environmental Conservation', 'emoji': '♻️', 'order': 2,
                     'content': 'Our environment faces many challenges. We all need to help protect it.\n\nEnvironmental problems:\n\n🌪️ Climate change - global temperatures rising\n🌊 Pollution - air, water, soil pollution\n🌳 Deforestation - cutting down forests\n🏭 Waste - plastic and other waste accumulation\n🦁 Loss of biodiversity - species becoming extinct\n\nWhat we can do:\n\n1. Reduce, Reuse, Recycle ♻️\n   - Reduce what you use\n   - Reuse items instead of throwing away\n   - Recycle paper, plastic, metal, glass\n\n2. Plant trees 🌳\n   - Trees absorb CO₂ and produce oxygen\n   - Prevent soil erosion\n\n3. Save water 💧\n   - Turn off taps when not in use\n   - Collect rainwater\n\n4. Use less energy 💡\n   - Turn off lights when leaving a room\n   - Use solar energy\n\n5. Protect wildlife 🦁\n   - Do not litter in national parks\n   - Report poachers\n\nEvery small action makes a difference!',
                     'key_points': json.dumps(['Climate change and pollution threaten our planet', 'The 3 Rs: Reduce, Reuse, Recycle', 'Plant trees to absorb CO₂', 'Save water and energy', 'Protect wildlife and natural habitats']),
                     'examples': json.dumps(['Q: Name one environmental problem. A: Climate change, pollution, deforestation', 'Q: What are the 3 Rs? A: Reduce, Reuse, Recycle', 'Q: How can you save water? A: Turn off taps, collect rainwater']),
                     'did_you_know': 'Kenya banned plastic bags in 2017 - one of the strictest bans in the world!', 'definition': 'Conservation is the protection of the environment and natural resources.'}
                ]
            })

        if 'Life Skills' in subjects:
            s = subjects['Life Skills']
            content.append({
                'subject': s, 'grade': g,
                'topic_title': 'Career and Financial Skills', 'topic_icon': '💼',
                'topic_subtitle': 'Preparing for the future',
                'difficulty': 'hard', 'order': 1, 'lessons': [
                    {'title': 'Career Exploration', 'emoji': '💼', 'order': 1,
                     'content': 'Thinking about your future career is exciting! There are many options.\n\nSteps to choose a career:\n\n1. Know yourself 🧠\n   - What subjects do you enjoy?\n   - What are your strengths?\n   - What activities make you happy?\n\n2. Explore options 🔍\n   - Talk to people in different careers\n   - Research different professions\n   - Attend career days at school\n\n3. Consider your education 🎓\n   - What subjects do you need?\n   - What level of education is required?\n   - Which schools offer the right courses?\n\nCareer clusters in Kenya:\n- Health sciences (doctor, nurse, pharmacist)\n- Engineering (civil, electrical, mechanical)\n- Education (teacher, lecturer)\n- Business (accountant, entrepreneur, manager)\n- Technology (programmer, IT specialist)\n- Creative arts (artist, musician, actor)\n- Agriculture (farmer, vet, agronomist)\n- Law and justice (lawyer, judge, police)\n\nThere is no single "right" career - find what fits YOU!',
                     'key_points': json.dumps(['Know your interests and strengths', 'Explore different career options', 'Consider education requirements', 'There are many career clusters in Kenya', 'Choose a career that fits you']),
                     'examples': json.dumps(['Q: What subjects do you enjoy?', 'Q: Name a career in health sciences. A: Doctor, nurse', 'Q: Why is it important to explore careers? A: To find what suits you']),
                     'did_you_know': 'Most people change careers 5-7 times in their lifetime!', 'definition': 'A career is a profession or occupation that you train for and pursue.'},
                    {'title': 'Financial Literacy', 'emoji': '💰', 'order': 2,
                     'content': 'Managing money is an important life skill. Learn how to handle money wisely!\n\nEarning money 💵\n- Jobs and careers\n- Pocket money\n- Small business (lemonade stand, helping neighbors)\n\nSaving money 🏦\n- Pay yourself first (save before spending)\n- Set savings goals\n- Use a piggy bank or bank account\n- Save at least 10% of any money you get\n\nSpending wisely 🛒\n- Needs vs wants (need: food; want: candy)\n- Compare prices before buying\n- Avoid impulse buying\n- Make a budget\n\nBudgeting 📋\nA plan for your money:\n50% - Needs (food, transport, school supplies)\n30% - Wants (entertainment, treats)\n20% - Savings\n\nBanking basics 🏦\n- Savings account: earn interest on money\n- Mobile money: M-Pesa is popular in Kenya\n- Interest: money the bank pays you for keeping your money there',
                     'key_points': json.dumps(['Save at least 10% of money you get', 'Distinguish between needs and wants', 'Make a budget to plan spending', 'Use bank accounts and mobile money wisely']),
                     'examples': json.dumps(['Q: What is the difference between a need and a want? A: Need is essential, want is a luxury', 'Q: What percentage should you save? A: At least 10-20%', 'Q: What is M-Pesa? A: A mobile money service in Kenya']),
                     'did_you_know': 'The word "salary" comes from the Latin word "sal" meaning "salt" - Roman soldiers were paid in salt!', 'definition': 'Financial literacy is the ability to understand and manage money effectively.'}
                ]
            })

    # Write all content to database
    print('Seeding CBC missing grade content...')
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
    print(f'  Created {created_count} lessons across {len(content)} topics for grades PP1, PP2, G5, G6, G7, G8, G9')
    return created_count
