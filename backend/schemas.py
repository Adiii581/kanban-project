from pydantic import BaseModel
from typing import List, Optional

# Schemas for Cards
class CardBase(BaseModel):
    title: str
    description: Optional[str] = None

class CardCreate(CardBase):
    pass

class Card(CardBase):
    id: int
    list_id: int
    class Config:
        orm_mode = True

# Schemas for Lists
class ListBase(BaseModel):
    title: str

class ListCreate(ListBase):
    pass

class List(ListBase):
    id: int
    board_id: int
    cards: List[Card] = []
    class Config:
        orm_mode = True

# Schemas for Boards
class BoardBase(BaseModel):
    title: str

class BoardCreate(BoardBase):
    pass

class Board(BoardBase):
    id: int
    owner_id: int
    lists: List[List] = []
    class Config:
        orm_mode = True

# Schemas for Users
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True
        
# Schema for JWT Token Response
class Token(BaseModel):
    access_token: str
    token_type: str