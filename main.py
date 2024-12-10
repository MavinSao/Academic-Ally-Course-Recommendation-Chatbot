from backend.core import llm_core
import streamlit as st
import time

# Set the page config with a new emoji for the tab
st.set_page_config(
    page_title="✨ Academic Ally",
    page_icon="✨",
)

def stream_response_words(response, delay=0.02):
    """Yield words from the response one by one with a specified delay."""
    for word in response.split(" "):
        yield word + " "
        time.sleep(delay)

# Example queries that users can try
EXAMPLE_QUERIES = {
    "Programming Courses": "I want to learn programming. What courses would you recommend for a beginner?",
    "Data Science Track": "I'm interested in becoming a data scientist. What course pathway should I follow?",
    "Web Development": "What are the best courses for full-stack web development?",
    "Machine Learning": "I want to learn machine learning. Where should I start?",
    "Business Analytics": "I'm looking for courses in business analytics and visualization."
}

st.title("🎓 Academic Ally: Course Recommendation Chatbot")
st.subheader("Tailored course suggestions to suit your educational journey!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Add example queries section
st.sidebar.header("Try an Example Query")
example_selection = st.sidebar.selectbox(
    "Select an example query:",
    list(EXAMPLE_QUERIES.keys())
)

# Handle example query
if st.sidebar.button("Try this example"):
    example_query = EXAMPLE_QUERIES[example_selection]
    # Display user message
    with st.chat_message("user"):
        st.markdown(example_query)
    st.session_state.messages.append({"role": "user", "content": example_query})
    
    try:
        res = llm_core(query=example_query)
        with st.chat_message("assistant"):
            st.write_stream(stream_response_words(res))
        st.session_state.messages.append({"role": "assistant", "content": res})
    except Exception as e:
        st.error(f"An error occurred while fetching the response. {e}")
        with st.chat_message("assistant"):
            st.markdown("Sorry, I couldn't process that.")
        st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't process that."})

# Handle regular chat input
if prompt := st.chat_input("What courses are you interested in?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        res = llm_core(query=prompt)
        with st.chat_message("assistant"):
            st.write_stream(stream_response_words(res))
        st.session_state.messages.append({"role": "assistant", "content": res})
    except Exception as e:
        st.error(f"An error occurred while fetching the response. {e}")
        with st.chat_message("assistant"):
            st.markdown("Sorry, I couldn't process that.")
        st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't process that."})