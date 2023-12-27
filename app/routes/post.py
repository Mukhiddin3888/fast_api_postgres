
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, utils
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("/", response_model= List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
  
    return posts



@router.get("/{id}", response_model=schemas.PostResponse)
def get_post_by_id(id:int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_post(post : schemas.PostBase ,db: Session = Depends(get_db)):
    
#    new_post = models.Post(title = post.title, content = post.content, published = post.published, )
#    **post.dict() 
   new_post = models.Post(**post.dict() )

   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post 


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, post: schemas.PostBase, db: Session = Depends(get_db)):
    
    current_post = db.query(models.Post).filter(models.Post.id == id)
    
    c_post = current_post.first()
    
    if c_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")
    
    
    # post.update({'title': 'updated title', 'content': 'updated content'}, synchronize_session = False)
    current_post.update(post.dict(), synchronize_session = False)
    
    db.commit()
    
    return current_post.first()



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} is wrong id ")
    
    db.delete(post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)