import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="💡 Enterprise Knowledge Intelligence", layout="wide")
st.title("💡 Enterprise Knowledge Intelligence System")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar navigation
option = st.sidebar.radio("Choose Query Type", ["Ask", "Ask Image", "Ask SQL"])

def call_api(endpoint, payload=None, files=None):
    """Generic API call function for text, SQL, or image."""
    url = f"http://127.0.0.1:8000/{endpoint}"
    try:
        if files:
            response = requests.post(url, files=files)
        else:
            response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return {}

# ------------------------------
# Ask Text
# ------------------------------
if option == "Ask":
    question = st.text_input("Enter your question")
    if st.button("Submit Question") and question:
        with st.spinner("Generating answer..."):
            data = call_api("ask", {"question": question})
            st.session_state.chat_history.append({
                "question": question,
                "answer": data.get("answer", "No response"),
                "confidence": data.get("confidence", 0.0),
                "hallucinated": data.get("hallucinated", False),
                "latency": data.get("latency", 0.0),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "text"
            })

# ------------------------------
# Ask Image
# ------------------------------
elif option == "Ask Image":
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if st.button("Submit Image") and uploaded_file:
        with st.spinner("Processing image..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = call_api("ask-image", files=files)
            st.session_state.chat_history.append({
                "question": f"Image: {uploaded_file.name}",
                "answer": data.get("answer", "No response"),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "image"
            })

# ------------------------------
# Ask SQL
# ------------------------------
elif option == "Ask SQL":
    sql_query = st.text_area("Enter SQL Query", height=100)
    if st.button("Submit SQL") and sql_query:
        with st.spinner("Executing SQL..."):
            data = call_api("ask-sql", {"question": sql_query})
            st.session_state.chat_history.append({
                "question": sql_query,
                "answer": data.get("answer", "No response"),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "sql"
            })

# ------------------------------
# Display Chat History
# ------------------------------
st.subheader("💬 Conversation History")
for idx, chat in enumerate(reversed(st.session_state.chat_history)):
    st.markdown(f"**Q ({chat['time']}):** {chat['question']}")
    st.text_area("Answer", chat['answer'], height=200, key=f"answer_{idx}")

    # Show confidence/hallucination/latency only for Ask (text) queries
    if chat['type'] == "text":
        cols = st.columns(3)
        cols[0].metric("Confidence", f"{chat['confidence']*100:.2f}%")
        cols[1].markdown(
            f"<span style='color:{'red' if chat['hallucinated'] else 'green'}; font-weight:bold'>Hallucinated: {chat['hallucinated']}</span>",
            unsafe_allow_html=True
        )
        cols[2].metric("Latency (s)", f"{chat['latency']:.2f}")

        # ------------------------------
        # Feedback Section
        # ------------------------------
        with st.expander("Provide Feedback"):
            rating = st.slider(f"Rate this answer (1-5)", 1, 5, 5, key=f"rating_{idx}")
            comment = st.text_area("Add comment (optional)", key=f"comment_{idx}")
            if st.button("Submit Feedback", key=f"feedback_btn_{idx}"):
                feedback_payload = {
                    "question": chat['question'],
                    "answer": chat['answer'],
                    "rating": rating,
                    "comment": comment
                }
                feedback_response = call_api("feedback", payload=feedback_payload)
                st.success(feedback_response.get("message", "Feedback submitted successfully."))

    st.markdown("---")