from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class JobSeeker(Base):
    __tablename__ = "jobseekers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skills = Column(String, nullable=True)
    experience = Column(String, nullable=True)

    user = relationship("User", back_populates="jobseeker_profile")
