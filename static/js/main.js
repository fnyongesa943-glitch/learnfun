/**
 * Kids Learning App - Main JavaScript
 * Handles quiz interactions, animations, sound effects, and UI updates.
 */

// ---- Sound Effects using Web Audio API ----
const SoundFX = {
    audioContext: null,

    init() {
        // Initialize audio context on first user interaction
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    },

    playCorrect() {
        this.init();
        const ctx = this.audioContext;
        const oscillator = ctx.createOscillator();
        const gainNode = ctx.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(ctx.destination);

        // Happy ascending tones
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
        oscillator.frequency.setValueAtTime(659.25, ctx.currentTime + 0.1); // E5
        oscillator.frequency.setValueAtTime(783.99, ctx.currentTime + 0.2); // G5

        gainNode.gain.setValueAtTime(0.3, ctx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.4);

        oscillator.start(ctx.currentTime);
        oscillator.stop(ctx.currentTime + 0.4);
    },

    playIncorrect() {
        this.init();
        const ctx = this.audioContext;
        const oscillator = ctx.createOscillator();
        const gainNode = ctx.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(ctx.destination);

        // Gentle descending tone (not discouraging)
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(440, ctx.currentTime); // A4
        oscillator.frequency.setValueAtTime(349.23, ctx.currentTime + 0.15); // F4

        gainNode.gain.setValueAtTime(0.2, ctx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);

        oscillator.start(ctx.currentTime);
        oscillator.stop(ctx.currentTime + 0.3);
    },

    playClick() {
        this.init();
        const ctx = this.audioContext;
        const oscillator = ctx.createOscillator();
        const gainNode = ctx.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(ctx.destination);

        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(800, ctx.currentTime);

        gainNode.gain.setValueAtTime(0.1, ctx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.05);

        oscillator.start(ctx.currentTime);
        oscillator.stop(ctx.currentTime + 0.05);
    },

    playCelebration() {
        this.init();
        const ctx = this.audioContext;

        // Play a fanfare sequence
        const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
        const startTime = ctx.currentTime;

        notes.forEach((freq, i) => {
            const oscillator = ctx.createOscillator();
            const gainNode = ctx.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(ctx.destination);

            oscillator.type = 'sine';
            oscillator.frequency.setValueAtTime(freq, startTime + i * 0.15);

            gainNode.gain.setValueAtTime(0.3, startTime + i * 0.15);
            gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + i * 0.15 + 0.3);

            oscillator.start(startTime + i * 0.15);
            oscillator.stop(startTime + i * 0.15 + 0.3);
        });
    }
};

// ---- Confetti Effect ----
function createConfetti() {
    const container = document.createElement('div');
    container.className = 'confetti-container';
    document.body.appendChild(container);

    const colors = ['#6366F1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#3B82F6'];

    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDelay = Math.random() * 2 + 's';
        confetti.style.animationDuration = (2 + Math.random() * 2) + 's';
        confetti.style.width = (5 + Math.random() * 10) + 'px';
        confetti.style.height = (5 + Math.random() * 10) + 'px';
        confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
        container.appendChild(confetti);
    }

    // Remove container after animation
    setTimeout(() => container.remove(), 5000);
}

// ---- Avatar Selection ----
function initAvatarSelection() {
    const avatars = document.querySelectorAll('.avatar-option');
    const hiddenInput = document.getElementById('avatar-input');

    avatars.forEach(avatar => {
        avatar.addEventListener('click', () => {
            avatars.forEach(a => a.classList.remove('selected'));
            avatar.classList.add('selected');
            if (hiddenInput) {
                hiddenInput.value = avatar.dataset.avatar;
            }
            SoundFX.playClick();
        });
    });
}

// ---- Quiz Functionality ----
function initQuiz() {
    const questionCards = document.querySelectorAll('.question-card');
    let currentQuestion = 0;
    const totalQuestions = questionCards.length;

    if (totalQuestions === 0) return;

    // Show only first question initially
    questionCards.forEach((card, index) => {
        if (index > 0) {
            card.style.display = 'none';
        }
    });

    // Update progress
    updateProgress(1, totalQuestions);

    // Handle option selection
    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const questionCard = this.closest('.question-card');
            const options = questionCard.querySelectorAll('.option-btn');
            const userAnswer = this.dataset.answer;
            const correctAnswer = questionCard.dataset.correct;
            const questionId = questionCard.dataset.questionId;

            SoundFX.playClick();

            // Disable all options after selection
            options.forEach(opt => {
                opt.style.pointerEvents = 'none';
                opt.classList.remove('selected');
            });

            // Show correct/wrong
            if (userAnswer === correctAnswer) {
                this.classList.add('correct-answer');
                questionCard.classList.add('correct');
                SoundFX.playCorrect();
            } else {
                this.classList.add('wrong-answer');
                questionCard.classList.add('incorrect');
                // Highlight correct answer
                options.forEach(opt => {
                    if (opt.dataset.answer === correctAnswer) {
                        opt.classList.add('correct-answer');
                    }
                });
                SoundFX.playIncorrect();
            }

            // Show explanation
            const explanation = questionCard.querySelector('.explanation');
            if (explanation) {
                explanation.style.display = 'block';
                explanation.style.animation = 'slideIn 0.3s ease';
            }

            // Show next button
            const nextBtn = questionCard.querySelector('.next-btn');
            if (nextBtn) {
                nextBtn.style.display = 'inline-flex';
                nextBtn.style.animation = 'pulse 1s infinite';
            }
        });
    });

    // Handle next button
    document.querySelectorAll('.next-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const currentCard = btn.closest('.question-card');
            currentCard.style.display = 'none';
            currentQuestion++;

            if (currentQuestion < totalQuestions) {
                const nextCard = questionCards[currentQuestion];
                nextCard.style.display = 'block';
                nextCard.style.animation = 'slideIn 0.3s ease';
                updateProgress(currentQuestion + 1, totalQuestions);
                SoundFX.playClick();
            }
        });
    });

    function updateProgress(current, total) {
        const progressFill = document.querySelector('.progress-bar-fill');
        const progressText = document.querySelector('.progress-text');
        if (progressFill) {
            progressFill.style.width = ((current / total) * 100) + '%';
        }
        if (progressText) {
            progressText.textContent = `${current}/${total}`;
        }
    }
}

// ---- Quiz Result Page ----
function initQuizResult() {
    const scoreElement = document.querySelector('.result-score');
    if (!scoreElement) return;

    const score = parseInt(scoreElement.textContent);

    // Add appropriate class
    if (score >= 80) {
        scoreElement.classList.add('excellent');
        createConfetti();
        SoundFX.playCelebration();
    } else if (score >= 50) {
        scoreElement.classList.add('good');
    } else {
        scoreElement.classList.add('try-again');
    }

    // Animate stars
    const stars = document.querySelectorAll('.result-stars span');
    stars.forEach((star, index) => {
        star.style.opacity = '0';
        setTimeout(() => {
            star.style.display = 'inline-block';
            star.style.animation = 'starPop 0.5s ease forwards';
        }, 300 + (index * 200));
    });
}

// ---- Flash Message Auto-Dismiss ----
function initFlashMessages() {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.animation = 'fadeOut 0.3s ease forwards';
            setTimeout(() => flash.remove(), 300);
        }, 4000);
    });
}

// ---- Animate Numbers on Scroll ----
function animateValue(element, start, end, duration) {
    const range = end - start;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const value = Math.floor(start + range * progress);
        element.textContent = value;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

// ---- Dark Mode Toggle ----
function initDarkMode() {
    const toggle = document.getElementById('darkModeToggle');
    if (!toggle) return;

    // Check saved preference
    const saved = localStorage.getItem('darkMode');
    if (saved === 'true') {
        document.body.classList.add('dark-mode');
        toggle.textContent = '☀️';
    }

    toggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        toggle.textContent = isDark ? '☀️' : '🌙';
        localStorage.setItem('darkMode', isDark);
        SoundFX.playClick();
    });
}

// ---- Initialize on DOM Ready ----
document.addEventListener('DOMContentLoaded', () => {
    initDarkMode();
    initAvatarSelection();
    initQuiz();
    initQuizResult();
    initFlashMessages();

    // Add hover sound to buttons
    document.querySelectorAll('.btn, .nav-link, .subject-card, .quiz-item').forEach(el => {
        el.addEventListener('mouseenter', () => SoundFX.playClick());
    });
});
