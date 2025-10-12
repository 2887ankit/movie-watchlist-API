from typing import Optional
from sqlmodel import SQLModel, Field

# Table model
class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    year: int
    watched: bool = False

# Input/output schemas
class MovieCreate(SQLModel):
    title: str
    year: int
    watched: bool = False
