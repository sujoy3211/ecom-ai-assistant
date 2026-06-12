import os
from dotenv import load_dotenv
from groq import Groq
from serpapi import GoogleSearch

# Load env from backend folder
load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def search_real_products(query: str):
    api_key = os.getenv("SERPAPI_KEY")
    print(f"SERPAPI KEY loaded: {api_key[:10] if api_key else 'NONE'}")
    try:
        params = {
            "engine": "google_shopping",
            "q": query,
            "api_key": api_key,
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
        print(f"Products found: {len(products)}")
        return products
    except Exception as e:
        print(f"SerpAPI error: {e}")
        return []

def get_ai_response(user_query: str) -> dict:
    products = search_real_products(user_query)

    context = ""
    for i, p in enumerate(products):
        context += f"\nProduct {i+1}: {p['name']}, Price: {p['price']}, Store: {p['source']}\n"

    if products:
        prompt = f"""You are a helpful AI shopping assistant.
Based on these real products found online, answer the customer's question.
Mention product names and prices. Be friendly and concise.

Real Products Found:
{context}

Customer Question: {user_query}

Answer:"""
    else:
        prompt = f"""You are a helpful AI shopping assistant.
Answer this shopping question helpfully.

Customer Question: {user_query}

Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content,
        "relevant_products": products
    }