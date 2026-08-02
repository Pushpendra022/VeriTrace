# Deployment

## Gemini API key

Create or view an authorization key at [Google AI Studio](https://aistudio.google.com/apikey). Place it only in the repository-root `.env` as `GEMINI_API_KEY=...`; never put it in `frontend/.env` or a `VITE_` variable. New AI Studio keys are authorization keys restricted to Gemini by default. For production, add the same secret through Render's Environment page rather than committing it. The configured model remains controlled by `GEMINI_MODEL`.

## Supabase PostgreSQL

Create a Supabase project, open database connection settings, and copy the direct or session-pooler PostgreSQL URI. Convert the scheme to `postgresql+psycopg://` if necessary and retain `sslmode=require`. Set it only as Render's `DATABASE_URL`; never expose it to Vercel. From `backend`, run `alembic upgrade head` against that URL.

## Render backend

The root `render.yaml` Blueprint creates the Python service with repository root directory `backend`, build command `pip install -r requirements.txt`, and start command `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Configure the prompted `DATABASE_URL`, `FRONTEND_URL`, and `GEMINI_API_KEY` secrets. Health path is `/api/health`.

## Vercel frontend

Import the repository with root directory `frontend`, framework Vite, build command `npm run build`, and output `dist`. Set `VITE_API_BASE_URL=https://your-api.example/api`. Do not set Gemini or database secrets. `vercel.json` rewrites client-side routes to `index.html`.

Set backend `FRONTEND_URL` to the exact Vercel origin (comma-separated origins are supported). Wildcards are rejected in production. If health remains unavailable, check database SSL, migrations, allowed origin, and provider variables.
