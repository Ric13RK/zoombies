CREATE TABLE record_answer_table(
    question_user_id text,
    question_id text,
    question_complexity text,
    question_correct_response boolean,
    question_tags JSON DEFAULT NULL,
    time_taken bigint
);
