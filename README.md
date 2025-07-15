#  🤖 Smart Web Assistant

This is a full-stack AI assistant that lets you summarize any webpage and then chat with an LLM about the contents — all from a handy Chrome Extension.

Built using:
- **FastAPI** + **LangChain** + **Hugging Face** on the backend
- **Chrome Extension** (with Readability.js) on the frontend
- Optional fallback to **SerpAPI** for better answers

---

## 📁 Project Structure

```
langchain-chatbot/
│
├── backend/                  # FastAPI + LangChain backend
│   ├── main.py               # FastAPI app
│   ├── chatbot.py            # Core LLM + summarization logic
│   ├── schema.py             # Pydantic request model
│   └── .env                  # Environment variables
│
├── extension/                # Chrome Extension UI
│   ├── manifest.json         # Chrome extension config
│   ├── popup.html            # Popup UI
│   ├── popup.css             # Popup styling
│   ├── popup.js              # Sends data to the backend
│   ├── content.js            # Injected into web pages
│   └── Readability.js        # Extracts main content from page
│
├── requirements.txt          # Python dependencies
└── README.md                 # You're here
```

---

## 🧪 Features

✅ Summarize any article or webpage  
✅ Ask questions about what you're reading  
✅ Automatic fallback to web search if the answer isn't in the text  
✅ Lightweight, fast, and easy to deploy  

---

## 🚀 Setup Instructions

### 🔧 Backend (FastAPI + LangChain)

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/langchain-chatbot
cd langchain-chatbot/backend
```

2. **Create a virtual environment**

```bash
python -m venv .venv
source .venv/Scripts/activate    # Windows
# or
source .venv/bin/activate        # Mac/Linux
```

3. **Install dependencies**

```bash
pip install -r ../requirements.txt
```

4. **Set your environment variables**

Create a `.env` file in the `backend/` folder:

```
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token
SERPAPI_API_KEY=your_serpapi_key  # optional, for fallback search
```

5. **Run the backend**

```bash
uvicorn main:app --reload
```

The backend will be live at: `http://localhost:8000`

---

### 🌐 Frontend (Chrome Extension)

1. Open Google Chrome  
2. Go to `chrome://extensions/`  
3. Enable **Developer mode** (top-right toggle)  
4. Click **"Load unpacked"**  
5. Select the `extension/` folder from this repo  

Now you should see your extension in the Chrome toolbar!

---

### 🧠 How It Works (Flow)

1. You visit any webpage and click the extension.
2. It extracts the content using `Readability.js`.
3. Sends it to your FastAPI server (`/summary-chat`).
4. The backend summarizes the page and answers your question.
5. You get a chat-like response in the popup.

---

## 🧰 API Endpoint

### `POST /summary-chat`

**Request Body:**
```json
{
  "content": "Full text of the webpage...",
  "question": "What is the main takeaway?"
}
```

**Response:**
```json
{
  "summary": "This article is about...",
  "response": "The main takeaway is...",
  "source": "model" | "search" | "welcome"
}
```

---

## 🔍 Fallback Search

If the LLM can't answer (uncertain phrases like *"not mentioned"* or *"I don't know"*), the backend automatically uses SerpAPI to search the web and tries again with that context.

Set this up by adding your `SERPAPI_API_KEY` in `.env`.

---

## ✅ TODO / Ideas

- [ ] Add support for multiple users or sessions
- [ ] Deploy backend to Render, Hugging Face, or Fly.io
- [ ] Add history panel to the Chrome extension
- [ ] Support multiple LLMs (OpenAI, Mistral, Claude)

---

## 🧑‍💻 Author Notes

This was built as a personal project to speed up reading and make research more interactive. Great for summarizing blogs, tutorials, research papers, or even legal documents.

If you find this helpful or want to contribute, feel free to fork or open issues!

---

## 📄 License

MIT – Use it, remix it, improve it ✨
