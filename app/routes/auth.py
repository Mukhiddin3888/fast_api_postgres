

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List

router = APIRouter(
    prefix= '/login',
    tags=['Auth']
)

@router.post("/",  response_model=schemas.Token)
def login_user( user: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    
    n_user = db.query(models.User).filter(models.User.email == user.username).first()
   
    if not user:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Bad Credentialls")
   
    v_email = utils.verifyPassword(user.password, n_user.password ) 
   
    if not v_email:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Bad Credentialls")
   
    access_token = oauth2.create_access_token(data={"user_id": n_user.id})
    
    return {"access_token" : access_token, "token_type": "bearer"} 
