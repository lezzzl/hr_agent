from langgraph.graph import END, START, StateGraph

from hr_agent_app.nodes import (
    agent_node,
    blocked_message_node,
    formatter_node,
    input_check_node,
    interview_node,
    role_selection_node,
    route_after_input,
    route_after_interview,
    skills_extraction_node,
    route_after_agent,
)
from hr_agent_app.state import InterviewState
from langgraph.prebuilt import ToolNode
from hr_agent_app.tools import book_interview_slot, list_interview_slots, search_hr_documents



def build_graph(checkpointer=None):
    builder = StateGraph(InterviewState)

    tools = [search_hr_documents, list_interview_slots, book_interview_slot]
    tool_node = ToolNode(tools)

    builder.add_node("input_check", input_check_node)
    builder.add_node("block_message", blocked_message_node)
    builder.add_node("agent", agent_node)
    builder.add_node("interview", interview_node)
    builder.add_node("skills_extraction", skills_extraction_node)
    builder.add_node("role_selection", role_selection_node)
    builder.add_node("formatter", formatter_node)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "input_check")
    builder.add_conditional_edges(
        "input_check",
        route_after_input,
        {
            "ask_question": "interview",
            "agent": "agent",
            "block_message": "block_message",
        },
    )
    builder.add_conditional_edges(
        "agent", route_after_agent,
        {
            "tools": "tools",
            "end": END,
        },
    )
    builder.add_edge("tools", "agent")
    builder.add_edge("block_message", END)

    builder.add_conditional_edges(
        "interview",
        route_after_interview,
        {
            "extraction": "skills_extraction",
            "end": END,
        },
    )
    builder.add_edge("skills_extraction", "role_selection")
    builder.add_edge("role_selection", "formatter")
    builder.add_edge("formatter", END)

    if checkpointer is None:
        return builder.compile()

    return builder.compile(checkpointer=checkpointer)


graph = build_graph()
