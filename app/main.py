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
    

my_posts = [{
    "id": 1,
    "title": "currently i am sending body title 1",
    "content": "content 1",
    "published": False,
    "rating": 1
},
            {
    "id": 2,
    "title": "currently i am sending body title 2",
    "content": "content 2",
    "published": False,
    "rating": 2
},
            ]

def find_post(id: int):
    for p in my_posts:
        if p['id'] == id:
            return p  
 

def find_post_index(id: int):
    for i , p in enumerate( my_posts):
        if p['id'] == id:
            return i 
    
    

@app.get("/get-posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"success":True ,"data": posts}

@app.get("/posts/latest")
def get_latest_post():
    # latest = my_posts[len(my_posts) - 1]
    cursor.execute(""" SELECT * FROM posts ORDER BY created_at DESC LIMIT 1  """)
    latest_post = cursor.fetchone()
    return {"success":True ,"data": latest_post}


@app.get("/posts/{id}")
def get_post_by_id(id: int, response : Response):
    # post = find_post(id)
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""",str(id))
    updated_post = cursor.fetchone()
    print(updated_post)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} Not found") 
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"success":False, "data": f"Post with id: {id} Not found"}
    return {"success":True ,"data": updated_post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def send_data(post: Post):
    
    cursor.execute(""" INSERT INTO posts (title, content, published ) VALUES (%s,%s,%s) RETURNING * """,( post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    # my_new_post = post.dict()
    # my_new_post["id"] = randrange(3,100000)
    # my_posts.append(my_new_post)
    print(new_post)
    return {"success":True , "data": new_post }



@app.put("/update-post/{id}", status_code=status.HTTP_201_CREATED)
def send_data(id:int ,post: Post):
    my_new_post = post.dict()
    index = find_post_index(id)
    if index == None:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail={f"does not exist"})
    
    my_new_post['id'] = id
    my_posts[index] = my_new_post
    
    return {"success":True , "data": my_posts,"post":my_new_post }



@app.delete("/delete-post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    
    if index == None:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail={f"does not exist"})
    my_posts.pop(index)
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)
