from models import Base
from database import engine
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from models import User

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/users/")
def register_user(user_in: UserCreate):
    session = SessionLocal()
    try:
        existing = session.query(User).filter(User.username == user_in.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")
        user = User.create_user(username=user_in.username, password=user_in.password)
        session.add(user)
        session.commit()
        return {"id": str(user.id), "username": user.username}
    finally:
        session.close()

Base.metadata.create_all(bind=engine)
