import streamlit as st
import requests
import time
import pandas as pd

# Flask API URL
API_URL = "http://localhost:5000/ask"

def get_response(prompt: str):
    try:
        response = requests.post(API_URL, json={"question": prompt})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def write_answer(data):
    if "error" in data:
        st.error(data["error"])
        return

    sql_query = data.get("sql_query", "")
    result = data.get("result", "")
    response_time = data.get("response_time", "")

    # Display SQL query with animated typing effect
    st.subheader("Generated SQL Query:")
    st.markdown(f"```sql\n{sql_query}\n```")

    # Display result with animated typing effect
    st.subheader("Query Result:")
    if isinstance(result, list) and result:  
        st.table(pd.DataFrame(result)) 
    else:
        st.write("No results found.")

    # Display response time
    st.subheader("Response Time:")
    st.write(response_time)

# Streamlit app
st.title("Crew Training Chatbot")

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new question
if prompt := st.chat_input("Ask a question"):
    # User input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = get_response(prompt)
        write_answer(answer)

        # Save assistant's response to session state
        if "error" not in answer:
            st.session_state.messages.append({"role": "assistant", "content": str(answer.get('sql_query', ''))})
