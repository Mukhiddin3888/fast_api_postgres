


from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass    

class UserResponse(BaseModel):
    id:int
    email: str
    created_at: datetime
    password:str
    
    class Config:
        orm_mode = True

class VoteBase(BaseModel):
    post_id: int
    direction:conint(le=1, ge=0)
    
        
class VoteResponse(VoteBase):
    pass 
   
    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner: UserResponse
    # vote_count: int

    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
                
class TokenData(BaseModel):
    id: Optional[int] = None                
    
