import os
import streamlit as st
import pandas as pd
from src.generator.question_generator import QuestionGenerator

"""
   Basically rerun your streamlit app by changing your  sesssion state.
   by changing session state.
   
   e.g :- generate MCQ Question then again generate MCQ Question.
"""

def rerun():
    st.session_state["rerun_trigger"] = not st.session_state["rerun_trigger"]

    
class QuizManager:
    def __init__(self):
        self.questions = []
        self.user_answers = []
        self.results = []
        
        
    """
        Number of questions generated previously that stored inside the question, refresh the page again
        it will generate the new questions.
    """ 
           
    def generate_questions(self, generator: QuestionGenerator, question_type: str, topic: str, difficulty: str, num_questions: int):
        self.questions = []
        self.user_answers = []
        self.results = []
        
        # Reset generator context to avoid using previous options
        generator.reset_context()
        
        try:
            for _ in range(num_questions):
                if question_type == "Multiple Choice":
                    question = generator.generate_mcq(topic, difficulty.lower())
                    
                    self.questions.append({
                        'type': 'MCQ',
                        'question': question.question,
                        'options': question.options,
                        'correct_answer': question.correct_answer
                    })
                    
                else:
                    question = generator.generate_fill_blank(topic, difficulty.lower())
                        
                    self.questions.append({
                        'type': 'fill in the blank',
                        'question': question.question,
                        'correct_answer': question.answer
                })
                    
        except Exception as e:
            st.error(f"Error generating questions: {str(e)}")
            return False
    
        return True
    
    # user attempting Quiz and we collecting his answers
    def attempt_quiz(self):
        # Initialize user_answers list if not already initialized
        if len(self.user_answers) != len(self.questions):
            self.user_answers = [None] * len(self.questions)
            
        for looping_number, quest in enumerate(self.questions):
            st.markdown(f"**Question {looping_number + 1} : {quest['question']}**")
            
            if quest['type'] == 'MCQ':
                user_answer = st.radio(
                    f"Select the correct answer for Question {looping_number + 1}",
                    quest['options'],
                    key = f"mcq_{looping_number}"
                    )
                self.user_answers[looping_number] = user_answer
            else:
                user_answer = st.text_input(
                    f"Fill in the blank for Question {looping_number + 1}",
                    key = f"fill_blank_{looping_number}"
                )
                
                self.user_answers[looping_number] = user_answer
                
                
    # evaluating the user's answers and storing the results
    def evaluate_quiz(self):
        self.results = []
        
        for i, (quest, user_answer) in enumerate(zip(self.questions, self.user_answers)):
            result_dict = {
                'question_number': i+1,
                'question': quest['question'],
                'question_type': quest['type'],
                'user_answer': user_answer,
                'correct_answer': quest['correct_answer'], 
                "is_correct": False,
                
            }
            
            # lets check the correct answer
            
            if quest['type'] == 'MCQ':
                result_dict['options'] = quest['options']
                result_dict['is_correct'] = user_answer == quest['correct_answer'] if user_answer else False
                
            else:
                result_dict['options'] = []
                if user_answer:
                    result_dict['is_correct'] = user_answer.strip().lower() == quest['correct_answer'].strip().lower()
                else:
                    result_dict['is_correct'] = False
                
            self.results.append(result_dict)
            
            
    # Now we will generate the results of DataFrame and display it    
    def generate_result_dataframe(self):
        if not self.results:
            return pd.DataFrame()
        return pd.DataFrame(self.results)
    
    # but we dont want in dataframe , we want in report file and it will be genrated via CSV file.
    def save_to_csv(self, filename_prefix = "quiz_results"):
        if not self.results:
            st.warning("No results to save.")
            return None
        df = self.generate_result_dataframe()
        
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{filename_prefix}_{timestamp}.csv"
        
        os.makedirs('results', exist_ok = True)
        full_path = os.path.join('results', unique_filename)
    
        try:
            df.to_csv(full_path, index= False)
            st.success("Result saved Successfully")
            return full_path
        except Exception as  e:
            st.error(f"Failed to save results: {e}")
            return None
                
                
                    
                    
            