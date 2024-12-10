# ✨🎓 Academic Ally: Course Recommendation Chatbot

This is an AI-powered course recommendation chatbot that provides personalized course suggestions based on user interests and goals. This Streamlit application uses advanced natural language processing and retrieval techniques to offer tailored educational recommendations.

## Features

- Interactive chat interface
- Personalized course recommendations
- Integration with OpenAI's GPT-4o-mini model
- Efficient retrieval using FAISS vectorstore
- Conversation memory for context-aware responses

## Prerequisites

- Python 3.7+
- OpenAI API key

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Start chatting with the bot and get personalized course recommendations!

## How It Works

1. The chatbot uses a FAISS index to efficiently retrieve relevant course information based on user queries.
2. It employs the LangChain library to create a conversational retrieval chain, combining retrieved information with a language model.
3. The chatbot maintains conversation history to provide context-aware responses.
4. Responses are generated using a custom prompt template that ensures detailed and personalized course recommendations.


## Acknowledgments

- This project uses the LangChain library for building the conversational AI pipeline.
- Course data is retrieved using a FAISS index for efficient similarity search.
---

For any questions or support, please open an issue in the GitHub repository.
