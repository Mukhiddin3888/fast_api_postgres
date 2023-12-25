# Python version 3.11.5
import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
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
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"success":True ,"data": posts}

@app.get("/posts/latest")
def get_latest_post():

    cursor.execute(""" SELECT * FROM posts ORDER BY created_at DESC LIMIT 1  """)
    latest_post = cursor.fetchone()
    if latest_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    
    return {"success":True ,"data": latest_post}


@app.get("/posts/{id}")
def get_post_by_id(id: int, response : Response):

    cursor.execute(""" SELECT * FROM posts WHERE id = %s""",str(id))
    updated_post = cursor.fetchone()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    return {"success":True ,"data": updated_post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def send_data(post: Post):
    
    cursor.execute(""" INSERT INTO posts (title, content, published ) VALUES (%s,%s,%s) RETURNING * """,( post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"success":True , "data": new_post }



@app.put("/update-post/{id}", status_code=status.HTTP_201_CREATED)
def send_data(id:int ,post: Post):
   
    cursor.execute(""" UPDATE posts SET title = %s, content= %s, published = %s WHERE id  = %s RETURNING * """,(post.title, post.content, post.published, str(id)))
   
    updated_post  = cursor.fetchone() 
    conn.commit()
    
    if updated_post == None:
         raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail=f"{id} does not exist")
    return {"success":True , "updated_post": updated_post}



@app.delete("/delete-post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
  
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
   
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail=f"does not exist")
   
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)
