import streamlit as st
import requests

# ---------------- KONFIGURASI API ----------------
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
MODEL = "openai/gpt-3.5-turbo"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "X-Title": "AI Chatbot Streamlit"
}

# ---------------- PAGE TITLE ----------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Layout wrapper
st.markdown('<div id="main-container">', unsafe_allow_html=True)

st.title("🤖 AI Chatbot")
st.markdown("Powered by [Mistral AI](https://mistral.ai/) & OpenRouter")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- STYLING ----------------
st.markdown("""
    <style>
    html, body, [data-testid="stApp"] {
        height: 100%;
        margin: 0;
        padding: 0;
        background-color: #ffe6f0; /* Baby pink background */
    }

    #main-container {
        display: flex;
        flex-direction: column;
        height: 100vh;
        justify-content: space-between;
        padding: 1rem;
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
        background-color: #ff99cc; /* PINK for user */
        color: white;
        margin-left: auto;
    }

    .bot-message {
        background-color: #f0f0f0; /* SOFT GREY for bot */
        color: black;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE INIT ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- INPUT DI LUAR COLUMNS ----------------
user_input = st.chat_input("Type your message here...")

# ---------------- DISPLAY CHAT ----------------
for chat in st.session_state.chat_history:
    role = chat["role"]
    message = chat["content"]

    avatar = "💗" if role == "user" else "🤖"
    role_class = "bot-message" if role == "assistant" else "user-message"
    container_class = "message-container user-container" if role == "user" else "message-container"

    st.markdown(f"""
        <div class="{container_class}">
            <div class="avatar">{avatar}</div>
            <div>
                <div style="font-size: 0.75rem; color: gray; margin-bottom: 0.2rem;">{"You" if role == "user" else "Bot"}</div>
                <div class="chat-message {role_class}">{message}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ---------------- ACTION BUTTONS ----------------
chat_col, btn_col1, btn_col2 = st.columns([8, 1, 1])

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
    # Simpan input user ke riwayat
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        payload = {
            "model": MODEL,
            "messages": [{"role": "system", "content": "You are a helpful assistant."}] + st.session_state.chat_history
        }

        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=15)
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

    # Simpan balasan bot
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
