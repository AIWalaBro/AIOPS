import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helpers import *
from src.generator.question_generator import QuestionGenerator
load_dotenv()


def main():
    st.set_page_config(page_title= "AI Studdy Buddy", page_icon= "📚 ⛑️")
    # intialize our session state :- what is need of this
    # whenever we select an option from sidebar , it will refresh aumatically. 
    if "quiz_manager" not in st.session_state:
        st.session_state.quiz_manager  = QuizManager()
        
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated  = False
        
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted  = False
        
    if "rerun_trigger" not in st.session_state:
        st.session_state.rerun_trigger = False
        
    st.title(" AI Study Buddy")
    st.sidebar.header("Quiz Settings")
    
    question_type = st.sidebar.selectbox(
        "select Question Type",
        ["Multiple Choice", "Fill in the Blank"],
        index = 0
        
    )
    
    topic = st.sidebar.text_input("Enter Topic", placeholder= "Indian History, Geography, Sports, Economics")
    
    difficulty = st.sidebar.selectbox(
        "Difficulty Level",
        ["Easy", "Medium", "Hard"],
        index = 1
        
    )
    
    num_questions = st.sidebar.number_input(
        "Number of Questions",
        min_value = 1,
        max_value= 20,
        value = 5
        
    )
    
    
    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_submitted = False
        
        
        generator = QuestionGenerator()
        sucess = st.session_state.quiz_manager.generate_questions(
            generator, 
            question_type,
            topic,
            difficulty,
            num_questions
        )
        
        st.session_state.quiz_generated = sucess
        rerun() # why we rerun those changes reflect in the UI , for example when out of 4 option we choose one option
        
    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.header("Quiz Questions")
        st.session_state.quiz_manager.attempt_quiz()
        
        if st.button("Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            rerun()
            
    # now quiz is submitted and we want to show the results
    if st.session_state.quiz_submitted:
        st.header("Quiz Results")
        result_df = st.session_state.quiz_manager.generate_result_dataframe()
        
        
        if not result_df.empty:
            correct_count = result_df["is_correct"].sum()
            total_questions = len(result_df)
            
            score_percentage = (correct_count/ total_questions) * 100
            
            st.write(f"**{score_percentage }**")
            
            for _, result in result_df.iterrows():
                question_num = result['question_number']
                if result['is_correct']:
                    st.success(f"Question {question_num}: {result['question']}")
                else:
                    st.error(f"❌ Question {question_num}: {result['question']}")
                    st.write(f"Your Answer : {result["user_answer"]}")
                    st.write(f"Correct Answer : {result["correct_answer"]}")
                st.markdown("-------")
                
            if st.button("Save Results"):
                saved_file = st.session_state.quiz_manager.save_to_csv()
                if saved_file:
                    with open(saved_file, "rb") as f:
                        st.download_button(
                            label = "Download Results",
                            data = f.read(),
                            file_name = os.path.basename(saved_file),
                            mime = "text/csv"
                        )
                        
                else:
                    st.warning("No results to display. ")
                
if __name__ == "__main__":
    main()
                   