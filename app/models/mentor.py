from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Mentor(Base):
    __tablename__ = "mentors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    expertise = Column(String, nullable=True)
    bio = Column(String, nullable=True)

    user = relationship("User", back_populates="mentor_profile")
