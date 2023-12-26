# Python version 3.11.5
# uvicorn app.main:app --reload
# https://www.youtube.com/watch?v=0sOvCWFmrtA


import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

from sqlalchemy.orm import Session
from app import models
from app.database import engine,  get_db

models.Base.metadata.create_all(bind = engine)


app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
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
    

@app.get("/get-posts")
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
  
    return {"data": posts}



@app.get("/get-post-by-id/{id}")
def get_post_by_id(id:int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")
    return {"data": post}


@app.post("/create-post", status_code=status.HTTP_201_CREATED)
def create_post(post :Post ,db: Session = Depends(get_db)):
    
#    new_post = models.Post(title = post.title, content = post.content, published = post.published, )
#    **post.dict() 
   new_post = models.Post(**post.dict() )

   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return {"data":new_post }


@app.put("/update-post/{id}")
def update_post(id:int, post: Post, db: Session = Depends(get_db)):
    
    current_post = db.query(models.Post).filter(models.Post.id == id)
    
    c_post = current_post.first()
    
    if c_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")
    
    
    # post.update({'title': 'updated title', 'content': 'updated content'}, synchronize_session = False)
    current_post.update(post.dict(), synchronize_session = False)
    
    db.commit()
    
    return {"data": current_post.first()}



@app.delete("/delete-post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} is wrong id ")
    
    db.delete(post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)