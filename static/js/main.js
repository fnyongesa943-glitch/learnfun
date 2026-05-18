/**
 * Kids Learning App - Main JavaScript
 * Handles quiz interactions, animations, sound effects, and UI updates.
 */

// ---- Sound Effects using Web Audio API ----
const SoundFX = {
    audioContext: null,
    enabled: true,

    init() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    },

    toggle() {
        this.enabled = !this.enabled;
        localStorage.setItem('soundEnabled', this.enabled);
        return this.enabled;
    },

    playCorrect() {
        if (!this.enabled) return;
        this.init();
        const ctx = this.audioContext;
        const oscillator = ctx.createOscillator();
        const gainNode = ctx.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(ctx.destination);

        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(523.25, ctx.currentTime);
        oscillator.frequency.setValueAtTime(659.25, ctx.currentTime + 0.1);
        oscillator.frequency.setValueAtTime(783.99, ctx.currentTime + 0.2);

        gainNode.gain.setValueAtTime(0.3, ctx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.4);

        oscillator.start(ctx.currentTime);
        oscillator.stop(ctx.currentTime + 0.4);
    },

    playIncorrect() {
        if (!this.enabled) return;
        this.init();
        const ctx = this.audioContext;
        const oscillator = ctx.createOscillator();
        const gainNode = ctx.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(ctx.destination);

        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(440, ctx.currentTime);
        oscillator.frequency.setValueAtTime(349.23, ctx.currentTime + 0.15);

        gainNode.gain.setValueAtTime(0.2, ctx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);

        oscillator.start(ctx.currentTime);
        oscillator.stop(ctx.currentTime + 0.3);
    },

    playClick() {
        if (!this.enabled) return;
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
        if (!this.enabled) return;
        this.init();
        const ctx = this.audioContext;

        const notes = [523.25, 659.25, 783.99, 1046.50];
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
function createConfetti(count) {
    const container = document.createElement('div');
    container.className = 'confetti-container';
    document.body.appendChild(container);

    const colors = ['#2196F3', '#4CAF50', '#FF9800', '#EF4444', '#FF4081', '#FFD93D', '#26C6DA'];
    const total = count || 60;

    for (let i = 0; i < total; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDelay = Math.random() * 1.5 + 's';
        confetti.style.animationDuration = (2 + Math.random() * 2) + 's';
        confetti.style.width = (6 + Math.random() * 10) + 'px';
        confetti.style.height = (6 + Math.random() * 10) + 'px';
        confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
        container.appendChild(confetti);
    }

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

// ---- Quiz Functionality (legacy - for fallback) ----
function initQuiz() {
    const questionCards = document.querySelectorAll('.question-card');
    let currentQuestion = 0;
    const totalQuestions = questionCards.length;

    if (totalQuestions === 0) return;

    questionCards.forEach((card, index) => {
        if (index > 0) {
            card.style.display = 'none';
        }
    });

    updateProgress(1, totalQuestions);

    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const questionCard = this.closest('.question-card');
            const options = questionCard.querySelectorAll('.option-btn');
            const userAnswer = this.dataset.answer;
            const correctAnswer = questionCard.dataset.correct;
            const questionId = questionCard.dataset.questionId;

            SoundFX.playClick();

            options.forEach(opt => {
                opt.style.pointerEvents = 'none';
                opt.classList.remove('selected');
            });

            if (userAnswer === correctAnswer) {
                this.classList.add('correct-answer');
                questionCard.classList.add('correct');
                SoundFX.playCorrect();
            } else {
                this.classList.add('wrong-answer');
                questionCard.classList.add('incorrect');
                options.forEach(opt => {
                    if (opt.dataset.answer === correctAnswer) {
                        opt.classList.add('correct-answer');
                    }
                });
                SoundFX.playIncorrect();
            }

            const explanation = questionCard.querySelector('.explanation');
            if (explanation) {
                explanation.style.display = 'block';
                explanation.style.animation = 'slideIn 0.3s ease';
            }

            const nextBtn = questionCard.querySelector('.next-btn');
            if (nextBtn) {
                nextBtn.style.display = 'inline-flex';
                nextBtn.style.animation = 'pulse 1s infinite';
            }
        });
    });

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

    if (score >= 80) {
        scoreElement.classList.add('excellent');
        createConfetti(80);
        SoundFX.playCelebration();
    } else if (score >= 50) {
        scoreElement.classList.add('good');
        createConfetti(30);
    } else {
        scoreElement.classList.add('try-again');
    }

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

// ---- Sound Toggle ----
function initSoundToggle() {
    const saved = localStorage.getItem('soundEnabled');
    if (saved !== null) {
        SoundFX.enabled = saved === 'true';
    }

    const toggleBtn = document.getElementById('soundToggle');
    if (toggleBtn) {
        updateSoundIcon(toggleBtn);
        toggleBtn.addEventListener('click', () => {
            SoundFX.toggle();
            updateSoundIcon(toggleBtn);
            SoundFX.playClick();
        });
    }
}

function updateSoundIcon(btn) {
    btn.textContent = SoundFX.enabled ? '\uD83D\uDD0A' : '\uD83D\uDD07';
    btn.title = SoundFX.enabled ? 'Mute sound' : 'Enable sound';
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

    const saved = localStorage.getItem('darkMode');
    if (saved === 'true') {
        document.body.classList.add('dark-mode');
        toggle.textContent = '\u2600\uFE0F';
    }

    toggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        toggle.textContent = isDark ? '\u2600\uFE0F' : '\uD83C\uDF19';
        localStorage.setItem('darkMode', isDark);
        SoundFX.playClick();
    });
}

// ---- Initialize on DOM Ready ----
document.addEventListener('DOMContentLoaded', () => {
    initDarkMode();
    initSoundToggle();
    initAvatarSelection();
    initQuiz();
    initQuizResult();
    initFlashMessages();

    document.querySelectorAll('.btn, .nav-link, .subject-card, .quiz-item').forEach(el => {
        el.addEventListener('mouseenter', () => SoundFX.playClick());
    });
});
