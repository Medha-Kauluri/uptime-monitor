import logging
from datetime import datetime

import requests
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import URLMonitor

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT_SECONDS = 10


def _is_up(status_code: int) -> bool:
    return 200 <= status_code < 400


def check_single_url(monitor: URLMonitor) -> None:
    try:
        response = requests.get(
            monitor.url,
            timeout=REQUEST_TIMEOUT_SECONDS,
            allow_redirects=True,
        )
        monitor.status_code = response.status_code
        monitor.response_time_ms = response.elapsed.total_seconds() * 1000
        monitor.status = "UP" if _is_up(response.status_code) else "DOWN"
    except requests.RequestException as exc:
        logger.warning("Check failed for %s: %s", monitor.url, exc)
        monitor.status = "DOWN"
        monitor.status_code = None
        monitor.response_time_ms = None

    monitor.checked_at = datetime.utcnow()


def check_all_urls() -> None:
    db: Session = SessionLocal()
    try:
        monitors = db.query(URLMonitor).all()
        for monitor in monitors:
            check_single_url(monitor)
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("Unexpected error during URL checks")
        raise
    finally:
        db.close()
