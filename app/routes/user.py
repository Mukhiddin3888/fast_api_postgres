
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, utils
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List

router = APIRouter(
    prefix= '/users',
    tags=['Users']
)

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user( user: schemas.UserCreate ,db: Session = Depends(get_db)):
    
   # hash user's password
   user.password = utils.hashPassword(password=user.password)
    
   new_user = models.User(**user.dict() )
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return new_user 


@router.get("/", response_model= List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    
    users = db.query(models.User).all()
  
    return users


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} not found")
    
    return user