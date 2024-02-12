
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, oauth2
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List, Optional

from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# @router.get("/", response_model= List[schemas.PostResponse])
@router.get("/")
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    votes_count1 = db.query(models.Vote).filter(models.Vote.post_id == models.Post.id)
    
    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id , isouter=True).group_by(models.Post.id).all()
    
    results = []
    for post in posts:
        vote_count = db.query(models.Vote).filter(models.Vote.post_id == post.id).count()
        post_with_vote_count = {"post": post, "votes": vote_count}
        results.append(post_with_vote_count)
    
    # print(results)
    
    return results



@router.get("/{id}", response_model=schemas.PostResponse)
def get_post_by_id(id:int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_post(post : schemas.PostBase ,
                db: Session = Depends(get_db), 
                get_current_user: int =Depends(oauth2.get_current_user)):
    
#    new_post = models.Post(title = post.title, content = post.content, published = post.published, )
#    **post.dict() 
   new_post = models.Post( owner_id = get_current_user.id,**post.dict() )
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post 


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, post: schemas.PostBase, 
                db: Session = Depends(get_db),
                get_current_user: int =Depends(oauth2.get_current_user)):
    
    current_post = db.query(models.Post).filter(models.Post.id == id)
    
    c_post = current_post.first()
    
    if c_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found")
    
    if c_post.owner_id != get_current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{id} post not belongs to you ")
    
    # post.update({'title': 'updated title', 'content': 'updated content'}, synchronize_session = False)
    current_post.update(post.dict(), synchronize_session = False)
    
    db.commit()
    
    return current_post.first()



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_db),
                get_current_user: int =Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} is wrong id ")
    
    if post.owner_id != get_current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{id} post not belongs to you ")

    db.delete(post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
