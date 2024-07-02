from fastapi import UploadFile
from sqlalchemy.orm import Session
from app import schemas,models,utils
import uuid,os


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):

    
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=utils.hash_pass(user.password), 
        phone_no=user.phone_no,
        
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    IMGDIR = 'profile_pictures'

    
    # if profile_picture:
        
    #     os.makedirs(IMGDIR, exist_ok=True)

       
    #     extension = os.path.splitext(profile_picture.filename)[1]  
    #     unique_filename = f"{uuid.uuid4()}{extension}"
    #     file_location = os.path.join(IMGDIR, unique_filename)
        
      
    #     with open(file_location, "wb") as file_object:
    #         file_object.write(profile_picture.file.read())
    #     db_user.profile_picture_url = file_location
    #     db.commit()
    #     db.refresh(db_user)

    return db_user


def update_password(password,user,db):
    

    user.hashed_password = utils.hash_pass(password)

    db.commit()
    db.refresh(user)


def update_profile(db,user_profile,user):
    # user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.first_name = user_profile.first_name
        user.last_name = user_profile.last_name
        user.phone_no = user_profile.phone_no
        

        db.commit()
        db.refresh(user)

    
        
    return user

    db.commit()
    db.refresh(user)

def update_profile_picture(profile_picture,db,user):
    IMGDIR = 'profile_pictures'
        
    os.makedirs(IMGDIR, exist_ok=True)

    
    extension = os.path.splitext(profile_picture.filename)[1]  
    if user.profile_picture:
        unique_filename = f"{user.profile_picture}{extension}"
    else:
        unique_filename = f"{uuid.uuid4()}{extension}"
    file_location = os.path.join(IMGDIR, unique_filename)
    
    
    with open(file_location, "wb") as file_object:
        file_object.write(profile_picture.file.read())
    if not user.profile_picture:
        user.profile_picture_url = file_location
        db.commit()
        db.refresh(user)
    return user


def delete_profile_picture(db: Session, user_id: int) :
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.profile_picture_url = None
        db.commit()
        db.refresh(user)
    return user

def delete_phone_number(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.phone_number = None
        db.commit()
        db.refresh(user)
    return user



