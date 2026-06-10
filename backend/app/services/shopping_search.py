import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

def search_shopping(query: str):
    """Search real products from Google Shopping"""
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": os.getenv("SERPAPI_KEY"),
        "gl": "in",
        "hl": "en",
        "num": 5
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    products = []
    for item in results.get("shopping_results", [])[:5]:
        products.append({
            "name": item.get("title", ""),
            "price": item.get("price", "N/A"),
            "source": item.get("source", ""),
            "link": item.get("link", ""),
            "thumbnail": item.get("thumbnail", ""),
            "rating": item.get("rating", ""),
            "reviews": item.get("reviews", "")
        })

    return products