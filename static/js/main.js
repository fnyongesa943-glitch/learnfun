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
    },

    playStreak() {
        if (!this.enabled) return;
        this.init();
        const ctx = this.audioContext;
        const oscillator = ctx.createOscillator();
        const gainNode = ctx.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(ctx.destination);

        oscillator.type = 'triangle';
        oscillator.frequency.setValueAtTime(600, ctx.currentTime);
        oscillator.frequency.linearRampToValueAtTime(900, ctx.currentTime + 0.2);

        gainNode.gain.setValueAtTime(0.25, ctx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);

        oscillator.start(ctx.currentTime);
        oscillator.stop(ctx.currentTime + 0.3);
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

// ---- Score Popup ----
function showScorePopup(points) {
    const popup = document.createElement('div');
    popup.className = 'score-popup';
    popup.textContent = `\uD83C\uDF89 +${points} points!`;
    document.body.appendChild(popup);
    setTimeout(() => popup.remove(), 1500);
}

// ---- Streak System ----
const StreakTracker = {
    count: 0,
    max: 0,
    
    recordCorrect() {
        this.count++;
        if (this.count > this.max) this.max = this.count;
        return this.count;
    },
    
    recordWrong() {
        this.count = 0;
    },
    
    getStreak() {
        return this.count;
    },
    
    showStreakBadge() {
        if (this.count >= 3) {
            const badge = document.createElement('div');
            badge.className = 'streak-badge feedback-bounce';
            badge.textContent = `\uD83D\uDD25 ${this.count} in a row!`;
            document.body.appendChild(badge);
            SoundFX.playStreak();
            setTimeout(() => badge.remove(), 2000);
        }
    }
};

// ---- Count Up Animation ----
function animateCountUp(element, target, duration = 500) {
    const start = parseInt(element.textContent) || 0;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(start + (target - start) * eased);
        element.textContent = current;

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.classList.add('count-up');
            setTimeout(() => element.classList.remove('count-up'), 300);
        }
    }

    requestAnimationFrame(update);
}

// ---- Button Ripple Effect ----
function initRippleEffect() {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            
            this.style.setProperty('--x', x + '%');
            this.style.setProperty('--y', y + '%');
            
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.left = (e.clientX - rect.left) + 'px';
            ripple.style.top = (e.clientY - rect.top) + 'px';
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

// ---- Intersection Observer for Appear Animations ----
function initAppearAnimations() {
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

        document.querySelectorAll('.appear').forEach(el => observer.observe(el));
    } else {
        document.querySelectorAll('.appear').forEach(el => el.classList.add('visible'));
    }
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

// ---- Enhanced Quiz Interactions (Modern) ----
function initModernQuiz() {
    const questionCards = document.querySelectorAll('.question-card-new');
    if (questionCards.length === 0) return;

    let currentQuestion = 0;
    let totalScore = 0;
    let streak = 0;
    const totalQuestions = questionCards.length;
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content || '';

    // Hide all questions except first
    questionCards.forEach((card, index) => {
        if (index > 0) card.style.display = 'none';
    });

    function updateProgress(current) {
        const pct = ((current) / totalQuestions) * 100;
        const progressFill = document.getElementById('quizProgressFill');
        const progressCurrent = document.getElementById('progressCurrent');
        const scoreDisplay = document.getElementById('scoreDisplay');
        
        if (progressFill) {
            progressFill.style.width = pct + '%';
            progressFill.classList.add('progress-bar-animated');
        }
        if (progressCurrent) {
            animateCountUp(progressCurrent, current, 300);
        }
        if (scoreDisplay) {
            scoreDisplay.textContent = '\u2B50 ' + totalScore + ' pts';
            scoreDisplay.classList.add('count-up');
            setTimeout(() => scoreDisplay.classList.remove('count-up'), 300);
        }
    }

    function showFeedback(questionCard, isCorrect, points) {
        const popup = questionCard.querySelector('.feedback-popup');
        if (!popup) return;
        
        const icon = popup.querySelector('.feedback-icon');
        const text = popup.querySelector('.feedback-text');

        if (isCorrect) {
            popup.className = 'feedback-popup feedback-correct';
            icon.textContent = '\uD83D\uDD25';
            text.textContent = 'Awesome! Great job!';
            popup.style.display = 'flex';
            popup.style.animation = 'feedbackSlideIn 0.4s ease, feedbackBounce 0.6s ease';
            
            if (points > 0) {
                setTimeout(() => showScorePopup(points), 400);
            }
        } else {
            popup.className = 'feedback-popup feedback-incorrect';
            icon.textContent = '\uD83D\uDCA1';
            text.textContent = 'Try again next time!';
            popup.style.display = 'flex';
            popup.style.animation = 'feedbackSlideIn 0.4s ease, wrongShake 0.4s ease';
        }

        setTimeout(() => { popup.style.display = 'none'; }, 2000);
    }

    function selectAnswer(btn) {
        const card = btn.closest('.question-card-new');
        const options = card.querySelectorAll('.option-btn-new');
        const userAnswer = btn.dataset.answer;
        const correctAnswer = card.dataset.correct;
        const questionId = card.dataset.questionId;
        const points = parseInt(card.dataset.points) || 10;
        const hiddenInput = card.querySelector(`input[name="q${questionId}"]`);

        if (hiddenInput) hiddenInput.value = userAnswer;

        options.forEach(opt => {
            opt.style.pointerEvents = 'none';
            opt.classList.remove('option-selected');
        });

        if (userAnswer === correctAnswer) {
            btn.classList.add('option-correct');
            totalScore += points;
            streak = StreakTracker.recordCorrect();
            SoundFX.playCorrect();
            showFeedback(card, true, points);
            StreakTracker.showStreakBadge();
        } else {
            btn.classList.add('option-wrong');
            options.forEach(opt => {
                if (opt.dataset.answer === correctAnswer) {
                    opt.classList.add('option-correct');
                }
            });
            StreakTracker.recordWrong();
            SoundFX.playIncorrect();
            showFeedback(card, false, 0);
        }

        const explanation = card.querySelector('.explanation-new');
        if (explanation) {
            explanation.style.display = 'block';
            explanation.style.animation = 'slideIn 0.3s ease';
        }

        updateProgress(currentQuestion + 1);

        if (currentQuestion < totalQuestions - 1) {
            const nextBtn = document.getElementById('nextBtn-' + questionId);
            if (nextBtn) {
                nextBtn.style.display = 'inline-flex';
                nextBtn.style.animation = 'pulse 1s infinite';
            }
        } else {
            const finishBtn = document.getElementById('finishBtn');
            if (finishBtn) {
                finishBtn.style.display = 'inline-flex';
                finishBtn.style.animation = 'pulse 1s infinite';
            }
        }
    }

    document.querySelectorAll('.option-btn-new').forEach(btn => {
        btn.addEventListener('click', function() {
            const card = this.closest('.question-card-new');
            if (card.querySelector('.option-correct, .option-wrong')) return;
            selectAnswer(this);
        });
    });

    document.querySelectorAll('.btn-next').forEach(btn => {
        btn.addEventListener('click', () => {
            const currentCard = btn.closest('.question-card-new');
            currentCard.style.display = 'none';
            currentQuestion++;

            if (currentQuestion < totalQuestions) {
                const nextCard = questionCards[currentQuestion];
                nextCard.style.display = 'block';
                nextCard.style.animation = 'slideIn 0.3s ease';
                SoundFX.playClick();
            }
        });
    });

    updateProgress(0);
}

// ---- Initialize on DOM Ready ----
document.addEventListener('DOMContentLoaded', () => {
    initDarkMode();
    initSoundToggle();
    initAvatarSelection();
    initQuiz();
    initModernQuiz();
    initQuizResult();
    initFlashMessages();
    initRippleEffect();
    initAppearAnimations();

    // Subtle hover sound on interactive elements
    document.querySelectorAll('.btn, .nav-link, .subject-card, .quiz-item').forEach(el => {
        el.addEventListener('mouseenter', () => SoundFX.playClick());
    });
});
