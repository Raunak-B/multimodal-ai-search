from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client

# 1. Initialize API and Model
app = FastAPI(title="Multimodal Search API")
print("Loading CLIP Model...")
model = SentenceTransformer('clip-ViT-B-32')

# 2. Initialize Supabase
SUPABASE_URL = "https://fdgibcafoqzmqdvrgpcp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZkZ2liY2Fmb3F6bXFkdnJncGNwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA4MTI5NjMsImV4cCI6MjA5NjM4ODk2M30.x2VPoVdi9mXrA45WsE0fU9rPJSd6FcbgkrY8kprEn3M"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 3. Setup CORS so your Next.js frontend (running on port 3000) is allowed to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Define the data structure we expect from the frontend
class TextSearchRequest(BaseModel):
    query: str

# 5. Create the Text Search Endpoint
@app.post("/search/text")
def search_by_text(request: TextSearchRequest):
    try:
        # Convert the user's text search into a 512-dimensional vector
        query_embedding = model.encode(request.query).tolist()
        
        # Call the Postgres function we created earlier
        response = supabase.rpc('match_products', {
            'query_embedding': query_embedding,
            'match_threshold': 0.2, # Lowered threshold to ensure we get results from a small test catalog
            'match_count': 5
        }).execute()
        
        return {"status": "success", "results": response.data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Multimodal Search API is running!"}