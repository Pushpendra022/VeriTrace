from datetime import datetime, timedelta, timezone

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.models.document import Document


def delete_expired_reviews(db: Session, retention_days: int | None, now: datetime | None = None) -> int:
    """Delete persisted review data older than the configured retention period.

    Original uploads are never stored. ORM/database cascades remove extracted pages,
    chunks, claims, and verification traces belonging to expired documents.
    """
    if retention_days is None:
        return 0
    cutoff = (now or datetime.now(timezone.utc)) - timedelta(days=retention_days)
    result = db.execute(delete(Document).where(Document.updated_at < cutoff))
    db.commit()
    return result.rowcount or 0
