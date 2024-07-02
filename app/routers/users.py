from fastapi import APIRouter, Depends, HTTPException,File,UploadFile,Form
from sqlalchemy.orm import Session
# from app import crud, schemas
from app import schemas,crud,utils,models
from app.dependencies import get_db_session
from starlette import status
from typing import Optional


router = APIRouter()



@router.post("/auth/register/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate = Depends(), db: Session = Depends(get_db_session)):
    # if profile_picture:
    #     utils.validate_image(profile_picture)
    
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.post("/auth/token",response_model=schemas.Token)
async def get_token(username:str = Form(...),password:str=Form(...),db:Session = Depends(get_db_session)):
    
    user  = utils.authenticate_user(username,password,db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user")
    

    token =  utils.get_access_token(user.email,user.id)

    return {'access_token':token,'token_type':'bearer'}


@router.patch("/update-profile",response_model=schemas.UserResponse)
def update_user_profile(user_profile : schemas.UserUpdate ,db:Session = Depends(get_db_session),current_user:models.User = Depends(utils.get_current_user)):
   
    user = crud.update_profile(db=db, user=current_user,user_profile=user_profile)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.patch("/update-profile-picture",response_model=schemas.UserResponse)
async def update_picture(profile_picture:UploadFile = File(...),db:Session = Depends(utils.get_db_session),current_user : models.User = Depends(utils.get_current_user) ):
    utils.validate_image(profile_picture)
    user = crud.update_profile_picture(db = db,profile_picture=profile_picture,user=current_user)
    return user

@router.patch("/update-password")
async def update_password(passwords : schemas.PasswordUpdate,db:Session = Depends(utils.get_db_session),current_user : models.User = Depends(utils.get_current_user)):
    user  = utils.authenticate_user(current_user.email,passwords.old_password,db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please enter correct old password")
    
    crud.update_password(password=passwords.password,user=current_user,db=db)

    return {"message":"password updated successfylly"}



@router.delete("/profile-picture", response_model=schemas.UserResponse)
def delete_profile_picture( db: Session = Depends(get_db_session),current_user:models.User = Depends(utils.get_current_user)):
    user = crud.delete_profile_picture(db, user_id=current_user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.delete("/phone-number", response_model=schemas.UserResponse)
def delete_phone_number( db: Session = Depends(get_db_session),current_user : models.User = Depends(utils.get_current_user)):
    user = crud.delete_phone_number(db, user_id=current_user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user



