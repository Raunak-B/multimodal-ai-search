import os
from PIL import Image
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client

# 1. Initialize your Supabase Client
# Replace these strings with your actual project credentials from your Supabase Dashboard settings
SUPABASE_URL = "https://fdgibcafoqzmqdvrgpcp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZkZ2liY2Fmb3F6bXFkdnJncGNwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA4MTI5NjMsImV4cCI6MjA5NjM4ODk2M30.x2VPoVdi9mXrA45WsE0fU9rPJSd6FcbgkrY8kprEn3M"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Load the CLIP Model locally into memory
# This automatically downloads the 512-dimensional 'ViT-B/32' model weights on the first run
print("Loading CLIP model... This may take a minute on the first run.")
model = SentenceTransformer('clip-ViT-B-32')

# 3. Define a sample catalog of products to push to your database
# For your local testing, ensure these image files actually exist in your folder paths!
mock_products = [
    {
        "name": "Classic Leather Boot",
        "description": "Premium waterproof dark brown leather boots designed for rugged outdoor use.",
        "image_path": "images/leather_boot.jpg", # Ensure this file exists locally
        "image_url": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?q=80&w=600&auto=format&fit=crop", # Public URL for frontend rendering
        "price": 129.99,
        "category": "Footwear"
    },
    {
        "name": "White Minimalist Sneaker",
        "description": "Clean, breathable white canvas sneakers perfect for casual summer wear.",
        "image_path": "images/white_sneaker.jpg",
        "image_url": "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?q=80&w=600&auto=format&fit=crop",
        "price": 79.50,
        "category": "Footwear"
    }
]

def ingest_catalog():
    for idx, product in enumerate(mock_products):
        print(f"Processing item {idx+1}/{len(mock_products)}: {product['name']}...")
        
        try:
            # Open the image file using Pillow
            img = Image.open(product["image_path"])
            
            # Generate the mathematical 512-dimensional vector embedding for this specific image
            # We convert the resulting numpy array into a standard Python list so Postgres can parse it
            image_embedding = model.encode(img).tolist()
            
            # Prepare the final payload payload for Postgres
            db_payload = {
                "name": product["name"],
                "description": product["description"],
                "image_url": product["image_url"],
                "price": product["price"],
                "category": product["category"],
                "embedding": image_embedding # The 512-float vector list goes here
            }
            
            # Push the data to your Supabase 'products' table
            response = supabase.table("products").insert(db_payload).execute()
            print(f"Successfully uploaded: {product['name']}")
            
        except Exception as e:
            print(f"Failed to process {product['name']}. Error: {str(e)}")

if __name__ == "__main__":
    ingest_catalog()