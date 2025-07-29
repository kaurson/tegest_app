-- Estonian Language Learning App Database Schema for Supabase
-- This schema adapts the existing physics learning app structure for Estonian language learning

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- USERS AND AUTHENTICATION
-- ============================================================================

-- Users table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS users (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    native_language TEXT DEFAULT 'English',
    estonian_level TEXT DEFAULT 'beginner' CHECK (estonian_level IN ('beginner', 'elementary', 'intermediate', 'upper_intermediate', 'advanced')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    preferences JSONB DEFAULT '{}'::jsonb,
    study_goals TEXT[],
    daily_study_target_minutes INTEGER DEFAULT 30
);

-- ============================================================================
-- CORE LEARNING CONTENT
-- ============================================================================

-- Estonian language levels and topics
CREATE TABLE IF NOT EXISTS language_levels (
    id SERIAL PRIMARY KEY,
    level_name TEXT UNIQUE NOT NULL,
    level_code TEXT UNIQUE NOT NULL,
    description TEXT,
    estimated_hours INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Learning topics/categories
CREATE TABLE IF NOT EXISTS learning_topics (
    id SERIAL PRIMARY KEY,
    level_id INTEGER REFERENCES language_levels(id) ON DELETE CASCADE,
    topic_name TEXT NOT NULL,
    topic_description TEXT,
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    estimated_duration_minutes INTEGER,
    prerequisites INTEGER[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Vocabulary categories
CREATE TABLE IF NOT EXISTS vocabulary_categories (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES learning_topics(id) ON DELETE CASCADE,
    category_name TEXT NOT NULL,
    category_description TEXT,
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Vocabulary words
CREATE TABLE IF NOT EXISTS vocabulary_words (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES vocabulary_categories(id) ON DELETE CASCADE,
    estonian_word TEXT NOT NULL,
    english_translation TEXT NOT NULL,
    pronunciation TEXT,
    part_of_speech TEXT,
    example_sentence_est TEXT,
    example_sentence_en TEXT,
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    frequency_rating INTEGER CHECK (frequency_rating BETWEEN 1 AND 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Grammar rules
CREATE TABLE IF NOT EXISTS grammar_rules (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES learning_topics(id) ON DELETE CASCADE,
    rule_name TEXT NOT NULL,
    rule_description TEXT NOT NULL,
    rule_explanation TEXT,
    examples JSONB,
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- LESSON MANAGEMENT (Adapted from existing Lessons table)
-- ============================================================================

-- Main lessons table
CREATE TABLE IF NOT EXISTS lessons (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id UUID UNIQUE NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES learning_topics(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    description TEXT,
    lesson_type TEXT DEFAULT 'interactive' CHECK (lesson_type IN ('interactive', 'vocabulary', 'grammar', 'conversation', 'reading', 'listening')),
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    steps TEXT[] NOT NULL,
    step_statuses TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    step_responses JSONB[] NOT NULL DEFAULT ARRAY[]::JSONB[],
    current_step_index INTEGER DEFAULT 0,
    total_steps INTEGER GENERATED ALWAYS AS (array_length(steps, 1)) STORED,
    completed_steps INTEGER GENERATED ALWAYS AS (
        array_length(
            array_remove(step_statuses, 'not_started'),
            1
        )
    ) STORED,
    progress_percentage INTEGER GENERATED ALWAYS AS (
        CASE 
            WHEN array_length(steps, 1) > 0 
            THEN (array_length(array_remove(step_statuses, 'not_started'), 1) * 100) / array_length(steps, 1)
            ELSE 0
        END
    ) STORED,
    status TEXT DEFAULT 'in_progress' CHECK (status IN ('not_started', 'in_progress', 'completed', 'paused', 'abandoned')),
    estimated_duration_minutes INTEGER,
    actual_duration_minutes INTEGER,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- SESSION MANAGEMENT (Adapted from existing lesson_sessions table)
-- ============================================================================

-- Learning sessions
CREATE TABLE IF NOT EXISTS learning_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id UUID UNIQUE NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    lesson_id UUID REFERENCES lessons(id) ON DELETE SET NULL,
    session_type TEXT DEFAULT 'lesson' CHECK (session_type IN ('lesson', 'practice', 'quiz', 'conversation', 'review')),
    messages JSONB[] DEFAULT ARRAY[]::JSONB[],
    responses JSONB[] DEFAULT ARRAY[]::JSONB[],
    vocabulary_encountered TEXT[],
    grammar_rules_practiced INTEGER[],
    mistakes_made JSONB[],
    corrections_given JSONB[],
    session_duration_seconds INTEGER,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- EXERCISES AND ASSESSMENTS
-- ============================================================================

-- Exercise types
CREATE TABLE IF NOT EXISTS exercise_types (
    id SERIAL PRIMARY KEY,
    type_name TEXT UNIQUE NOT NULL,
    type_description TEXT,
    difficulty_range INTEGER[],
    estimated_duration_seconds INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Exercises
CREATE TABLE IF NOT EXISTS exercises (
    id SERIAL PRIMARY KEY,
    exercise_type_id INTEGER REFERENCES exercise_types(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES learning_topics(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    question TEXT NOT NULL,
    options JSONB, -- For multiple choice, true/false, etc.
    correct_answer TEXT,
    explanation TEXT,
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    points INTEGER DEFAULT 1,
    time_limit_seconds INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User exercise attempts
CREATE TABLE IF NOT EXISTS exercise_attempts (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    exercise_id INTEGER REFERENCES exercises(id) ON DELETE CASCADE,
    session_id UUID REFERENCES learning_sessions(session_id) ON DELETE CASCADE,
    user_answer TEXT,
    is_correct BOOLEAN,
    time_taken_seconds INTEGER,
    points_earned INTEGER,
    attempted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- PROGRESS TRACKING
-- ============================================================================

-- User progress by topic
CREATE TABLE IF NOT EXISTS user_progress (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES learning_topics(id) ON DELETE CASCADE,
    vocabulary_mastered INTEGER DEFAULT 0,
    grammar_rules_mastered INTEGER DEFAULT 0,
    exercises_completed INTEGER DEFAULT 0,
    exercises_correct INTEGER DEFAULT 0,
    time_spent_minutes INTEGER DEFAULT 0,
    proficiency_level INTEGER DEFAULT 1 CHECK (proficiency_level BETWEEN 1 AND 5),
    last_practiced TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, topic_id)
);

-- Vocabulary learning progress
CREATE TABLE IF NOT EXISTS vocabulary_progress (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    word_id INTEGER REFERENCES vocabulary_words(id) ON DELETE CASCADE,
    learning_status TEXT DEFAULT 'new' CHECK (learning_status IN ('new', 'learning', 'reviewing', 'mastered')),
    correct_attempts INTEGER DEFAULT 0,
    incorrect_attempts INTEGER DEFAULT 0,
    last_reviewed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    next_review TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, word_id)
);

-- Study streaks and statistics
CREATE TABLE IF NOT EXISTS user_statistics (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    total_study_time_minutes INTEGER DEFAULT 0,
    current_streak_days INTEGER DEFAULT 0,
    longest_streak_days INTEGER DEFAULT 0,
    lessons_completed INTEGER DEFAULT 0,
    exercises_completed INTEGER DEFAULT 0,
    vocabulary_mastered INTEGER DEFAULT 0,
    grammar_rules_mastered INTEGER DEFAULT 0,
    total_points INTEGER DEFAULT 0,
    level_progress JSONB DEFAULT '{}'::jsonb,
    achievements JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Daily study logs
CREATE TABLE IF NOT EXISTS daily_study_logs (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    study_date DATE NOT NULL,
    total_time_minutes INTEGER DEFAULT 0,
    lessons_completed INTEGER DEFAULT 0,
    exercises_completed INTEGER DEFAULT 0,
    vocabulary_learned INTEGER DEFAULT 0,
    grammar_rules_practiced INTEGER DEFAULT 0,
    points_earned INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, study_date)
);

-- ============================================================================
-- AGENT SYSTEM (Adapted from existing prompts table)
-- ============================================================================

-- Agent prompts and configurations
CREATE TABLE IF NOT EXISTS agent_prompts (
    id SERIAL PRIMARY KEY,
    agent_name TEXT UNIQUE NOT NULL,
    agent_type TEXT NOT NULL CHECK (agent_type IN ('tutor', 'conversation', 'grammar', 'vocabulary', 'pronunciation', 'assessment')),
    system_prompt TEXT NOT NULL,
    user_secondary_prompt TEXT,
    context_instructions TEXT,
    difficulty_adjustment_rules JSONB,
    personality_traits JSONB,
    language_style TEXT DEFAULT 'formal' CHECK (language_style IN ('formal', 'informal', 'mixed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Agent conversation history
CREATE TABLE IF NOT EXISTS agent_conversations (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id UUID REFERENCES learning_sessions(session_id) ON DELETE CASCADE,
    agent_name TEXT NOT NULL,
    conversation_messages JSONB[] DEFAULT ARRAY[]::JSONB[],
    conversation_summary TEXT,
    language_used TEXT DEFAULT 'Estonian',
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    topics_covered TEXT[],
    vocabulary_introduced TEXT[],
    grammar_focus TEXT[],
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- CONTENT MANAGEMENT
-- ============================================================================

-- Learning materials (texts, audio, etc.)
CREATE TABLE IF NOT EXISTS learning_materials (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES learning_topics(id) ON DELETE CASCADE,
    material_type TEXT NOT NULL CHECK (material_type IN ('text', 'audio', 'video', 'image', 'interactive')),
    title TEXT NOT NULL,
    content TEXT,
    file_url TEXT,
    file_size_bytes INTEGER,
    duration_seconds INTEGER,
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    vocabulary_used TEXT[],
    grammar_rules_covered INTEGER[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Cultural content and context
CREATE TABLE IF NOT EXISTS cultural_content (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT CHECK (category IN ('history', 'traditions', 'customs', 'geography', 'literature', 'music', 'food')),
    difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 5),
    related_vocabulary TEXT[],
    related_grammar_rules INTEGER[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Users indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_estonian_level ON users(estonian_level);

-- Lessons indexes
CREATE INDEX IF NOT EXISTS idx_lessons_user_id ON lessons(user_id);
CREATE INDEX IF NOT EXISTS idx_lessons_topic_id ON lessons(topic_id);
CREATE INDEX IF NOT EXISTS idx_lessons_status ON lessons(status);
CREATE INDEX IF NOT EXISTS idx_lessons_created_at ON lessons(created_at);

-- Sessions indexes
CREATE INDEX IF NOT EXISTS idx_learning_sessions_user_id ON learning_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_sessions_lesson_id ON learning_sessions(lesson_id);
CREATE INDEX IF NOT EXISTS idx_learning_sessions_started_at ON learning_sessions(started_at);

-- Vocabulary indexes
CREATE INDEX IF NOT EXISTS idx_vocabulary_words_category_id ON vocabulary_words(category_id);
CREATE INDEX IF NOT EXISTS idx_vocabulary_words_difficulty ON vocabulary_words(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_vocabulary_words_estonian ON vocabulary_words(estonian_word);

-- Progress indexes
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_topic_id ON user_progress(topic_id);
CREATE INDEX IF NOT EXISTS idx_vocabulary_progress_user_id ON vocabulary_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_vocabulary_progress_word_id ON vocabulary_progress(word_id);
CREATE INDEX IF NOT EXISTS idx_vocabulary_progress_next_review ON vocabulary_progress(next_review);

-- Exercise indexes
CREATE INDEX IF NOT EXISTS idx_exercises_topic_id ON exercises(topic_id);
CREATE INDEX IF NOT EXISTS idx_exercises_type_id ON exercises(exercise_type_id);
CREATE INDEX IF NOT EXISTS idx_exercise_attempts_user_id ON exercise_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_exercise_attempts_exercise_id ON exercise_attempts(exercise_id);

-- Daily logs indexes
CREATE INDEX IF NOT EXISTS idx_daily_study_logs_user_id ON daily_study_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_daily_study_logs_study_date ON daily_study_logs(study_date);

-- ============================================================================
-- TRIGGERS AND FUNCTIONS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_lessons_updated_at BEFORE UPDATE ON lessons FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_learning_sessions_updated_at BEFORE UPDATE ON learning_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_vocabulary_words_updated_at BEFORE UPDATE ON vocabulary_words FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_grammar_rules_updated_at BEFORE UPDATE ON grammar_rules FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_learning_topics_updated_at BEFORE UPDATE ON learning_topics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_exercises_updated_at BEFORE UPDATE ON exercises FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_progress_updated_at BEFORE UPDATE ON user_progress FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_vocabulary_progress_updated_at BEFORE UPDATE ON vocabulary_progress FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_statistics_updated_at BEFORE UPDATE ON user_statistics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_agent_prompts_updated_at BEFORE UPDATE ON agent_prompts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_learning_materials_updated_at BEFORE UPDATE ON learning_materials FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to calculate vocabulary mastery
CREATE OR REPLACE FUNCTION calculate_vocabulary_mastery(user_uuid UUID)
RETURNS INTEGER AS $$
BEGIN
    RETURN (
        SELECT COUNT(*) 
        FROM vocabulary_progress 
        WHERE user_id = user_uuid AND learning_status = 'mastered'
    );
END;
$$ LANGUAGE plpgsql;

-- Function to update user statistics
CREATE OR REPLACE FUNCTION update_user_statistics()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_statistics (user_id, vocabulary_mastered)
    VALUES (NEW.user_id, calculate_vocabulary_mastery(NEW.user_id))
    ON CONFLICT (user_id) 
    DO UPDATE SET 
        vocabulary_mastered = calculate_vocabulary_mastery(NEW.user_id),
        updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update statistics when vocabulary progress changes
CREATE TRIGGER update_stats_on_vocabulary_progress 
    AFTER INSERT OR UPDATE ON vocabulary_progress 
    FOR EACH ROW EXECUTE FUNCTION update_user_statistics();

-- ============================================================================
-- SAMPLE DATA INSERTION
-- ============================================================================

-- Insert basic language levels
INSERT INTO language_levels (level_name, level_code, description, estimated_hours) VALUES
('Beginner', 'A1', 'Basic Estonian for beginners', 80),
('Elementary', 'A2', 'Elementary Estonian communication', 160),
('Intermediate', 'B1', 'Intermediate Estonian proficiency', 240),
('Upper Intermediate', 'B2', 'Upper intermediate Estonian', 320),
('Advanced', 'C1', 'Advanced Estonian mastery', 400);

-- Insert basic exercise types
INSERT INTO exercise_types (type_name, type_description, difficulty_range, estimated_duration_seconds) VALUES
('multiple_choice', 'Multiple choice questions', ARRAY[1,5], 60),
('true_false', 'True or false statements', ARRAY[1,4], 45),
('fill_in_blank', 'Fill in the blank exercises', ARRAY[2,5], 90),
('translation', 'Translation exercises', ARRAY[2,5], 120),
('pronunciation', 'Pronunciation practice', ARRAY[1,5], 60),
('conversation', 'Conversation practice', ARRAY[2,5], 300),
('grammar_exercise', 'Grammar-focused exercises', ARRAY[2,5], 120),
('vocabulary_matching', 'Vocabulary matching exercises', ARRAY[1,4], 75);

-- Insert basic agent prompts
INSERT INTO agent_prompts (agent_name, agent_type, system_prompt, user_secondary_prompt, language_style) VALUES
('estonian_tutor', 'tutor', 'You are a patient and encouraging Estonian language tutor. Help students learn Estonian through clear explanations, examples, and practice exercises.', 'Please help me learn Estonian by explaining this concept and providing practice exercises.', 'formal'),
('conversation_partner', 'conversation', 'You are a friendly Estonian conversation partner. Engage in natural conversations while helping the student practice their Estonian speaking skills.', 'Let''s have a conversation in Estonian about everyday topics.', 'mixed'),
('grammar_expert', 'grammar', 'You are an expert in Estonian grammar. Explain grammar rules clearly with examples and help students understand the structure of the Estonian language.', 'Please explain this Estonian grammar rule and provide examples.', 'formal'),
('vocabulary_helper', 'vocabulary', 'You are a vocabulary assistant for Estonian learners. Help students learn new words, their meanings, and how to use them in context.', 'Please help me learn these Estonian words and how to use them.', 'formal');

-- ============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================================================

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE vocabulary_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_statistics ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_study_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE exercise_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_conversations ENABLE ROW LEVEL SECURITY;

-- Users can only access their own data
CREATE POLICY "Users can view own profile" ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON users FOR UPDATE USING (auth.uid() = id);

-- Lessons policies
CREATE POLICY "Users can view own lessons" ON lessons FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own lessons" ON lessons FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own lessons" ON lessons FOR UPDATE USING (auth.uid() = user_id);

-- Sessions policies
CREATE POLICY "Users can view own sessions" ON learning_sessions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own sessions" ON learning_sessions FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own sessions" ON learning_sessions FOR UPDATE USING (auth.uid() = user_id);

-- Progress policies
CREATE POLICY "Users can view own progress" ON user_progress FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own progress" ON user_progress FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own progress" ON user_progress FOR UPDATE USING (auth.uid() = user_id);

-- Vocabulary progress policies
CREATE POLICY "Users can view own vocabulary progress" ON vocabulary_progress FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own vocabulary progress" ON vocabulary_progress FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own vocabulary progress" ON vocabulary_progress FOR UPDATE USING (auth.uid() = user_id);

-- Statistics policies
CREATE POLICY "Users can view own statistics" ON user_statistics FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own statistics" ON user_statistics FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own statistics" ON user_statistics FOR UPDATE USING (auth.uid() = user_id);

-- Daily logs policies
CREATE POLICY "Users can view own daily logs" ON daily_study_logs FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own daily logs" ON daily_study_logs FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own daily logs" ON daily_study_logs FOR UPDATE USING (auth.uid() = user_id);

-- Exercise attempts policies
CREATE POLICY "Users can view own exercise attempts" ON exercise_attempts FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own exercise attempts" ON exercise_attempts FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Agent conversations policies
CREATE POLICY "Users can view own conversations" ON agent_conversations FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own conversations" ON agent_conversations FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own conversations" ON agent_conversations FOR UPDATE USING (auth.uid() = user_id);

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE users IS 'User profiles and preferences for Estonian language learning';
COMMENT ON TABLE language_levels IS 'CEFR language levels for Estonian learning progression';
COMMENT ON TABLE learning_topics IS 'Topics and themes for Estonian language learning';
COMMENT ON TABLE vocabulary_categories IS 'Categories for organizing Estonian vocabulary';
COMMENT ON TABLE vocabulary_words IS 'Individual Estonian vocabulary words with translations and examples';
COMMENT ON TABLE grammar_rules IS 'Estonian grammar rules and explanations';
COMMENT ON TABLE lessons IS 'Learning lessons with steps and progress tracking';
COMMENT ON TABLE learning_sessions IS 'Individual learning sessions with conversation history';
COMMENT ON TABLE exercises IS 'Learning exercises and assessments';
COMMENT ON TABLE user_progress IS 'User progress tracking by topic';
COMMENT ON TABLE vocabulary_progress IS 'Individual vocabulary word learning progress';
COMMENT ON TABLE user_statistics IS 'Overall user learning statistics and achievements';
COMMENT ON TABLE daily_study_logs IS 'Daily study activity logs';
COMMENT ON TABLE agent_prompts IS 'AI agent prompts and configurations';
COMMENT ON TABLE agent_conversations IS 'Conversation history with AI agents';
COMMENT ON TABLE learning_materials IS 'Learning content and resources';
COMMENT ON TABLE cultural_content IS 'Cultural context and information for Estonian learning'; 