from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime



class Post(Base):
    __tablename__ = "posts2"
    
    id = Column(Integer, primary_key= True, nullable= False)
    title = Column(String, nullable=False)
    content = Column(String, nullable= False)
    published = Column(Boolean, nullable=False, default=False)
    # date_created = Column(DateTime, nullable=False, )
    