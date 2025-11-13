from app.agents.agent_state import AgentState
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.llm_manager import get_llm
from app.agents.prompts.normal_chat_prompt import NORMAL_CHAT_PROMPT
from app.core.loggers import logger


def normal_chat_node(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0)

    history = state.get("messages", [])
    user_query = state.get("user_query", "")

    llm_message = history + [HumanMessage(content=user_query)]
    logger.info(f"normal_chat_node: Generating casual response.")

    system_message = NORMAL_CHAT_PROMPT

    messages = [SystemMessage(content=system_message), ] + llm_message

    response = llm.invoke(messages)
    state["reply"] = response.content.strip()
    return state