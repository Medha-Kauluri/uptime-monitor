from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas


class DuplicateURLError(Exception):
    pass


def normalize_url(payload: schemas.URLCreate) -> str:
    return str(payload.url).rstrip("/")


def create_url(db: Session, payload: schemas.URLCreate) -> models.URLMonitor:
    db_url = models.URLMonitor(url=normalize_url(payload))
    db.add(db_url)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateURLError from exc
    db.refresh(db_url)
    return db_url


def get_urls(db: Session) -> list[models.URLMonitor]:
    return db.query(models.URLMonitor).order_by(models.URLMonitor.id).all()
