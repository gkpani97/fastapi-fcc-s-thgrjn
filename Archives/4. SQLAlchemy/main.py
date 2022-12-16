from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas

# This function call creates the table (here "posts") if it is not already present
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/post/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db)):
    # filter is used for WHERE and first() is used instead of all() to get only one result more efficiently.
    result_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not result_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found!")
    return result_post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    # instead of typing the whole object, we can convert it to dict and use **kwargs like argument extension
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found!")
    post.delete(synchronize_session= False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}", response_model=schemas.Post) 
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    update_query = db.query(models.Post).filter(models.Post.id == id)
    if update_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found!")
    update_query.update(post.dict(), synchronize_session= False)
    db.commit()
    return update_query.first()