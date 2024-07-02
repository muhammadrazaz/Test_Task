from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Annotated

def get_db_session(db: Session = Depends(get_db)):
    return db

