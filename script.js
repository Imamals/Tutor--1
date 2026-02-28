// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Simulated Code Execution
function simulateRun(output, btn) {
    const parent = btn.parentElement;
    const outputDiv = parent.querySelector('.output');

    btn.textContent = 'Running...';
    btn.disabled = true;

    setTimeout(() => {
        outputDiv.style.display = 'block';
        outputDiv.textContent = '> ' + output;
        btn.textContent = 'Run Code';
        btn.disabled = false;
    }, 600);
}

// Special Input Simulation
function runInputSnippet(btn) {
    const parent = btn.parentElement;
    const inputContainer = parent.querySelector('.input-field-container');
    const inputField = parent.querySelector('.terminal-input');
    const outputDiv = parent.querySelector('.output');

    outputDiv.style.display = 'none';
    inputContainer.style.display = 'block';
    inputField.focus();

    inputField.onkeydown = function (e) {
        if (e.key === 'Enter') {
            const val = inputField.value;
            inputContainer.style.display = 'none';
            outputDiv.style.display = 'block';
            outputDiv.textContent = `> What is your name? ${val}\n> Hello, ${val}!`;
            inputField.value = '';
        }
    };
}

// Quiz Logic
function checkAnswer(isCorrect, btn) {
    const options = btn.parentElement.querySelectorAll('.option');
    const feedback = document.getElementById('quiz-feedback');

    // Reset classes
    options.forEach(opt => {
        opt.classList.remove('correct', 'incorrect');
        opt.disabled = true;
    });

    if (isCorrect) {
        btn.classList.add('correct');
        feedback.innerHTML = '<p style="color: #10b981; margin-top: 1rem; font-weight: 600;">Correct! You have a good grasp of Python syntax.</p>';
    } else {
        btn.classList.add('incorrect');
        feedback.innerHTML = '<p style="color: #ef4444; margin-top: 1rem; font-weight: 600;">Not quite. Hint: "def" stands for define.</p>';

        // Show the correct answer
        options.forEach(opt => {
            if (opt.textContent.includes('def')) {
                opt.classList.add('correct');
            }
        });
    }
}

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const nav = document.getElementById('navbar');
    if (window.scrollY > 50) {
        nav.style.padding = '0.7rem 0';
        nav.style.background = 'rgba(15, 23, 42, 0.95)';
    } else {
        nav.style.padding = '1rem 0';
        nav.style.background = 'rgba(15, 23, 42, 0.8)';
    }
});
