from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from app.agents.agent_state import AgentState
from app.agents.nodes.chatbot_node import chatbot_node
from app.agents.nodes.normal_chat_node import normal_chat_node
from app.agents.nodes.tool_caller_node import tool_caller_node

def create_graph():
    graphflow = StateGraph(AgentState)

    def route_after_chatbot(state: AgentState) -> str:
        decision = state.get("reply", "").strip().lower()
        if decision == "database_query_tool":
            return "call_tools"
        elif decision == "normal_chat":
            return "casual"
        else:
            return "call_tools"

    graphflow.add_node("chatbot_node", chatbot_node)
    graphflow.add_node("tool_caller_node", tool_caller_node)
    graphflow.add_node("normal_chat_node", normal_chat_node)

    graphflow.set_entry_point("chatbot_node")

    graphflow.add_conditional_edges(
        "chatbot_node",
        route_after_chatbot,
        {
            "call_tools": "tool_caller_node",
            "casual": "normal_chat_node"
        }
    )

    graphflow.add_edge("tool_caller_node", END)
    graphflow.add_edge("normal_chat_node", END)

    memory = MemorySaver()
    graph = graphflow.compile(checkpointer=memory)


    image_bytes = graph.get_graph().draw_mermaid_png()
    with open("agent_workflow_graph.png", "wb") as f:
        f.write(image_bytes)
    print("Graph saved as 'agent_workflow_graph.png'")
    from IPython.display import Image, display
    display(Image(image_bytes))

    return graph