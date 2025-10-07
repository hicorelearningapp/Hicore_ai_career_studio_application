from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    college: str = None

class CourseCreate(BaseModel):
    course_id: str

class ProjectCreate(BaseModel):
    project_id: str
