from pydantic import BaseModel
from typing import List, Optional

# --- Schemas for Cards ---
class CardBase(BaseModel):
    title: str
    description: Optional[str] = None

class CardCreate(CardBase):
    pass

class CardSchema(CardBase):
    id: int
    list_id: int
    class Config:
        from_attributes = True

# --- Schemas for Lists ---
class ListBase(BaseModel):
    title: str

class ListCreate(ListBase):
    pass

class ListSchema(ListBase):
    id: int
    board_id: int
    cards: List[CardSchema] = []
    class Config:
        from_attributes = True

# --- Schemas for Boards ---
class BoardBase(BaseModel):
    title: str

class BoardCreate(BoardBase):
    pass

class BoardSchema(BoardBase):
    id: int
    owner_id: int
    lists: List[ListSchema] = []
    class Config:
        from_attributes = True

# --- Schemas for Users ---
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    class Config:
        from_attributes = True
        
# --- Schema for JWT Token ---
class Token(BaseModel):
    access_token: str
    token_type: str