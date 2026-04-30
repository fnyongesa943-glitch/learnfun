# 🌈 LearnFun - Kids Learning App

A fun, interactive educational web application for children aged 6-12, built with Python Flask.

## Features

- **🔢 Math** - Addition, subtraction, and multiplication quizzes
- **📚 Reading** - Word puzzles, story comprehension, and vocabulary
- **🔬 Science** - Animals, weather, and space exploration
- **⭐ Points & Badges** - Reward system to keep kids motivated
- **📊 Progress Tracking** - Dashboard showing learning achievements
- **🦉 Ollie the Owl** - Friendly mascot that guides users
- **🎵 Sound Effects** - Audio feedback for correct/incorrect answers
- **🎉 Confetti Celebrations** - Visual rewards for great scores
- **📱 Responsive Design** - Works on desktop, tablet, and mobile

## Project Structure

```
kids_learning_app/
├── app.py                 # Main application entry point
├── config.py              # Configuration settings
├── models.py              # Database models (User, Quiz, Score, etc.)
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── blueprints/
│   ├── __init__.py
│   ├── auth.py            # Login/Signup routes
│   ├── main.py            # Home and subject routes
│   ├── quiz.py            # Quiz and scoring routes
│   └── progress.py        # Progress dashboard routes
├── templates/
│   ├── base.html          # Base template with navbar
│   ├── index.html         # Home page
│   ├── login.html         # Login form
│   ├── signup.html        # Registration with avatar selection
│   ├── subjects.html      # Subject listing
│   ├── subject_detail.html# Quizzes for a subject
│   ├── quiz.html          # Interactive quiz page
│   ├── quiz_result.html   # Quiz results and review
│   └── progress.html      # User progress dashboard
└── static/
    ├── css/
    │   └── style.css      # Child-friendly styles & animations
    ├── js/
    │   └── main.js        # Quiz logic, sounds, confetti
    └── images/            # (Optional custom images)
```

## How to Run Locally

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Navigate to the project folder

```bash
cd kids_learning_app
```

### Step 2: Create a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the application

```bash
python app.py
```

### Step 5: Open in your browser

Navigate to: **http://localhost:5000**

## Using the App

1. **Sign Up** - Create an account with a username, email, password, and choose an avatar
2. **Browse Subjects** - Choose from Math, Reading, or Science
3. **Take Quizzes** - Answer questions with instant feedback and explanations
4. **Earn Points** - Get points for correct answers
5. **Collect Badges** - Unlock badges for achievements
6. **Track Progress** - View your dashboard to see growth over time

## Badge System

| Badge | Requirement |
|-------|-------------|
| 🌟 First Steps | Complete your first quiz |
| 💯 Perfect Score | Get 100% on any quiz |
| 🔢 Math Star | Complete 3 math quizzes |
| 📚 Reading Pro | Complete 3 reading quizzes |
| 🔬 Science Wizard | Complete 3 science quizzes |
| 🎯 Quiz Master | Complete 5 quizzes |
| 🏆 Champion | Complete 10 quizzes |
| 🚀 Rocket Learner | Reach level 5 |

## Technology Stack

- **Backend**: Python 3, Flask, Flask-SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Sounds**: Web Audio API (no external files needed)
- **Fonts**: Google Fonts (Nunito)

## Design Features

- Bright, vibrant colors with soft rounded edges
- Smooth CSS animations and hover effects
- Large, readable fonts optimized for children
- Mobile-responsive layout
- Ollie the Owl mascot for guidance
- Confetti celebration effects
- Sound feedback for interactions

## License

This project is for educational purposes.
