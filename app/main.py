# Python version 3.11.5
#  in requiremnts txt info

from fastapi import FastAPI
from app import models
from app.database import engine
from app.routes import post, user, auth, vote
from app.config import settings

models.Base.metadata.create_all(bind = engine)



app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

