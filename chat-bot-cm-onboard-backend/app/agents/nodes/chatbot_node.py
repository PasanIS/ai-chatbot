from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.agent_state import AgentState
from app.agents.llm_manager import get_llm
from app.agents.prompts.routing_prompt import ROUTING_PROMPT
from app.core.loggers import logger


def chatbot_node(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0)

    history = state.get("messages", [])
    user_query = state.get("user_query", "")
    llm_message = history + [HumanMessage(content=user_query)]

    logger.info(f"Chatbot Node: Routing user query for {len(llm_message)} messages.")

    system_message = ROUTING_PROMPT

    messages = [SystemMessage(content=system_message), ] + llm_message

    response = llm.invoke(messages)

    state["reply"] = response.content.strip()
    logger.info(f"chatbot_node: Decision is '{state['reply']}'")
    return state