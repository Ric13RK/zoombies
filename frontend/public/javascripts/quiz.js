// NOTE: This assumes the questionset has been injected into a variable named questions

let currentQuestion = 0;
let totalQuestions = questions.length;
let questionsCorrect = 0;
let currentTimestamp = 0;

const renderQuestion = () => {
    let questionContent = questions[currentQuestion];
    let answersHtml = "";
    for (let i = 0; i < questionContent.answers.length; i++) {
        answersHtml += `
        <div class="form-check">
            <input class="form-check-input" type="radio" name="answer" id="answer${i}">
            <label class="form-check-label" for="answer${i}" id="labelAnswer${i}">
                ${questionContent.answers[i]}
            </label>
        </div>
        `
    }
    let templateHtml = `
    <div>
        <h3>${questionContent.question}</h3>
        <br/>
        ${answersHtml}
        <br/>
        <div class="d-grid gap-2 col-6 mx-auto" id="submit-button">
            <button class="btn btn-block btn-secondary" onclick="checkAnswer()">Check Answer</button>
        </div>
    </div>
    `

    document.getElementById("questionPane").innerHTML = templateHtml;
}

const nextQuestion = () => {
    currentQuestion++;
    // Display the final screen if the quiz is over.
    if (currentQuestion >= totalQuestions) {
        document.getElementById("questionPane").innerHTML = `
            <div>
                <p class="lead text-center"> Congratulations you have finished the quiz </p>
                <h4 class="display-4 text-center">${questionsCorrect}/${questions.length}</h4>
                <p class="text-center">Your results will be available to your manager now</p>
                <br/>
                <div class="d-grid gap-2 col-6 mx-auto">
                    <a class="btn btn-success" href="/">Go Home</a>
                </div>
            </div>
        `
        // Break earlys
        return;
    }

    renderQuestion();
    currentTimestamp = Date.now();
}

const checkAnswer = () => {
    let timeTaken = Date.now() - currentTimestamp;
    let isCorrect = false;
    for (let i = 0; i < questions[currentQuestion].answers.length; i++) {
        let button = document.getElementById(`answer${i}`);
        if (button.checked) {
            if (questions[currentQuestion].answers[i] == questions[currentQuestion].correct_answer) {
                // Draw correct
                document.getElementById(`labelAnswer${i}`).innerHTML += `
                    <svg style="color:green" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check" viewBox="0 0 16 16">
                            <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/>
                    </svg>
                `
                isCorrect = true;
                questionsCorrect++;
            } else {
                // Draw incorrect
                document.getElementById(`labelAnswer${i}`).innerHTML += `
                    <svg style="color:red" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                    </svg>
                `
            }
        } else {
            button.disabled = true;
        }
        
    }

    let buttonClass = isCorrect ? "btn-success" : "btn-danger";
    document.getElementById("submit-button").innerHTML = `
        <button class="btn btn-block ${buttonClass}" onclick="nextQuestion()">Next Question</button>
    `

    let recordedAnswer = {
        user_id: getCookie("user"),
        question_id: questions[currentQuestion].id,
        correct_response: isCorrect,
        tags: questions[currentQuestion].tags,
        question_complexity: questions[currentQuestion].question_complexity,
        time_taken: timeTaken
    }

    fetch(api_endpoint + "/recordAnswer", {
        method: 'POST',
        body: JSON.stringify(recordedAnswer),
        mode: 'no-cors',
        headers: {
            'Content-type': 'application/json; charset=UTF-8'
        }
    })
}

// Direct from https://www.w3schools.com/js/js_cookies.asp
const getCookie = (cname) => {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

renderQuestion()
currentTimestamp = Date.now();