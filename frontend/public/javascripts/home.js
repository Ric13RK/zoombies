const changePage = () => {
    let questionNumber = document.getElementById("questionCount").value;
    // Default question number to 5 if blank
    if (questionNumber == "") {
        questionNumber = 5;
    }

    document.location.href = "/quiz?questions=" + questionNumber;
}

const addUser = () => {
    let user = document.getElementById("user").value;
    document.cookie = "user=" + user;

    document.location.href = '/';
}