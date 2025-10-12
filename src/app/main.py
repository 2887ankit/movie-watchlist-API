from typing import List, Optional

from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import select, Session

from .models import Movie, MovieCreate
from .db import get_session, lifespan

app = FastAPI(title="Movie Watchlist", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/items", response_model=List[Movie])
def list_movies(
    watched: Optional[bool] = Query(default=None, description="Filter by watched state"),
    session: Session = Depends(get_session),
):
    stmt = select(Movie)
    if watched is not None:
        stmt = stmt.where(Movie.watched == watched)
    return session.exec(stmt).all()

@app.post("/items", response_model=Movie, status_code=201)
def create_movie(payload: MovieCreate, session: Session = Depends(get_session)):
    # Light validation on year
    if payload.year < 1900 or payload.year > 2030:
        raise HTTPException(status_code=422, detail="year must be between 1900 and 2030")
    movie = Movie(**payload.model_dump())
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie