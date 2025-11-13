from datetime import datetime, timedelta
from sqlalchemy.orm import Session as DBSession

from app.schemas.session import SessionCreate
from app.models.session import Session as SessionModel
from app.repositories.session_repository import SessionRepository
from fastapi import HTTPException

class SessionService:
    def __init__(self, db: DBSession):
        self.db = db
        self.session_repo = SessionRepository(db)

    def create_session(self, session_data: SessionCreate) -> SessionModel:
        return self.session_repo.create_session(session_data)

    def validate_session(self, session_id: str) -> SessionModel:
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")

        session = self.session_repo.get_session_by_id(session_id)

        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")

        if session.expires_at and session.expires_at < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Session expired")

        return self.session_repo.update_session_activity(session)

    def is_session_valid(self, session_id: str) -> bool:
        try:
            self.validate_session(session_id)
            return True
        except HTTPException:
            return False