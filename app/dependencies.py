from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Annotated
import redis
def get_db_session(db: Session = Depends(get_db)):
    return db

r = redis.Redis(host='localhost', port=6379, db=0)

def get_redis():
    return r

