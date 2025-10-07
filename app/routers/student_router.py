from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from managers.student_manager import StudentManager
from app.database import SessionLocal
from app.schemas.student_schema import StudentCreate, CourseCreate, ProjectCreate
from app.models.student import Student
router = APIRouter(prefix="/students", tags=["Students"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add course to student
@router.post("/{student_id}/courses")
def add_course(student_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    manager = StudentManager(db)
    try:
        return manager.add_course(student_id, course.course_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Add project to student
@router.post("/{student_id}/projects")
def add_project(student_id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    manager = StudentManager(db)
    try:
        return manager.add_project(student_id, project.project_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# List student courses
@router.get("/{student_id}/courses")
def list_courses(student_id: int, db: Session = Depends(get_db)):
    manager = StudentManager(db)
    return manager.list_courses(student_id)

# List student projects
@router.get("/{student_id}/projects")
def list_projects(student_id: int, db: Session = Depends(get_db)):
    manager = StudentManager(db)
    return manager.list_projects(student_id)
