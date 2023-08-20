# AI Quiz Generator - Guess the Anime!
 An AI Quiz Generator that utilises LLM to generate fun and accurate descriptions of anime without character names for you to guess
 
 ![AIQuizGenerator-GuessTheAnimeScreenshot](https://github.com/lyrador/aiquizgenerator-guesstheanime/assets/65401176/4a97414b-ce30-403e-88f7-1a75a615283d)

Steps to Use:
1. Clone repo and open up directory in terminal
2. Install the required libraries with
```
pip install pandas langchain openai streamlit chromadb tiktoken
```
3. Create an OpenAI account and create a new secretkey at https://platform.openai.com/account/api-keys
4. Copy the key and replace the value in APIKEY in constants.py
5. Run the app with
```
streamlit run appname.py
```

Credits:
Original anime dataset obtained from https://www.kaggle.com/datasets/svanoo/myanimelist-dataset and cleaned with CleanAnimeDatasetCSV.ipynb
