from pydantic import BaseModel,constr,EmailStr,field_validator
from typing import Optional

class UserBase(BaseModel):
    first_name: str = constr(min_length=2, max_length=25, regex="^[A-Za-z]+$")
    last_name: str = constr(min_length=2, max_length=25, regex="^[A-Za-z]+$")
    email: EmailStr
    phone_no: str =  constr(regex="^\+\d{1,3}\d{4,14}(?:x.+)?$")
    profile_img = Optional[str] = None


class UserCreate(UserBase):
    password : str = constr(min_length=8, regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$")
    confirm_password : str

    @field_validator('password','confirm_password')
    def match_password(cls,password:str,confirm_password:str):
        if password != confirm_password:
            return ValueError('Password do not match')
        return password



