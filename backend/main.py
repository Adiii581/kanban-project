from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

import auth
import models
import schemas
from models import SessionLocal, create_tables

app = FastAPI()

# CORS Middleware to allow the frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://kanban-project.vercel.app"], # IMPORTANT: Update this with your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

@app.on_event("startup")
def on_startup():
    create_tables()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# === AUTHENTICATION ENDPOINTS ===
@app.post("/api/users/register", response_model=schemas.UserSchema)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# === BOARD ENDPOINTS ===
@app.post("/api/boards/", response_model=schemas.BoardSchema)
def create_board(board: schemas.BoardCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_board = models.Board(**board.dict(), owner_id=current_user.id)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

@app.get("/api/boards/", response_model=List[schemas.BoardSchema])
def get_user_boards(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Board).filter(models.Board.owner_id == current_user.id).all()

@app.get("/api/boards/{board_id}", response_model=schemas.BoardSchema)
def get_board_details(board_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.owner_id == current_user.id).first()
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found or you do not have permission to view it")
    return board

# === LIST ENDPOINTS ===
@app.post("/api/boards/{board_id}/lists", response_model=schemas.ListSchema)
def create_list_for_board(board_id: int, list_data: schemas.ListCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.owner_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found or you do not have permission")
    db_list = models.List(**list_data.dict(), board_id=board_id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

# === CARD ENDPOINTS ===
@app.post("/api/lists/{list_id}/cards", response_model=schemas.CardSchema)
def create_card_for_list(list_id: int, card_data: schemas.CardCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_list = db.query(models.List).join(models.Board).filter(models.List.id == list_id, models.Board.owner_id == current_user.id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found or you do not have permission")
    db_card = models.Card(**card_data.dict(), list_id=list_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card