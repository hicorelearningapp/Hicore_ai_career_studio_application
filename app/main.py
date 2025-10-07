from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, student_router, master_router
from app.database import Base, engine

import app.models.user
import app.models.student
import app.models.jobseeker
import app.models.mentor
import app.models.employee
import app.models.master

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth with Factory + SOLID")

# ✅ Add CORS Middleware
origins = [
    "http://localhost:3000",      # your local React frontend
    "http://127.0.0.1:3000",
    "https://your-frontend-domain.com",  # your deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or use ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(student_router.router)
app.include_router(master_router.router)
