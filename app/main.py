# Python version 3.11.5
# source "/Users/abbosbobomurodov/Desktop/python tutorial/freecodecampPython/venv/bin/activate"
# uvicorn app.main:app --reload
# https://www.youtube.com/watch?v=0sOvCWFmrtA

# pip freeze > requirements.txt



import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine,  get_db
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind = engine)


app = FastAPI()




    
while True:
    try: 
        conn = psycopg2.connect(host= 'localhost', database = 'fastapitutorial', user = 'postgres',password = 'pgAdminPasswordDB', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('db conected !')
        break
    except Exception as error:
        print('db connection failed !')
        print('error: ', error)
        time.sleep(2)
    

@app.get("/get-posts", response_model= List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
  
    return posts



@app.get("/get-post-by-id/{id}", response_model=schemas.PostResponse)
def get_post_by_id(id:int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")
    return post


@app.post("/create-post", status_code=status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_post(post : schemas.PostBase ,db: Session = Depends(get_db)):
    
#    new_post = models.Post(title = post.title, content = post.content, published = post.published, )
#    **post.dict() 
   new_post = models.Post(**post.dict() )

   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post 


@app.put("/update-post/{id}", response_model=schemas.PostResponse)
def update_post(id:int, post: schemas.PostBase, db: Session = Depends(get_db)):
    
    current_post = db.query(models.Post).filter(models.Post.id == id)
    
    c_post = current_post.first()
    
    if c_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")
    
    
    # post.update({'title': 'updated title', 'content': 'updated content'}, synchronize_session = False)
    current_post.update(post.dict(), synchronize_session = False)
    
    db.commit()
    
    return current_post.first()



@app.delete("/delete-post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} is wrong id ")
    
    db.delete(post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/create-user", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user( user: schemas.UserCreate ,db: Session = Depends(get_db)):
    
   # hash user's password
   
   hashed_password = pwd_context.hash(user.password) 
   user.password = hashed_password
    
   new_user = models.User(**user.dict() )
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return new_user 


@app.get("/get-user", response_model= List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    
    users = db.query(models.User).all()
  
    return users

