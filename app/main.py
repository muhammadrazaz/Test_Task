from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal,engine,Base
from app.routers import users

Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()



app = FastAPI()




@app.get("/")
async def root(db:Session=Depends(get_db)):
    return {"message": "Hello World"}

app.include_router(users.router,prefix="/api")