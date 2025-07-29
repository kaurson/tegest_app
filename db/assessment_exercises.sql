CREATE TABLE IF NOT EXISTS assessment_exercises (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    options JSONB NOT NULL,
    answer TEXT NOT NULL,
    difficulty TEXT
);

INSERT INTO assessment_exercises (question, options, answer, difficulty) VALUES
('What is the Estonian word for "cat"?', '["kass", "koer", "lind", "hobune"]', 'kass', 'beginner'),
('Which of these means "hello" in Estonian?', '["tere", "aitäh", "palun", "head aega"]', 'tere', 'beginner'),
('What is the Estonian word for "dog"?', '["kass", "koer", "lind", "hobune"]', 'koer', 'beginner'),
('How do you say "thank you" in Estonian?', '["tere", "aitäh", "palun", "head aega"]', 'aitäh', 'beginner'),
('Which of these means "goodbye" in Estonian?', '["tere", "aitäh", "palun", "head aega"]', 'head aega', 'beginner'),
('What is the Estonian word for "bird"?', '["kass", "koer", "lind", "hobune"]', 'lind', 'beginner'),
('Which of these is a color in Estonian?', '["punane", "kass", "koer", "aitäh"]', 'punane', 'beginner'),
('What is the Estonian word for "horse"?', '["kass", "koer", "lind", "hobune"]', 'hobune', 'beginner'),
('How do you say "please" in Estonian?', '["tere", "aitäh", "palun", "head aega"]', 'palun', 'beginner'),
('Which of these is a number in Estonian?', '["üks", "kass", "aitäh", "koer"]', 'üks', 'beginner');

CREATE TABLE IF NOT EXISTS user_assessments (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    answers JSONB NOT NULL,
    score INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 