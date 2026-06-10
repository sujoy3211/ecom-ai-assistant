import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from .shopping_search import search_shopping

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(user_query: str) -> dict:

    # Step 1: Search real products from internet
    products = search_shopping(user_query)

    # Step 2: Build context from real products
    context = ""
    for i, p in enumerate(products):
        context += f"\nProduct {i+1}: {p['name']}, Price: {p['price']}, Store: {p['source']}\n"

    # Step 3: Build prompt
    prompt = f"""You are a helpful shopping assistant.
Based on the real products found online below, answer the customer's question.
Be friendly, helpful and recommend the best option with reasons.
mention prices and where to buy.

Real Products Found:
{context}

Customer Question: {user_query}

Answer:"""

    # Step 4: Get Groq response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content,
        "relevant_products": products
    }