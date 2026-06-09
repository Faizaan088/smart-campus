from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    complaints = relationship("Complaint",back_populates="user")
class Complaint(Base):
    __tablename__="complaints"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    description=Column(String)
    status=Column(String)
    category=Column(String)
    priority=Column(String)
    user_id=Column(Integer,ForeignKey("users.id"))
    created_at=Column(String)
    user = relationship("User",back_populates="complaints")