from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

    
app = FastAPI()

#used to validate the POST payload
class Post(BaseModel):
    title: str
    content: str
    # Adding a variable with a default value. So can ignore this altogether, while sending the payload.
    published: bool = True
    # optional input
    Rating: Optional[int] = None

my_posts = [{"id": 1, "title": "Title 1", "content": "Content 1"}, {"id": 2, "title": "Title 2", "content": "Content 2"}]

@app.get("/posts")
async def root():
    return my_posts

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Normal way of accepting payload as a Dictionary Data Structure using Body
# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)): 
#     print(payLoad)
#     return {"message": "successfully created post"}

# Using BaseModel to validate payload
@app.post("/posts")
def create_posts(post: Post):
    print(post.dict()) # converts the pydantic model to dict
    print(f"Title: {post.title}\nContent: {post.content}\nPublished: {post.published}, \nRating: {post.Rating}")
    return {"data": post}