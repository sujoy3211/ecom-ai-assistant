import json
import os
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Setup ChromaDB - store inside services folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
client = PersistentClient(path=os.path.join(BASE_DIR, "chroma_db"))
collection = client.get_or_create_collection(name="products")

def load_products():
    data_path = os.path.join(BASE_DIR, "../../../data/products.json")
    with open(data_path, "r") as f:
        return json.load(f)

def build_vector_store():
    products = load_products()

    if collection.count() > 0:
        print("✅ Vector store already loaded!")
        return

    print("⏳ Building vector store...")

    for product in products:
        text = f"{product['name']}. {product['description']}. {product['specs']}. Price: {product['price']} rupees."
        embedding = embedding_model.encode(text).tolist()
        collection.add(
            ids=[product["id"]],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{
                "name": product["name"],
                "category": product["category"],
                "price": str(product["price"])
            }]
        )

    print(f"✅ {len(products)} products loaded into vector store!")

def search_products(query: str, top_k: int = 3):
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results