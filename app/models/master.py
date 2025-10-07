from sqlalchemy import Column, Integer, String
from app.database import Base

class MasterCourse(Base):
    __tablename__ = "master_courses"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(String, unique=True, nullable=False)
    course_name = Column(String, nullable=False)

class MasterProject(Base):
    __tablename__ = "master_projects"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, unique=True, nullable=False)
    project_name = Column(String, nullable=False)
