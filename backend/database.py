from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase 
engine = create_engine("sqlite:///../database.db")
class Base(DeclarativeBase):
    pass
Sessionlocal = sessionmaker(bind=engine)