from sqlalchemy import Column,String,Integer

from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(length=25), index=True)
    last_name = Column(String(length=25), index=True)
    email = Column(String(length=100), unique=True, index=True)
    hashed_password = Column(String(length=255))
    phone_no = Column(String(length=13))
    profile_picture = Column(String(length=100))