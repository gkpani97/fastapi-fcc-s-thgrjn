from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas, utils
from .routers import post, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Hello World"}