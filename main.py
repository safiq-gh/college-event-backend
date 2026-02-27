from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import event, register

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event.router, prefix="/api")
app.include_router(register.router, prefix="/api")