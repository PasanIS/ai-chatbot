from langchain_core.messages import HumanMessage, AIMessage
from app.agents.agent_state import AgentState
from app.agents.tools.sql_query_tool import sql_query_tool
import traceback

from app.core.loggers import logger


def tool_caller_node(state: AgentState) -> AgentState:

    try:
        decision = state.get("reply", "").strip().lower()
        messages = state.get("messages", [])

        if not messages or not isinstance(messages[-1], (HumanMessage, AIMessage)):
            query = state.get("user_query", "")
            history_list = []
        else:
            query = messages[-1].content
            history_list = messages[:-1]

        message_history = []
        for msg in history_list:
            if isinstance(msg, HumanMessage):
                message_history.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                message_history.append({"role": "assistant", "content": msg.content})

        if decision == "database_query_tool":

            logger.info("tool_caller_node: Routing to sql_query_tool.")

            tool_input = message_history + [{"role": "user", "content": query}]
            result = sql_query_tool.invoke({"user_query": tool_input})
            state["reply"] = result

        elif decision == "web_search_tool":

            logger.warning("tool_caller_node: Web search tool called but not implemented.")

            state["reply"] = "Web search tools not implemented yet."
        else:

            logger.warning(f"tool_caller_node: Unknown decision '{decision}'.")
            pass

    except Exception as e:

        logger.error(f"Error in tool_caller_node: {e}\n{traceback.format_exc()}")

        state["reply"] = f"An error occurred in the tool caller: {e}"

    return state