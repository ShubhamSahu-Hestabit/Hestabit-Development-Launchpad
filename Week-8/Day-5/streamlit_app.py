import streamlit as st
import requests
import uuid

API_CHAT = "http://localhost:8000/chat"
API_GENERATE = "http://localhost:8000/generate"

SYSTEM_PROMPT = "You are a helpful healthcare assistant."

st.set_page_config(page_title="Healthcare Assistant", layout="wide")
st.title("🏥 Healthcare Assistant")
st.caption("Local LLM • FastAPI Backend")

# ------------------------
# Session State
# ------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------------
# Sidebar
# ------------------------
st.sidebar.header("⚙️ Settings")
mode = st.sidebar.radio("Mode", ["Chat", "Generate"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7)
top_p = st.sidebar.slider("Top P", 0.1, 1.0, 0.9)
top_k = st.sidebar.slider("Top K", 10, 100, 40)
if st.sidebar.button("Clear Chat"):
    st.session_state.history = []

# ------------------------
# Chat Mode
# ------------------------
if mode == "Chat":

    st.subheader("💬 Chat")
    for user, bot in st.session_state.history:
        st.chat_message("user").markdown(user)
        st.chat_message("assistant").markdown(bot)

    if prompt := st.chat_input("Ask a healthcare question..."):

        st.chat_message("user").markdown(prompt)
        payload = {
            "session_id": st.session_state.session_id,
            "system_prompt": SYSTEM_PROMPT,
            "message": prompt,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k
        }

        try:
            response = requests.post(API_CHAT, json=payload, stream=True)
            answer = ""
            placeholder = st.chat_message("assistant").empty()
            for chunk in response.iter_content(chunk_size=1):
                if chunk:
                    text = chunk.decode("utf-8")
                    answer += text
                    placeholder.markdown(answer + "▌")
            placeholder.markdown(answer)
        except Exception as e:
            answer = f"Backend error: {e}"
            st.chat_message("assistant").markdown(answer)

        st.session_state.history.append((prompt, answer))

# ------------------------
# Generate Mode
# ------------------------
else:
    st.subheader("🧠 Generate")
    prompt = st.text_area("Prompt", placeholder="Enter a healthcare prompt...")
    if st.button("Generate"):
        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k
        }
        try:
            response = requests.post(API_GENERATE, json=payload, stream=True)
            output = ""
            box = st.empty()
            for chunk in response.iter_content(chunk_size=1):
                if chunk:
                    text = chunk.decode("utf-8")
                    output += text
                    box.markdown(output + "▌")
            box.markdown(output)
        except Exception as e:
            st.error(f"Backend error: {e}")

st.divider()
st.caption("⚠️ Informational use only. Always consult a medical professional.")