from fastapi import FastAPI
from app.routers import auth,student_router,master_router
from app.database import Base,engine

import app.models.user
import app.models.student
import app.models.jobseeker
import app.models.mentor
import app.models.employee
import app.models.master

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth with Factory + SOLID")

app.include_router(auth.router)
app.include_router(student_router.router)
app.include_router(master_router.router)

