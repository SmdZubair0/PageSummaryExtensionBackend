# 📖 LangChain + FastAPI Backend

This project is a **LangChain-powered FastAPI backend** that supports:
- Loading and storing webpage data into **FAISS**.
- Summarizing stored content.
- Answering user queries using **retrieval-based QA** with session tracking.

---
##### These APIs can be accessed here : https://github.com/SmdZubair0
---

## 🚀 Features
- **/load** → Store webpage data (title, text, timestamp) into FAISS.
- **/summarize** → Summarize the stored content.
- **/query** → Retrieve relevant content from FAISS and answer questions.
- Session-based APIs using `session_id`.
- Configurable with environment variables.
- Built with **FastAPI**, **LangChain**, and **FAISS**.

---

## 📂 Project Structure
```bash
src/
├── api/                    # API routes
│   ├── __init__.py
│   ├── DataLoader.py       # Load page data into FAISS
│   ├── Query.py            # Answer queries from stored data
│   ├── TextSummarizer.py   # Summarize stored data
│
├── core/                   # Core settings and configs
│   ├── __init__.py
│   ├── config.py
│
├── models/                 # Request and Response models
│   ├── __init__.py
│   ├── request_models.py
│   ├── response_models.py
│
├── utils/                  # Helper functions
│   ├── __init__.py
│   ├── helpers.py
│   ├── HuggingFaceEmbedder.py
│   ├── StringLoader.py
│
├── resources/              # Extra resources (if any)
├── tests/                  # Unit tests
│
├── main.py                 # FastAPI routers entry point
├── app.py                  # Alternative app entry point
├── Dockerfile              # Containerization
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
├── .gitignore
├── .env.example            # Example environment variables
```

## ⚡ API Endpoints

---

### 🏠 Root
**GET /**  
**Response**
```json
{
  "status": "ok",
  "message": "Backend is running"
}
```

### 📥 Load Data

**POST /load?session_id=<session_id>**
**Request Body (PageData)**
```json
{
  "url": "https://example.com/article",
  "title": "Understanding Machine Learning",
  "text": "This article explains the basics of machine learning...",
  "timestamp": "2025-08-04T14:30:00Z"
}
```

**Response (DataloaderResponse)**
```json
{
  "status": "success",
  "timestamp": "2025-08-04T15:00:00Z",
  "chunks": 5
}
```

### 📝 Summarize Data

**POST /summarize?session_id=<session_id>**
**Response (TextSummarizerResponse)**
```json
{
  "status": "success",
  "summary": "This article discusses how AI is transforming modern education systems."
}
```

### 🔍 Query Data

**POST /query?session_id=<session_id>**
**Request Body (QueryModel)**
```json
{
  "query": "Summarize this article",
  "chat_history": [
    {"role": "user", "content": "Explain AI"},
    {"role": "assistant", "content": "AI stands for Artificial Intelligence..."}
  ],
  "timestamp": "2025-08-04T14:35:00Z"
}
```

**Response (QueryResponse)**
```json
{
  "status": "success",
  "result": "AI stands for Artificial Intelligence, which enables machines to mimic human intelligence.",
  "chat_history": [
    {"role": "user", "content": "What is AI?"},
    {"role": "assistant", "content": "AI stands for Artificial Intelligence..."
    }
  ]
}
```
---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/langchain-fastapi-backend.git
cd langchain-fastapi-backend
```

### 2️⃣ Create Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate venv
# On Linux / Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
```bash
Create a .env file in the project root with:

GROP_API_KEY=your_groq_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

### 5️⃣ Run the Server
```bash
uvicorn src.main:app --reload
```
