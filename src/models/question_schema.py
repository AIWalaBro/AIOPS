from typing import List
from pydantic import BaseModel, Field, validator

class MCQQuestion(BaseModel):
    question: str = Field(..., description="The question text")
    options: List[str] = Field(..., description="List of answer options")
    correct_answer: str = Field(..., description="The correct answer from the options provided")
    
    """ sometime llm give the question as a dict fromat then that time how it will be get clean UI.
        & this valdator only work on the question field not the options and correct answers fields.
    """
    @validator('question', pre=True)
    def clean_question(cls, value):
        if isinstance(value, dict):
            return value.get('description', str(value))
        return str(value)
    
    
class FillBlankQuetion(BaseModel):
    question: str = Field(..., description="The question text with '___'blanks")
    answer: str = Field(..., description="The correct answer for the blank")
    
    @validator('question', pre = True)
    def clean_question(cls, value):
        if isinstance(value, dict):
            return value.get('description', str(value))
        return str(value)
        