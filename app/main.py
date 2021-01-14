from typing import Optional, List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/", response_model=List[schemas.Person])
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.Person).all()
    return users

