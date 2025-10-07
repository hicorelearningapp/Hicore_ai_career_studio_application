from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.master import MasterCourse, MasterProject
from pydantic import BaseModel

router = APIRouter(prefix="/master", tags=["Master Data"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schemas
class MasterCourseCreate(BaseModel):
    course_id: str
    course_name: str

class MasterProjectCreate(BaseModel):
    project_id: str
    project_name: str

# Add a master course
@router.post("/courses")
def add_master_course(course: MasterCourseCreate, db: Session = Depends(get_db)):
    existing = db.query(MasterCourse).filter(MasterCourse.course_id == course.course_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course ID already exists")
    db_course = MasterCourse(course_id=course.course_id, course_name=course.course_name)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return {"course_id": db_course.course_id, "course_name": db_course.course_name}

# Add a master project
@router.post("/projects")
def add_master_project(project: MasterProjectCreate, db: Session = Depends(get_db)):
    existing = db.query(MasterProject).filter(MasterProject.project_id == project.project_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Project ID already exists")
    db_project = MasterProject(project_id=project.project_id, project_name=project.project_name)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return {"project_id": db_project.project_id, "project_name": db_project.project_name}

# List all master courses
@router.get("/courses")
def list_master_courses(db: Session = Depends(get_db)):
    courses = db.query(MasterCourse).all()
    return [{"course_id": c.course_id, "course_name": c.course_name} for c in courses]

# List all master projects
@router.get("/projects")
def list_master_projects(db: Session = Depends(get_db)):
    projects = db.query(MasterProject).all()
    return [{"project_id": p.project_id, "project_name": p.project_name} for p in projects]
