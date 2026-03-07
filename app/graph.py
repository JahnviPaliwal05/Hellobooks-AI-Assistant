from typing import TypedDict
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from groq import Client

from app.rag_pipeline import load_vector_store

load_dotenv()

# -----------------------------
# Groq setup
# -----------------------------

client = Client(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"   # free compatible
MAX_TOKENS = 512                # response limit
MAX_PROMPT_CHARS = 2000         # prompt safety


# -----------------------------
# Graph state
# -----------------------------

class GraphState(TypedDict):
    question: str
    context: str
    answer: str


# -----------------------------
# Vector DB
# -----------------------------

vector_db = load_vector_store()


# -----------------------------
# Retrieve documents
# -----------------------------

def retrieve(state: GraphState):

    question = state["question"].strip()

    if not question:
        return {"context": "", "answer": "Please ask a valid question."}

    if vector_db is None:
        return {"context": "", "answer": "Vector database not loaded."}

    docs = vector_db.similarity_search(question, k=3)

    context = "\n".join([doc.page_content for doc in docs])

    return {
        "question": question,
        "context": context
    }


# -----------------------------
# Generate answer using Groq
# -----------------------------

def generate(state: GraphState):

    question = state["question"]
    context = state["context"]

    prompt = f"""
You are an AI accounting assistant for Hellobooks.

Use the provided context to answer the question.

Context:
{context}

Question:
{question}

Provide a clear and helpful answer.
"""

    # protect free API usage
    if len(prompt) > MAX_PROMPT_CHARS:
        prompt = prompt[:MAX_PROMPT_CHARS] + "\n[context truncated]"

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=MAX_TOKENS
        )

        answer = response.choices[0].message.content

    except Exception as e:

        answer = f"Error generating response: {str(e)}"

    return {"answer": answer}


# -----------------------------
# Build LangGraph workflow
# -----------------------------

def build_graph():

    workflow = StateGraph(GraphState)

    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)

    workflow.set_entry_point("retrieve")

    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()