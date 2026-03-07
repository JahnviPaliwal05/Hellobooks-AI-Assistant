# Hellobooks AI Assistant

An AI-powered accounting assistant built using RAG (Retrieval Augmented Generation), Streamlit UI, and Groq LLM.

The assistant answers accounting-related questions using company knowledge documents.

---

## Features

* Retrieval Augmented Generation (RAG)
* Vector database search
* Fast inference using Groq LLM
* Interactive Streamlit interface
* Docker support for easy deployment

---

## Tech Stack

* Python
* Streamlit
* LangChain
* LangGraph
* Groq API
* HuggingFace Embeddings
* FAISS Vector Database
* Docker

---



---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repository-link>
cd hellobooks-ai-assistant
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Add Environment Variables

Create `.env` file:

```
GROQ_API_KEY=your_groq_api_key
```

---

### 5. Run Application

```bash
streamlit run ui/streamlit_app.py
```

Open in browser:

http://localhost:8501

---

## Running with Docker

### Build Docker Image

```bash
docker build -t hellobooks-ai .
```

### Run Container

```bash
docker run -p 8501:8501 --env-file .env hellobooks-ai
```

Open in browser:

http://localhost:8501

---

## Example Questions

* What is GST?
* How do invoices work?
* What is a balance sheet?
* How does bookkeeping work?

---

## Author

AI Assistant project for Hellobooks internship task.
