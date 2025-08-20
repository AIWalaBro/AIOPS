from langchain.prompts import PromptTemplate

mcq_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} multiple-choice question about {topic}.\n\n"
        "IMPORTANT GUIDELINES:\n"
        "1. Create diverse, plausible wrong options (distractors)\n"
        "2. Avoid using the same names/categories repeatedly\n"
        "3. Make wrong options believable but clearly incorrect\n"
        "4. Mix different types of answers (names, dates, concepts, places)\n"
        "5. Ensure all options are roughly the same length and format\n\n"
        "Return ONLY a JSON object with these exact fields:\n"
        "- 'question': A clear, specific question\n"
        "- 'options': An array of exactly 4 diverse possible answers\n"
        "- 'correct_answer': One of the options that is the correct answer\n\n"
        "GOOD Example (diverse options):\n"
        '{{\n'
        '    "question": "What is the capital of France?",\n'
        '    "options": ["London", "Berlin", "Paris", "Madrid"],\n'
        '    "correct_answer": "Paris"\n'
        '}}\n\n'
        "BAD Example (repetitive options):\n"
        '{{\n'
        '    "question": "Who built the Taj Mahal?",\n'
        '    "options": ["Akbar", "Jahangir", "Shah Jahan", "Aurangzeb"],\n'
        '    "correct_answer": "Shah Jahan"\n'
        '}}\n\n'
        "BETTER Example (diverse options):\n"
        '{{\n'
        '    "question": "Who built the Taj Mahal?",\n'
        '    "options": ["Shah Jahan", "Babur", "British East India Company", "Humayun"],\n'
        '    "correct_answer": "Shah Jahan"\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty"]
)

fill_blank_prompt_template = PromptTemplate(
    template=(
        "Generate a {difficulty} fill-in-the-blank question about {topic}.\n\n"
        "Return ONLY a JSON object with these exact fields:\n"
        "- 'question': A sentence with '_____' marking where the blank should be\n"
        "- 'answer': The correct word or phrase that belongs in the blank\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "The capital of France is _____.",\n'
        '    "answer": "Paris"\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty"]
)