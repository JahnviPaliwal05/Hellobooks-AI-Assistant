import os
from dotenv import load_dotenv
from graph import build_graph
from rag_pipeline import create_vector_store

load_dotenv()

if not os.path.exists("vectorstore"):
    create_vector_store()

graph = build_graph()

while True:

    question = input("\nAsk accounting question: ")

    if question == "exit":
        break

    result = graph.invoke({
        "question": question
    })

    print("\nAnswer:", result["answer"])