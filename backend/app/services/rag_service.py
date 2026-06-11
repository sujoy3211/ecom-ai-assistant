import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from serpapi import GoogleSearch

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def search_real_products(query: str):
    """Search real products from Google Shopping via SerpAPI"""
    try:
        params = {
            "engine": "google_shopping",
            "q": query,
            "api_key": os.getenv("SERPAPI_KEY"),
            "gl": "in",
            "hl": "en",
            "num": "6"
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        products = []
        for item in results.get("shopping_results", [])[:6]:
            products.append({
                "name": item.get("title", ""),
                "price": item.get("price", "N/A"),
                "source": item.get("source", ""),
                "link": item.get("link", ""),
                "thumbnail": item.get("thumbnail", ""),
                "rating": str(item.get("rating", "")),
                "reviews": str(item.get("reviews", "")),
                "category": "Product",
                "brand": item.get("source", "")
            })
        return products
    except Exception as e:
        print(f"SerpAPI error: {e}")
        return []

def get_ai_response(user_query: str) -> dict:

    # Step 1: Search real products from internet
    products = search_real_products(user_query)

    # Step 2: Build context
    context = ""
    for i, p in enumerate(products):
        context += f"\nProduct {i+1}: {p['name']}, Price: {p['price']}, Store: {p['source']}, Link: {p['link']}\n"

    # Step 3: Build prompt
    if products:
        prompt = f"""You are a helpful AI shopping assistant like ChatGPT.
Based on these real products found online, answer the customer's question helpfully.
Mention product names, prices, and where to buy them.
Be friendly, concise and helpful.

Real Products Found Online:
{context}

Customer Question: {user_query}

Answer:"""
    else:
        prompt = f"""You are a helpful AI shopping assistant.
Answer this shopping question helpfully with general advice since no specific products were found.
Suggest where the customer can search online (Amazon, Flipkart, Google Shopping).

Customer Question: {user_query}

Answer:"""

    # Step 4: Get Groq response
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content,
        "relevant_products": products
    }