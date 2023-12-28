
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, oauth2
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List, Optional

router = APIRouter(
    prefix='/vote',
    tags=['Votes']
)



@router.post("/" ,status_code=status.HTTP_201_CREATED,)
def like_post( vote: schemas.VoteBase ,
              db: Session = Depends(get_db),
              get_current_user: int =Depends(oauth2.get_current_user)):
    
   valid_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first() 
   if not valid_post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found") 
   
   vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == get_current_user.id)
    
   found_vote = vote_query.first()
   
   if vote.direction == 1:
       if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                           detail=f"user {get_current_user.id} has already voted on post {vote.post_id}") 
       new_vote = models.Vote(post_id = vote.post_id, user_id = get_current_user.id) 
       db.add(new_vote)
       db.commit()  
       return {"message": "Successfully voted"}
   else:
       if not found_vote:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"user {get_current_user.id} has not voted yet on post {vote.post_id}") 
       vote_query.delete(synchronize_session=False)
       db.commit()
       return {"message": "Successfully deleted"}
          
    
  
        
    

   

   db.refresh(liked_post)
   return liked_post 

