from src.models.question_schema import MCQQuestion, FillBlankQuetion
from src.prompts.templates import mcq_prompt_template, fill_blank_prompt_template
from src.llm.groq_client import get_groq_llm
from src.common.custom_exception import CustomException
from src.common.logger import get_logger
from src.config.settings import settings
from langchain.output_parsers import PydanticOutputParser

"""
           why we return like this?
           becausewe want to use the logger with the class name generator so that this logger will be associated.
           so that this logger will be question generator specifically.
"""
class QuestionGenerator:
    def __init__(self):
        self.llm = get_groq_llm()
        self.logger = get_logger(self.__class__.__name__)
        self.used_options = set()  # Track used options to avoid repetition
        
    def reset_context(self):
        """Reset the used options for a new quiz generation session"""
        self.used_options.clear()
        self.logger.info("Context reset - cleared used options")
          
    """
    Now we creating the private helper method, so that we can send our prompt to the LLM, and pass the response and retry
    also if something goes wrong.
    """
    
    def _retry_and_parse(self, prompt, parser, topic, difficulty, avoid_options=None):
        for attempt in range(settings.MAX_RETIRES):
            try:
                self.logger.info(f"Generating question for topic {topic} with difficulty {difficulty}, attempt {attempt + 1}")
                
                # Create enhanced prompt with context about options to avoid
                prompt_kwargs = {"topic": topic, "difficulty": difficulty}
                if avoid_options:
                    avoid_list = ", ".join(list(avoid_options)[:10])  # Limit to avoid very long prompts
                    enhanced_prompt = prompt.template + f"\n\nIMPORTANT: Avoid using these previously used options: {avoid_list}\nGenerate completely different and diverse options."
                    from langchain.prompts import PromptTemplate
                    temp_prompt = PromptTemplate(template=enhanced_prompt, input_variables=prompt.input_variables)
                    response = self.llm.invoke(temp_prompt.format(**prompt_kwargs))
                else:
                    response = self.llm.invoke(prompt.format(**prompt_kwargs))
                    
                parsed = parser.parse(response.content)
                self.logger.info(f"Successfully generated the questions")
                return parsed
            except Exception as e:
                self.logger.error(f"Error on attempt {attempt + 1}: {str(e)}")
                if attempt == settings.MAX_RETIRES - 1:
                    raise CustomException(f"Failed to generate question after {settings.MAX_RETIRES} attempts", e)
            
                
    def generate_mcq(self, topic: str, difficulty: str = "medium") -> MCQQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object = MCQQuestion)
            
            # Pass previously used options to avoid repetition
            avoid_options = self.used_options if len(self.used_options) > 0 else None
            question = self._retry_and_parse(mcq_prompt_template, parser, topic, difficulty, avoid_options)
            
            if len(question.options) != 4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ Structure")
            
            # Track the options used in this question
            for option in question.options:
                self.used_options.add(option)
            
            self.logger.info(f"Generated a valid MCQ Question")
            return question
        except Exception as e:
            self.logger.error(f"Failed to generate MCQ: {str(e)}")
            raise CustomException(f"Failed to generate MCQ for topic {topic} with difficulty {difficulty}", e)
        
        
    def generate_fill_blank(self, topic: str, difficulty: str = "medium") -> FillBlankQuetion:
        try:
            parser = PydanticOutputParser(pydantic_object = FillBlankQuetion)
            question = self._retry_and_parse(fill_blank_prompt_template, parser, topic, difficulty)
            
            if "___" not in question.question:
                raise ValueError("Fill in the blank need '___'")
            
            self.logger.info(f"Gnerated a valid Fill in the blank Question")
            return question
        except Exception as e:
            self.logger.error(f"Failed to Filledup: {str(e)}")
            raise CustomException(f"Fill in the blank genarated failed", e)


                