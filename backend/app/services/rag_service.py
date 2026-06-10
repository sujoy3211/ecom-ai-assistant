import os
from dotenv import load_dotenv
from groq import Groq
from .vector_store import search_products, build_vector_store

# Load .env - look in multiple possible locations
load_dotenv()  # tries current directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))  # backend folder
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'backend', '.env'))  # absolute fallback

# Configure Groq
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Build vector store on startup
build_vector_store()

def get_ai_response(user_query: str) -> dict:

    # Step 1: Search relevant products
    results = search_products(user_query, top_k=3)

    # Step 2: Build context
    context = ""
    products_found = []

    for i, (doc, metadata) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        context += f"\nProduct {i+1}: {doc}\n"
        products_found.append({
            "name": metadata["name"],
            "category": metadata["category"],
            "price": f"₹{metadata['price']}"
        })

    # Step 3: Build prompt
    prompt = f"""You are a helpful e-commerce shopping assistant.
Answer the customer's question ONLY based on the products listed below.
If the answer is not in the products, say "I don't have that product available."
Be friendly, concise, and helpful.

Available Products:
{context}

Customer Question: {user_query}

Answer:"""

    # Step 4: Get Groq response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "answer": response.choices[0].message.content,
        "relevant_products": products_found
    }