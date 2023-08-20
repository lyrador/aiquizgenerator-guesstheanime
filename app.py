import constants
import os
import re
import streamlit as st
from langchain.document_loaders import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator

import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv('cleanedQuizData.csv')

os.environ["OPENAI_API_KEY"] = constants.APIKEY
embeddings = OpenAIEmbeddings()

def initialiseSessionState():
    if 'generateDisabled' not in st.session_state:
        st.session_state['generateDisabled'] = False
    if 'startQuiz' not in st.session_state:
        st.session_state['startQuiz'] = False
    if 'quizSubmitted' not in st.session_state:
        st.session_state['quizSubmitted'] = False
    if 'answerInput' not in st.session_state:
        st.session_state['answerInput'] = ""
    if 'llmResponseArr' not in st.session_state:
        st.session_state['llmResponseArr'] = []
    
def resetState():
    st.session_state['generateDisabled'] = False
    st.session_state['startQuiz'] = False
    st.session_state['quizSubmitted'] = False
    st.session_state['answerInput'] = ""
    st.session_state['llmResponseArr'] = []
    
def generateQuiz():
    # Define masks for anime year range to test from
    startRangeYear_mask = df['start_year'] >= startRangeYear
    endRangeYear_mask = df['start_year'] <= endRangeYear
    year_mask = startRangeYear_mask | endRangeYear_mask
    # Apply the combined mask to the DataFrame
    filtered_years_df = df[year_mask]
    # Define masks for popularity ranking to test from
    final_df = filtered_years_df[filtered_years_df['popularity_rank'] <= topRankingNum]
    final_df = final_df[['title', 'synopsis']]
    newNumRows = len(final_df.index)
    if newNumRows < 3:
        st.write("Need to expand your selection!")
    else:
        st.session_state['generateDisabled'] = True
        st.session_state['startQuiz'] = True
        final_df = final_df.sample(n = 1)
        final_df.to_csv('generatedQuizData.csv', index=False)
        loader = CSVLoader('generatedQuizData.csv')
        index = VectorstoreIndexCreator().from_loaders([loader])
        query = 'I am making a guessing game. There are details about an anime in the csv provided. Use 30 to 40 words to rephrase and describe the synopsis starting with "This is a story about". After the description, write "///". After "///", give the title of the anime starting with "The anime title is". Do not use any character names in this reponse.'
        llmResponse = index.query(query)
        st.session_state['llmResponseArr'] = llmResponse.split("///")
  
initialiseSessionState()
st.title('Quiz Generator - Guess the Anime!')
startRangeYear = st.selectbox('Start Range - Anime that starting airing from year:', range(1978, 2023))
endRangeYear = st.selectbox('End Range - Anime that starting airing from year:', range(startRangeYear, 2023))
topRankingNum = st.number_input('Top X popularity ranking anime', min_value=3, max_value=50000, value=1000)  
st.button('Start Generating', disabled=st.session_state['generateDisabled'], on_click=generateQuiz)
        
if st.session_state['startQuiz']:
    with st.form("my_form"):
        st.session_state['answerInput'] = st.text_input(st.session_state['llmResponseArr'][0], placeholder="What is the title of this anime?")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state['quizSubmitted'] = True
        
if st.session_state['quizSubmitted']:
    title = st.session_state['llmResponseArr'][1]
    processedAnswerInput = re.sub(r'[\W_]', '', st.session_state['answerInput'].lower())
    correctAnswer = st.session_state['llmResponseArr'][1].split("anime title is")[1]
    processedCorrectAnswer = re.sub(r'[\W_]', '', correctAnswer.lower())
    if (processedAnswerInput == processedCorrectAnswer):
        st.markdown(f'<h1 style="color:#33ff33;font-size:20px;text-align: center">{title}</h1>', unsafe_allow_html=True)
        st.markdown(f'<h1 style="color:#33ff33;font-size:18px;text-align: center">{"Great job!"}</h1>', unsafe_allow_html=True)
    else:
        st.markdown(f'<h1 style="color:red;font-size:20px;text-align: center">{title}</h1>', unsafe_allow_html=True)
        st.markdown(f'<h1 style="color:red;font-size:18px;text-align: center">{"Aww... Try again next time!"}</h1>', unsafe_allow_html=True)
    if st.button('Reset', on_click=resetState):
        resetState()