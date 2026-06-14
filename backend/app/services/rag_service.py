import os
import re
from dotenv import load_dotenv
from groq import Groq
from serpapi import GoogleSearch

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_store_link(source, product_name):
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
    valid = [p for p in products if p["price_value"] > 0]
    if not valid:
        return None
    return min(valid, key=lambda x: x["price_value"])

def compare_products(user_query: str) -> dict:
    vs_pattern = re.split(r'\s+vs\.?\s+|\s+versus\s+|\s+and\s+', user_query, flags=re.IGNORECASE)
    products_to_compare = []
    for p in vs_pattern:
        clean = re.sub(r'compare|which is better|difference between', '', p, flags=re.IGNORECASE).strip()
        if clean:
            products_to_compare.append(clean)

    if len(products_to_compare) < 2:
        return None

    all_products = {}
    for product_name in products_to_compare[:3]:
        results = search_real_products(product_name)
        if results:
            best = get_best_deal(results)
            all_products[product_name] = {
                "best_price": best["price"] if best else "N/A",
                "best_store": best["source"] if best else "N/A",
                "best_link": best["link"] if best else "",
                "rating": best["rating"] if best else "N/A",
                "thumbnail": best["thumbnail"] if best else "",
                "all_results": results[:3]
            }

    if len(all_products) < 2:
        return None

    context = ""
    for name, data in all_products.items():
        context += f"\n{name}:\n"
        context += f"  Best Price: {data['best_price']} at {data['best_store']}\n"
        context += f"  Rating: {data['rating']}\n"

    prompt = f"""You are an expert product comparison AI assistant.
Compare these products in detail:

{context}

Provide a structured comparison with:
1. Price Comparison Table
2. Rating Comparison
3. Category Winners:
   - Best Camera
   - Best Battery
   - Best Performance
   - Best Value for Money
4. Overall Winner with reason
5. Who should buy which product

User Query: {user_query}

Be specific, helpful and use emojis. Keep it concise."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    comparison_products = []
    for name, data in all_products.items():
        if data["all_results"]:
            best = data["all_results"][0]
            best["is_best_deal"] = False
            comparison_products.append(best)

    return {
        "answer": response.choices[0].message.content,
        "relevant_products": comparison_products,
        "best_deal": None,
        "is_comparison": True
    }

def get_ai_response(user_query: str, history: list = []) -> dict:
    # Detect comparison query
    comparison_keywords = ["vs", "versus", "compare", "difference between", "which is better", "which one"]
    is_comparison = any(kw in user_query.lower() for kw in comparison_keywords)

    if is_comparison:
        result = compare_products(user_query)
        if result:
            return result

    # Detect follow-up queries (not a product search)
    followup_keywords = ["more detail", "explain", "tell me more", "elaborate", "what about", 
                        "why", "how", "which one should", "recommend", "suggest", "difference",
                        "better", "worse", "pros", "cons", "advantage", "disadvantage"]
    is_followup = any(kw in user_query.lower() for kw in followup_keywords) and len(history) > 0

    products = []
    context = ""

    if not is_followup:
        # Search products only for new queries
        products = search_real_products(user_query)
        for i, p in enumerate(products):
            context += f"\nProduct {i+1}: {p['name']}, Price: {p['price']}, Store: {p['source']}, Rating: {p['rating']}\n"

    # Build conversation history for Groq
    messages = [
        {
            "role": "system",
            "content": """You are a smart AI shopping assistant like ChatGPT that helps users in India save money.
You remember the conversation context and give detailed, helpful answers.
When asked for more details, elaborate on the previous answer.
Always be helpful, use emojis, and provide actionable advice."""
        }
    ]

    # Add conversation history
    for msg in history[-6:]:  # last 6 messages for context
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    # Build current message
    if context:
        current_message = f"""Based on these real products found online:
{context}

User Question: {user_query}

Provide:
1. Direct answer to the question
2. Price comparison if relevant
3. Best deal recommendation
4. Deal score out of 10
Use emojis and be concise but helpful."""
    else:
        current_message = user_query

    messages.append({"role": "user", "content": current_message})

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    best_deal = get_best_deal(products) if products else None

    sorted_products = sorted(
        [p for p in products if p["price_value"] > 0],
        key=lambda x: x["price_value"]
    ) + [p for p in products if p["price_value"] == 0]

    for p in sorted_products:
        p["is_best_deal"] = (best_deal and p["source"] == best_deal["source"] and p["price"] == best_deal["price"])

    return {
        "answer": response.choices[0].message.content,
        "relevant_products": sorted_products[:6],
        "best_deal": best_deal
    }