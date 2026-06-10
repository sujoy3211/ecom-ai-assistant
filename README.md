# 🛒 AI E-commerce Shopping Assistant

An intelligent shopping assistant powered by **Retrieval Augmented Generation (RAG)** that answers product questions using a vector database and LLM.

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 🧠 How It Works

User Question → React Frontend → FastAPI Backend → ChromaDB Vector Search → Groq LLaMA 3.3 → Answer

1. User asks a question about products
2. Question is converted to embeddings using sentence-transformers
3. ChromaDB finds the most relevant products
4. Groq LLaMA 3.3 generates a natural language answer
5. Response returned with matched product cards

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, Framer Motion |
| Backend | FastAPI, Python |
| Vector DB | ChromaDB |
| Embeddings | Sentence Transformers |
| LLM | Groq LLaMA 3.3 70B |

## ⚙️ Setup

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
Create a `.env` file inside the `backend` folder:
```
GROQ_API_KEY=your_key_here
```

## 🎯 Features

- ✅ Natural language product search
- ✅ RAG pipeline with vector similarity search
- ✅ Real-time AI responses
- ✅ Product cards with Flipkart search links
- ✅ Animated professional UI
- ✅ REST API with Swagger docs at /docs

## 📁 Project Structure

```
ecom-ai-assistant/
├── backend/
│   └── app/
│       ├── main.py
│       ├── routes/
│       └── services/
├── frontend/
│   └── src/
│       └── App.jsx
└── data/
    └── products.json
```

## 🙋 Author

**Sujoy** — [GitHub](https://github.com/sujoy3211)