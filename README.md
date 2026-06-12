# Multimodal AI Search Engine 

A full-stack semantic search engine that leverages OpenAI's CLIP model and vector database technology to find products based on conceptual meaning rather than exact keyword matches.

##  Overview

Traditional search engines rely on exact keyword matching, which often fails when users describe items conceptually. This project bridges that gap by implementing a decoupled client-server architecture that translates natural language queries into 512-dimensional vector embeddings, allowing for highly accurate semantic matching against a multimodal database.

### Key Features
* **Semantic Search:** Understands context and meaning (e.g., searching "rugged footwear for rain" successfully surfaces "waterproof leather boots").
* **AI Vector Embeddings:** Utilizes the HuggingFace `clip-ViT-B-32` model for real-time text-to-vector translation.
* **High-Performance Vector DB:** Powered by PostgreSQL and the `pgvector` extension via Supabase for efficient cosine similarity calculations.
* **Modern Interface:** A responsive, dark-mode user experience built natively with Next.js and standard CSS modules (Zero-Tailwind architecture).

## 🛠️ Tech Stack

**Frontend:**
* Next.js (App Router)
* React Hooks
* CSS Modules

**Backend:**
* Python
* FastAPI
* HuggingFace `sentence-transformers` (CLIP)
* Uvicorn

**Database:**
* Supabase (PostgreSQL)
* `pgvector` extension

##  Architecture

1. **Client Request:** The Next.js frontend sends a strictly typed JSON payload containing the user's natural language query to the Python backend.
2. **AI Processing:** FastAPI receives the request and utilizes the CLIP model to encode the text string into a 512-dimensional mathematical vector.
3. **Database Query:** The backend queries the Supabase vector database using a custom Remote Procedure Call (RPC) to perform a cosine similarity match against pre-ingested product vectors.
4. **Response:** The closest semantic matches are returned and dynamically rendered on the frontend UI.

---
