from sqlmodel import Field, SQLModel


# Table model
class Movie(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    year: int
    watched: bool = False


# Payload model for create
class MovieCreate(SQLModel):
    title: str
    year: int
    watched: bool = False
