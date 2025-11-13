from sqlalchemy.orm import Session as DBSession
from app.agents.agent_graph import create_graph
from app.agents.agent_state import AgentState
from app.repositories.chatbot_repository import ChatbotRepository
from app.services.session_services import SessionService
from langchain_core.messages import HumanMessage, AIMessage

class ChatService:
    def __init__(self, db: DBSession):
        self.db = db
        self.agent = create_graph()
        self.chat_repo = ChatbotRepository(db)
        self.session_service = SessionService(db)

    async def get_chat_history(self, session_id: str):
        return await self.chat_repo.get_chat_history(session_id)

    async def process_message(self, session_id: str, message: str):
        self.chat_repo.create_message(session_id=session_id, sender="user", content=message)
        history_models = self.chat_repo.get_chat_history(session_id)
        formatted_messages = []
        for m in history_models:
            if m.sender == "user":
                formatted_messages.append(HumanMessage(content=m.content))
            elif m.sender == "bot":
                formatted_messages.append(AIMessage(content=m.content))

        thread_config = {
            "configurable": {
                "thread_id": session_id,
                "checkpoint_ns": "default"
            }
        }

        initial_agent_state: AgentState = {
            "messages": formatted_messages,
            "user_query": message,
            "reply": "",
            "decision": ""
        }

        agent_state = await self.agent.ainvoke(initial_agent_state, config=thread_config)
        response = agent_state["reply"]

        bot_msg = self.chat_repo.create_message(session_id=session_id, sender="bot", content=response)

        return {"reply": response, "saved": True, "message": bot_msg}