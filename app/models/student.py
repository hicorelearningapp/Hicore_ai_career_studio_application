from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # link to User
    name = Column(String, nullable=False)
    college = Column(String, nullable=True)

    user = relationship("User", back_populates="student_profile")
    # Courses/Projects relationships
    courses = relationship("Course", back_populates="student", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="student", cascade="all, delete-orphan")


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(String, nullable=False)
    course_name = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="courses")


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, nullable=False)
    project_name = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="projects")
