from app.tool.base import BaseTool
import random
import re

class FillInTheBlankTool(BaseTool):
    name: str = "fill_in_the_blank"
    description: str = "Create a fill-in-the-blank exercise from a text by removing double characters from random words."
    parameters: dict = {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "The input text (about 10 sentences)."
            },
            "num_blanks": {
                "type": "integer",
                "description": "How many blanks to create (default: 5).",
                "default": 5
            },
            "user_answers": {
                "type": "array",
                "items": {"type": "string"},
                "description": "User's answers for the blanks (for checking)."
            },
            "correct_answers": {
                "type": "array",
                "items": {"type": "string"},
                "description": "The correct answers (for checking)."
            }
        },
        "required": ["text"]
    }

    async def execute(self, text: str, num_blanks: int = 5, user_answers=None, correct_answers=None):
        if user_answers is not None and correct_answers is not None:
            # Check mode
            score = 0
            feedback = []
            for user, correct in zip(user_answers, correct_answers):
                if user.strip().lower() == correct.lower():
                    score += 1
                    feedback.append(f"✅ {user} (correct)")
                else:
                    feedback.append(f"❌ {user} (correct: {correct})")
            return {
                "score": score,
                "total": len(correct_answers),
                "feedback": feedback
            }

        # Generate mode
        words = re.findall(r'\b\w+\b', text)
        double_char_words = [w for w in words if re.search(r'(.)\\1', w)]
        if len(double_char_words) == 0:
            return {"error": "No words with double characters found in the text."}
        selected = random.sample(double_char_words, min(num_blanks, len(double_char_words)))
        blanks = []
        correct_answers = []
        blanked_text = text
        for idx, word in enumerate(selected):
            blank_word = re.sub(r'(.)\\1', r'__', word, count=1)
            blanked_text = re.sub(r'\b' + re.escape(word) + r'\b', blank_word, blanked_text, count=1)
            blanks.append(blank_word)
            correct_answers.append(word)
        return {
            "exercise_text": blanked_text,
            "blanks": blanks,
            "correct_answers": correct_answers
        } 