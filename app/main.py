# Python version 3.11.5
#  in requiremnts txt info



import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import engine,  get_db
from app.routes import post, user


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
    

app.include_router(post.router)
app.include_router(user.router)

