var express = require('express');
var router = express.Router();
const axios = require('axios')

const configuration = {
  api_endpoint: process.env.API_ENDPOINT || "https://virtserver.swaggerhub.com/nathan.duckett/zoombies_frontend/1.1"
}

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Quiz', userDefined: req.cookies.user });
});

router.get('/add', function(req, res, next) {
  res.render('addQuestion', { 
    title: 'Add Question',
    incorrectAnswerReference: [1, 2, 3],
    added: req.query.success
  });
});

router.post('/add', (req, res, next) => {
  let body = {
    question: req.body.title,
    correct_answer: req.body.correctAnswer,
    incorrect_answer: [
      req.body.incorrectAnswer1,
      req.body.incorrectAnswer2,
      req.body.incorrectAnswer3,
    ],
    question_complexity: req.body.complexity,
    tags: req.body.tags.split(",")
  };

  axios.post(configuration.api_endpoint + "/addQuestion", body).then(apiResponse => {
    if (apiResponse.status_code != 201) {
      res.redirect("/add?success=true")
    }
  })
});

router.get('/quiz', (req, res, next) => {
  let user = req.cookies.user;
  let questionCount = req.query.questions;
  
  // Return to root page if not providing a valid question count.
  if (questionCount < 1) {
    res.redirect("/")
  }

  axios.get(configuration.api_endpoint + "/getQuestions?user=" + user + "&number=" + questionCount).then(apiResponse => {
    questions = processQuestions(apiResponse.data)

    console.log(JSON.stringify(questions))
    res.render('quiz', {
      title: 'AWS Quiz',
      questions: JSON.stringify(questions),
      api_endpoint: configuration.api_endpoint
    });
  })
});

const processQuestions = (apiResponse) => {
  let questionsRefined = [];
  apiResponse["questions"].forEach((question) => {
    let answers = [question.correct_answer, ...question.incorrect_answer]
    shuffleArray(answers)
    question["answers"] = answers
    questionsRefined.push(question)
  });

  return questionsRefined
}

const shuffleArray = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
  }
}

module.exports = router;
