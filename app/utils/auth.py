from fastapi import Request, HTTPException,Depends,status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2AuthorizationCodeBearer
from app import models,routers,schemas
from datetime import datetime,timedelta
from jose import jwt ,JWTError
from sqlalchemy.orm import Session
from app.dependencies import get_db_session

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(30)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_pass(password:str):
    return pwd_context.hash(password)


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def authenticate_user(email:str,password:str,db):
    user  = db.query(models.User).filter(models.User.email ==email).first()
    print(user)
 
    if not user:
        return False
    
    if not pwd_context.verify(password,user.hashed_password):
        return False
    
    return user
    

def get_access_token(email:str,user_id:int):
    encode = {'sub':email,"id":user_id}
    expires  = datetime.now() + ACCESS_TOKEN_EXPIRE_MINUTES
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm = ALGORITHM)







# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super(JWTBearer, self).__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
#         if credentials:
#             if not credentials.scheme == "Bearer":
#                 raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
#             if not self.verify_jwt(credentials.credentials):
#                 raise HTTPException(status_code=403, detail="Invalid token or expired token.")
#             return credentials.credentials
#         else:
#             raise HTTPException(status_code=403, detail="Invalid authorization code.")

#     def verify_jwt(self, jwtoken: str) -> bool:
#         isTokenValid: bool = False

#         try:
#             payload = jwt.decode(jwtoken)
#         except:
#             payload = None
#         if payload:
#             isTokenValid = True

#         return isTokenValid
    

def verify_token(token: str,credentials_exception:HTTPException):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_bearer),db: Session = Depends(get_db_session)):
  
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = verify_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user