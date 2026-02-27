# College Event Registration — Backend

FastAPI + Supabase backend for the college event registration website.

---

## Tech Stack
- Python + FastAPI
- Supabase (PostgreSQL)
- Deployed on Railway

---

## Local Setup

1. **Clone the repo**
```bash
git clone https://github.com/yourname/college-event-backend.git
cd college-event-backend
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

5. **Run the server**
```bash
uvicorn main:app --reload
```

Server runs at `http://localhost:8000`  
API docs at `http://localhost:8000/docs`

---

## Project Structure
```
backend/
├── main.py          # App entry point, CORS config
├── database.py      # Supabase client
├── models.py        # Pydantic request schemas
├── routes/
│   ├── event.py     # GET /event
│   └── register.py  # POST /register, GET /register/:id
├── .env             # Secret keys (never commit this)
├── .gitignore
└── requirements.txt
```

---

## API Reference

| Method | Endpoint                  | Description                  |
|--------|---------------------------|------------------------------|
| GET    | /api/event                | Get event details and QR     |
| GET    | /api/register/check?email=| Check if email is registered |
| POST   | /api/register             | Submit registration          |
| GET    | /api/register/:id         | Check registration status    |

For full API details see `API_CONTRACT.md`

---

## Deployment

Deployed on Railway. Pushes to `main` auto-deploy.
