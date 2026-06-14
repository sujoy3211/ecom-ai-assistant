import os
from dotenv import load_dotenv
from groq import Groq
from serpapi import GoogleSearch

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_store_link(source, product_name):
    """Build direct store search link based on source name"""
    q = product_name.replace(" ", "+")
    q_encoded = product_name.replace(" ", "%20")
    
    store_links = {
        "amazon": f"https://www.amazon.in/s?k={q}",
        "flipkart": f"https://www.flipkart.com/search?q={q}",
        "meesho": f"https://www.meesho.com/search?q={q}",
        "myntra": f"https://www.myntra.com/{q_encoded}",
        "snapdeal": f"https://www.snapdeal.com/search?keyword={q}",
        "croma": f"https://www.croma.com/searchB?q={q}",
        "reliance": f"https://www.reliancedigital.in/search?q={q}",
        "nykaa": f"https://www.nykaa.com/search/result/?q={q}",
        "tata": f"https://www.tatacliq.com/search/?text={q}",
        "ajio": f"https://www.ajio.com/search/?text={q}",
        "jiomart": f"https://www.jiomart.com/search/{q}",
        "shopsy": f"https://shopsy.in/search?q={q}",
        "cashify": f"https://www.cashify.in/search?q={q}",
        "vijay": f"https://www.vijaysales.com/search/{q}",
        "samsung": f"https://www.samsung.com/in/search/?searchvalue={q}",
        "apple": f"https://www.apple.com/in/search/{q}",
    }
    
    source_lower = source.lower()
    for key, url in store_links.items():
        if key in source_lower:
            return url
    
    return f"https://www.google.com/search?q={q}+buy+online+{source.replace(' ', '+')}"

def search_real_products(query: str):
    api_key = os.getenv("SERPAPI_KEY")
    try:
        params = {
            "engine": "google_shopping",
            "q": query,
            "api_key": api_key,
            "gl": "in",
            "hl": "en",
            "num": "10"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        products = []
        for item in results.get("shopping_results", [])[:10]:
            source = item.get("source", "")
            name = item.get("title", "")
            products.append({
                "name": name,
                "price": item.get("price", "N/A"),
                "price_value": float(str(item.get("extracted_price", 0))),
                "source": source,
                "link": get_store_link(source, name),
                "thumbnail": item.get("thumbnail", ""),
                "rating": str(item.get("rating", "")),
                "reviews": str(item.get("reviews", "")),
                "category": "Product",
                "brand": source
            })
        return products
    except Exception as e:
        print(f"SerpAPI error: {e}")
        return []
def get_best_deal(products):
    """Find the best deal from all products"""
    valid = [p for p in products if p["price_value"] > 0]
    if not valid:
        return None
    return min(valid, key=lambda x: x["price_value"])

def get_ai_response(user_query: str) -> dict:
    products = search_real_products(user_query)

    context = ""
    for i, p in enumerate(products):
        context += f"\nProduct {i+1}: {p['name']}, Price: {p['price']}, Store: {p['source']}, Rating: {p['rating']}\n"

    best_deal = get_best_deal(products)
    best_deal_text = ""
    if best_deal:
        best_deal_text = f"\nBest Deal Found: {best_deal['name']} at {best_deal['price']} on {best_deal['source']}"

    if products:
        prompt = f"""You are a smart AI shopping assistant that helps users save money in India.

Based on real products found online, provide:
1. Brief answer to the question
2. Price comparison across stores
3. Best deal recommendation with reason
4. Deal score out of 10
{best_deal_text}

Real Products Found:
{context}

Customer Question: {user_query}

Keep response concise and helpful. Use emojis."""
    else:
        prompt = f"""You are a helpful AI shopping assistant.
Answer this shopping question helpfully.
Customer Question: {user_query}
Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    # Sort products by price
    sorted_products = sorted(
        [p for p in products if p["price_value"] > 0],
        key=lambda x: x["price_value"]
    ) + [p for p in products if p["price_value"] == 0]

    # Add best deal flag
    for p in sorted_products:
        p["is_best_deal"] = (best_deal and p["source"] == best_deal["source"] and p["price"] == best_deal["price"])

    return {
        "answer": response.choices[0].message.content,
        "relevant_products": sorted_products[:6],
        "best_deal": best_deal
    }