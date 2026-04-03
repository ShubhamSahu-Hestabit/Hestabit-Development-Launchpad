import streamlit as st
import requests
import time
from datetime import datetime
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Enterprise AI", layout="wide")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8001")

# ---------------- STYLING ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
h1 {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1>🚀 Enterprise Knowledge Intelligence</h1>
<p style='text-align:center; color:gray;'>Multimodal AI • RAG Powered</p>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Controls")
mode = st.sidebar.selectbox("Mode", ["💬 Ask", "🖼️ Ask Image", "🗄️ Ask SQL"])

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []

# ---------------- API ----------------
def call_api(endpoint, payload=None, files=None):
    url = f"{API_URL}/{endpoint}"
    try:
        if files:
            response = requests.post(url, files=files)
        else:
            response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return {}

# ---------------- ✅ FIXED STREAM ----------------
def stream_text(text):
    """Stream text while preserving formatting"""
    for line in text.split("\n"):
        yield line + "\n"
        time.sleep(0.05)

# ---------------- RENDER CHAT ----------------
for idx, chat in enumerate(st.session_state.chat_history):

    with st.chat_message("user"):
        st.markdown(chat["question"])

    with st.chat_message("assistant"):
        st.markdown(chat["answer"])

        if chat["type"] == "text":
            cols = st.columns(3)
            cols[0].metric("Confidence", f"{chat['confidence']*100:.2f}%")
            cols[1].metric("Hallucination", "Yes" if chat["hallucinated"] else "No")
            cols[2].metric("Latency", f"{chat['latency']:.2f}s")

            if chat["hallucinated"]:
                st.warning("⚠️ Possible hallucination detected")
            else:
                st.success("✅ Reliable answer")

            # FEEDBACK
            fb_cols = st.columns([1, 1, 6])

            if fb_cols[0].button("👍", key=f"like_{idx}"):
                call_api("feedback", {
                    "question": chat["question"],
                    "answer": chat["answer"],
                    "rating": 5,
                    "comment": ""
                })
                st.success("Feedback submitted 👍")

            if fb_cols[1].button("👎", key=f"dislike_{idx}"):
                st.session_state[f"fb_{idx}"] = True

            if st.session_state.get(f"fb_{idx}", False):
                comment = st.text_area("What went wrong?", key=f"comment_{idx}")

                if st.button("Submit Feedback", key=f"submit_{idx}"):
                    call_api("feedback", {
                        "question": chat["question"],
                        "answer": chat["answer"],
                        "rating": 1,
                        "comment": comment
                    })
                    st.success("Feedback submitted 👎")

# ---------------- INPUT ----------------

# TEXT MODE
if mode == "💬 Ask":
    question = st.chat_input("Ask something...")

    if question:
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("⏳ Thinking...")

            start = time.time()
            data = call_api("ask", {"question": question})
            latency = time.time() - start

            answer = data.get("answer", "No response")
            confidence = data.get("confidence", 0.0)
            hallucinated = data.get("hallucinated", False)

            placeholder.empty()

            # ✅ FIXED STREAMING DISPLAY
            full_text = ""
            for chunk in stream_text(answer):
                full_text += chunk
                placeholder.markdown(full_text)

            cols = st.columns(3)
            cols[0].metric("Confidence", f"{confidence*100:.2f}%")
            cols[1].metric("Hallucination", "Yes" if hallucinated else "No")
            cols[2].metric("Latency", f"{latency:.2f}s")

        st.session_state.chat_history.append({
            "question": question,
            "answer": answer,
            "confidence": confidence,
            "hallucinated": hallucinated,
            "latency": latency,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "text"
        })

# IMAGE MODE
elif mode == "🖼️ Ask Image":
    uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

    if uploaded_file and st.button("Analyze"):
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        data = call_api("ask-image", files=files)

        answer = data.get("answer", "No response")

        with st.chat_message("assistant"):
            st.image(uploaded_file)
            st.markdown(answer)

        st.session_state.chat_history.append({
            "question": f"Image: {uploaded_file.name}",
            "answer": answer,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "image"
        })

# SQL MODE
elif mode == "🗄️ Ask SQL":
    sql_query = st.chat_input("Enter SQL query...")

    if sql_query:
        with st.chat_message("user"):
            st.markdown(sql_query)

        with st.chat_message("assistant"):
            data = call_api("ask-sql", {"question": sql_query})
            answer = data.get("answer", "No response")
            st.markdown(answer)

        st.session_state.chat_history.append({
            "question": sql_query,
            "answer": answer,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "sql"
        })