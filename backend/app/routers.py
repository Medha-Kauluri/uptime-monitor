from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

router = APIRouter(prefix="/urls", tags=["urls"])


@router.post("", response_model=schemas.URLResponse, status_code=status.HTTP_201_CREATED)
def add_url(payload: schemas.URLCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_url(db, payload)
    except crud.DuplicateURLError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="URL is already being monitored",
        )


@router.get("", response_model=list[schemas.URLResponse])
def list_urls(db: Session = Depends(get_db)):
    return crud.get_urls(db)
