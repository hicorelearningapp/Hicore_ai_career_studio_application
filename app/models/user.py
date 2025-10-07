from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database import Base

class RoleEnum(str, Enum):
    student = "student"
    jobseeker = "jobseeker"
    mentor = "mentor"
    employee = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(SqlEnum(RoleEnum), nullable=False)
    provider = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    phone = Column(String, unique=True, nullable=True)

    # one-to-one relationships
    student_profile = relationship("Student", back_populates="user", uselist=False)
    jobseeker_profile = relationship("JobSeeker", back_populates="user", uselist=False)
    mentor_profile = relationship("Mentor", back_populates="user", uselist=False)
    employee_profile = relationship("Employee", back_populates="user", uselist=False)
