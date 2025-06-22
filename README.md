# 🤖 AI Chatbot - Streamlit + OpenRouter

A lightweight and interactive AI chatbot built using **Streamlit** and powered by **OpenRouter** (OpenAI/Mistral). This app provides a clean chat interface, styled chat bubbles, and features like **clear chat**, **download history**, and beautiful emoji-based avatars.

---

## 🚀 Features

- 🧠 Conversational AI via OpenRouter (supports OpenAI GPT-3.5, Mistral, etc.)
- 💬 Bubble-style chat UI with avatars (🤖 for AI, 👤 for user)
- 🎨 Custom styling using Inter font and CSS
- 🧹 Clear chat history button
- 📥 Download chat transcript (TXT)
- 📱 Mobile-friendly and responsive layout
- ✅ Error handling for failed API requests

---

## 📷 Screenshot
![image](https://github.com/user-attachments/assets/3bbb5a39-7ee2-4ca3-810a-5f2194d1fec2)

---

## 🛠️ Installation

1. **Clone this repo:**
   ```bash
   git clone https://github.com/your-username/streamlit-ai-chatbot.git
   cd streamlit-ai-chatbot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## 🔐 Setup
Make sure to create your OPENROUTER_API_KEY. You can get it from:
👉 https://openrouter.ai/
Then, add your API key in app.py:
```python
OPENROUTER_API_KEY = "sk-or-v1-..."  # replace with your actual key
```

## 📁 File Structure
```bash
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🧪 Example Models
You can experiment by switching the model inside the MODEL variable in app.py:
```python
MODEL = "openai/gpt-3.5-turbo"
# or
MODEL = "mistralai/mistral-7b-instruct"
```

---

📄 License
This project is open-source and free to use under the MIT License.

---

🙌 Credits
Built with Streamlit
Powered by OpenRouter

---

### 📌 Jangan Lupa
- Ganti `OPENROUTER_API_KEY`, URL repo, dan screenshot kalau ada.
- Tambahkan file `requirements.txt` berisi:
  ```txt
  streamlit
  requests
  ```
