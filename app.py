
import streamlit as st
import requests
from utils.logger import setup_logger

logger = setup_logger()

st.set_page_config(
    page_title="HR Resource Query Chatbot",
    page_icon="💼",
    layout="centered"
)

st.title("HR Resource Query Chatbot")
st.markdown("Find employees based on skills, experience, and projects.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
query = st.chat_input("Enter your query (e.g., 'Find Python developers with 3+ years experience')")
if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    try:
        # Send query to FastAPI backend
        response = requests.post(
            "http://localhost:8000/chat",
            json={"query": query},
            timeout=5
        )
        response.raise_for_status()
        result = response.json()

        with st.chat_message("assistant"):
            st.markdown(result["response"])
            # Display employee details in an expandable section
            for emp in result["employees"]:
                with st.expander(f"{emp['name']} Details"):
                    st.write(f"**Experience**: {emp['experience_years']} years")
                    st.write(f"**Skills**: {', '.join(emp['skills'])}")
                    st.write(f"**Projects**: {', '.join(emp['projects'])}")
                    st.write(f"**Availability**: {emp['availability'].capitalize()}")
                    st.write(f"**Relevance Score**: {emp['relevance_score']:.2%}")
        st.session_state.messages.append({"role": "assistant", "content": result["response"]})
        logger.info(f"Frontend processed query: {query}")
    except requests.RequestException as e:
        with st.chat_message("assistant"):
            st.error(f"Error connecting to backend: {str(e)}")
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})
        logger.error(f"Frontend error: {str(e)}")