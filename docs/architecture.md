# Architecture

VeriTrace is a React/Vite single-page application calling a FastAPI JSON API. TanStack Query owns server state and Zustand holds the active review selection. No secret is shipped to the browser.

FastAPI routes validate transport data and delegate extraction, chunking, retrieval, verification, and evidence location to focused services. SQLAlchemy models persist documents, page text, chunks, claims, and traces. SQLite is the local default; the same ORM uses Supabase PostgreSQL through `DATABASE_URL` in deployment.

The LLM boundary is `LLMProvider`. `GeminiProvider` uses the official Google Gen AI SDK; `MockProvider` accepts only built-in samples. Retrieval combines TF-IDF, fuzzy matching, keywords and numeric overlap. Model JSON is Pydantic-validated, deterministic fact checks can override semantic support, and an exact page quote must be located before evidence is highlighted.

Failures become stable `{error:{code,message,details}}` responses. Upload originals live only in generated temporary files and are removed in a `finally` block.

