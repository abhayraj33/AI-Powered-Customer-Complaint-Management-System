"""
Ye poore backend ka entry point hai. Isko run karke server start hoga.
Command: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import complaints
from app.db.session import init_db

app = FastAPI(title="Pharma Complaint Management System")


@app.on_event("startup")
def on_startup():
    # Server start hote hi database tables automatically ban jayengi (agar nahi hain to)
    init_db()

# CORS - taaki React frontend (jo alag port pe chalega) is backend ko call kar sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React ke common ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Complaint routes register karo
app.include_router(complaints.router)


@app.get("/")
def health_check():
    return {"status": "Server is running", "message": "Pharma Complaint Management System API"}