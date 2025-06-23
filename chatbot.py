import streamlit as st
import requests

# Konfigurasi API
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
MODEL = "openai/gpt-3.5-turbo"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "X-Title": "AI Chatbot Streamlit"
}

# ---------------- PAGE TITLE ----------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")
st.markdown("Powered by [Mistral AI](https://mistral.ai/) & OpenRouter")

# ---------------- STYLING ----------------
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet">
    <style>
    html, body, div, p {
        font-family: 'Inter', sans-serif;
    }
    .message-container {
        display: flex;
        margin-bottom: 1rem;
        align-items: flex-start;
    }
    .user-container {
        flex-direction: row-reverse;
    }
    .avatar {
        width: 40px;
        height: 40px;
        margin: 5px;
        font-size: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .chat-message {
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #1E88E5;
        color: white;
        margin-left: auto;
    }
    .bot-message {
        background-color: #f5f5f5;
        color: black;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE INIT ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- DISPLAY CHAT ----------------
for chat in st.session_state.chat_history:
    role = chat["role"]
    message = chat["content"]

    avatar = "🤖" if role == "assistant" else "👤"
    role_class = "bot-message" if role == "assistant" else "user-message"
    container_class = "message-container user-container" if role == "user" else "message-container"

    st.markdown(f"""
        <div class="{container_class}">
            <div class="avatar">{avatar}</div>
            <div class="chat-message {role_class}">
                {message}
            </div>
        </div>
    """, unsafe_allow_html=True)

# ---------------- USER INPUT + ACTION BUTTONS ----------------
chat_col, btn_col1, btn_col2 = st.columns([8, 1, 1])

with chat_col:
    user_input = st.chat_input("Type your message here...")

with btn_col1:
    if st.button("🧹", help="Clear chat"):
        st.session_state.chat_history = []
        st.experimental_rerun()

with btn_col2:
    if st.session_state.chat_history:
        chat_text = "\n\n".join([
            f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.chat_history
        ])
        st.download_button("📥", chat_text, file_name="chat_history.txt", mime="text/plain", help="Download chat")

# ---------------- HANDLE INPUT & API ----------------
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        payload = {
            "model": MODEL,
            "messages": [
            {"role": "system", "content": "You are a helpful assistant."}] + st.session_state.chat_history
            ]
        }

        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "choices" in data and data["choices"]:
                bot_reply = data["choices"][0]["message"]["content"]
            else:
                bot_reply = "Maaf, tidak ada respons dari AI."

        except requests.exceptions.Timeout:
            bot_reply = "Permintaan timeout. Silakan coba lagi nanti."
        except requests.exceptions.HTTPError as http_err:
            bot_reply = f"HTTP error: {http_err}"
        except requests.exceptions.RequestException as req_err:
            bot_reply = f"Request error: {req_err}"
        except (KeyError, ValueError) as parse_err:
            bot_reply = f"Respon AI tidak bisa diproses: {parse_err}"
        except Exception as e:
            bot_reply = f"Terjadi error tak terduga: {e}"

    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
