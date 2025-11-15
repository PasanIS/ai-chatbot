from sqlalchemy.orm import Session as DBSession
from app.models.chat_message import ChatMessage
from typing import List

class ChatbotRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def get_chat_history(self, session_id: str, limit: int = 10) -> List[ChatMessage]:

        messages = (
            self.db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
            .all()
        )
        return list(reversed(messages))

    def create_message(self, session_id: str, sender: str, content: str) -> ChatMessage:

        db_msg = ChatMessage(session_id=session_id, sender=sender, content=content)
        self.db.add(db_msg)
        self.db.commit()
        self.db.refresh(db_msg)
        return db_msg