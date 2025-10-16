from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from .db import get_session, lifespan
from .models import Movie, MovieCreate

app = FastAPI(title="Movie Watchlist V2", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items", response_model=list[Movie])
def list_movies(
    watched: bool | None = Query(default=None, description="Filter by watched state"),
    session: Session = Depends(get_session),
):
    stmt = select(Movie)
    if watched is not None:
        stmt = stmt.where(Movie.watched == watched)
    return session.exec(stmt).all()


@app.post("/items", response_model=Movie, status_code=201)
def create_movie(
    payload: MovieCreate,
    session: Session = Depends(get_session),
):
    # Light validation on year
    if payload.year < 1900 or payload.year > 2030:
        raise HTTPException(status_code=422, detail="Year must be between 1900 and 2030")

    movie = Movie(title=payload.title, year=payload.year, watched=payload.watched)
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie
