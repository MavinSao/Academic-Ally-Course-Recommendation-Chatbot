import dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

dotenv.load_dotenv()

# Initialize Sentence Transformer embeddings
model_name = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# Define a prompt template for course recommendations
PROMPT_TEMPLATE = """
As an AI course recommendation expert, provide personalized, high-quality suggestions based on the user's interests, goals, and background.

Chat History: {chat_history}
User Query: {question}
Relevant Courses: {context}

Response Guidelines:
1. Tone: Warm, professional, and approachable.
2. Analysis: Consider user's query, history, and educational needs.
3. Recommendations: For each course, include:
   - Title and institution
   - Brief overview
   - Skills to be gained
   - Key topics
   - Level, duration, language
   - Ratings (if available)
   - Course URL (if available)
4. Personalization: Explain how courses align with user's interests and needs.

Note: All recommendations will be drawn strictly from the provided course context.

Recommendation:
"""

PROMPT = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["chat_history", "question", "context"])

# Initialize the language model (only once)
llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o-mini")

# Set up conversation memory with summarization
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=1000,
    memory_key="chat_history",
    return_messages=True
)

# Load vector store
vectorstore = FAISS.load_local("./faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# Create the conversational retrieval chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": PROMPT}
)

def llm_core(query: str):
    result = qa_chain({"question": query})
    return result["answer"]

if __name__ == "__main__":
    result = llm_core("I'm an intermediate programmer with Python experience, looking to dive deep into machine learning for financial applications.")
    print(result)