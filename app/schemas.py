


from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # owner_id: int
    
class PostCreate(PostBase):
    pass    


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id:int
    email: str
    created_at: datetime
    password:str
    
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
                
class TokenData(BaseModel):
    id: Optional[int] = None                