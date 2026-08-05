document.getElementById('checkBtn').addEventListener('click', checkAnswer);

function checkAnswer() {
    const userInp = document.getElementById('userAnswer').value;
    const feedback = document.getElementById('feedback');
    const nextBtn = document.getElementById('nextBtn');
    const checkBtn = document.getElementById('checkBtn');

    // Проверка, ввёл ли пользователь что-нибудь
    if (userInp === "") {
        feedback.innerHTML = "Пожалуйста, введите число!";
        feedback.className = "incorrect";
        return;
    }

    const parsedUserAnswer = parseFloat(userInp);

    // Сверяем с константой CORRECT_ANSWER, которую мы создали в HTML
    if (parsedUserAnswer === CORRECT_ANSWER) {
        feedback.innerHTML = "🎉 Правильно!";
        feedback.className = "correct";

        // Переключаем видимость кнопок
        checkBtn.style.display = 'none';
        nextBtn.style.display = 'inline-block';
    } else {
        feedback.innerHTML = "❌ Неверно. Попробуй еще раз!";
        feedback.className = "incorrect";
    }
}

// Отправка ответа по нажатию клавиши Enter
document.getElementById('userAnswer').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const checkBtn = document.getElementById('checkBtn');
        if (checkBtn.style.display !== 'none') {
            checkAnswer();
        } else {
            window.location.reload(); // Если уже ответил верно, Enter обновит страницу
        }
    }
});

