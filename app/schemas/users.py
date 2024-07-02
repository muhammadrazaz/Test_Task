from pydantic import BaseModel,constr,EmailStr,field_validator,ValidationInfo,Field,StringConstraints
from typing import Optional
from typing_extensions import Annotated
import re




class UserBase(BaseModel):
    
    first_name:  Annotated[str,StringConstraints(min_length=2,max_length=25,strip_whitespace=True,to_upper=True)]
    last_name:  Annotated[str,StringConstraints(min_length=2,max_length=25,strip_whitespace=True,to_upper=True)]
   
    email: EmailStr
    phone_no: Annotated[str,StringConstraints(min_length=12,max_length=13)]
    

    @field_validator('first_name')
    def check_first_name(cls,first_name):
        name_regex = r'^[A-Za-z]+$'
        print('test') 
        if not re.fullmatch(name_regex,first_name):
            raise ValueError("first_name must string")
        
        return first_name
    
    @field_validator('last_name')
    def check_last_name(cls,last_name):
        name_regex = r'^[A-Za-z]+$'
        
        if not re.fullmatch(name_regex,last_name):
            raise ValueError("last name must be string")
        
        return last_name
        

        
    @field_validator('phone_no')
    def check_phone_no(cls,phone_no):
        phone_regex = r'^^\+\d{1,3}\d{4,14}(?:x.+)?$'
        
        if not re.fullmatch(phone_regex,phone_no):
            raise ValueError("Phone number must contain valid country code and number e.g +xxxxxxxxxxxx")
        return phone_no

class UserCreate(UserBase):
    password : str = constr(min_length=8,
                            #  pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$"
                             )
    confirm_password : str
    

    @field_validator('password')
    def match_password(cls,password:str,info: ValidationInfo):
        
        if 'confirem_password' in info.data and password != info.data['confirm_password']:
            raise ValueError('Password do not match')
        return password
    

class UserUpdate(UserBase):
    del UserBase.__annotations__['email']
    # del UserCreate.__annotations__['confirm_password']
    # pass


class PasswordUpdate(BaseModel):
    password : str = constr(min_length=8)
    confirm_password : str
    old_password : str 
    

    @field_validator('password')
    def match_password(cls,password:str,info: ValidationInfo):
        
        if 'confirem_password' in info.data and password != info.data['confirm_password']:
            raise ValueError('Password do not match')
        return password
   
    

class UserResponse(UserBase):
    id : int
    profile_picture : Optional[str] = None
    class Config:
        orm_mode = True
    
class UserLogin(BaseModel):
    email: EmailStr
    password : str

class Token(BaseModel):
    access_token :str
    token_type:str
    
    



