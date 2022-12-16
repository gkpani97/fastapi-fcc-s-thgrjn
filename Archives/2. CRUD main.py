from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    Rating: Optional[int] = None

my_posts = [{"id": 1, "title": "Title 1", "content": "Content 1"}, 
            {"id": 2, "title": "Title 2", "content": "Content 2"}]

def find_post(id):
    out= [p for p in my_posts if p["id"] == id]
    return out[0] if out else None

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return None

@app.get("/posts")
def get_posts():
    return my_posts


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = len(my_posts) + 1
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/post/{id}") # id is a path parameter
def get_posts(id: int):
# def get_posts(id: int, response: Response):
    out = find_post(int(id))
    if not out:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found!")
    return out


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id):
    index = find_index_post(int(id))
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found!")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}") 
def update_post(id: int, post: Post):# adding id: int here automatically converts id to int unlike how it happens in delete function
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found!")
    for key in post.dict():
        my_posts[index][key] = post.dict()[key]
    return {"data": post.dict()}