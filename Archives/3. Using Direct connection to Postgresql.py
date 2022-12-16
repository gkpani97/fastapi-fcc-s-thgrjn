from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    Rating: Optional[int] = None

while True:
    # We add it in while loop so that if there is any issue with network on database being online
    # the app can try infinitely until a connection is set up.
    # Offcourse this wont help with issues like wrong password
    try:
        conn = psycopg2.connect(host= 'localhost', database='fastapi', user='postgres', password='1234',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful!')
        break
    except Exception as error:
        print("Connection to the database failed!!")
        print("Error:", error)
        time.sleep(2)


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall() # fetches all results of the command. fetchmany and fetchone also there. look them up
    return {"data":posts}


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published),) # here we avoid using a f string f"INSERT.....{}{} " to avoid sql injection attacks and thus use %s placeholders.
    new_post = cursor.fetchone() # fetches one row.
    # doing until fetch wont change the db. so one has to commit
    conn.commit()
    return {"data": new_post}


@app.get("/post/{id}")
def get_posts(id: int):
    cursor.execute("""SELECT * from posts WHERE id = %s""",(str(id)),) # end the command argument with a comma. Here it is after id.
    result_post = cursor.fetchone()
    if not result_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found!")
    return {"data":result_post}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)),)
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}") 
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title= %s, content= %s, published= %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published,str(id)),)
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found!")
    return {"data": updated_post}