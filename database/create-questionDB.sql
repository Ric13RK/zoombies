CREATE TABLE questions_table( 
  id VARCHAR(30) primary key, 
  question json, 
  tags JSON DEFAULT NULL
);