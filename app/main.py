from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, student_router, master_router
from app.database import Base, engine
from app.routers import profile_routes

import app.models.user
import app.models.student
import app.models.jobseeker
import app.models.mentor
import app.models.employee
import app.models.master



# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth with Factory + SOLID")

# Allow all origins (for testing or open API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(student_router.router)
app.include_router(master_router.router)
app.include_router(profile_routes.router)
