from langgraph.graph import END, START, StateGraph

from hr_agent_app.nodes import (
    blocked_message_node,
    formatter_node,
    input_guardrail_node,
    interview_node,
    role_selection_node,
    route_after_guardrail,
    route_after_interview,
    skills_extraction_node,
)
from hr_agent_app.state import InterviewState


def build_graph(checkpointer=None):
    builder = StateGraph(InterviewState)

    builder.add_node("input_guardrail", input_guardrail_node)
    builder.add_node("block_message", blocked_message_node)
    builder.add_node("interview", interview_node)
    builder.add_node("skills_extraction", skills_extraction_node)
    builder.add_node("role_selection", role_selection_node)
    builder.add_node("formatter", formatter_node)

    builder.add_edge(START, "input_guardrail")
    builder.add_conditional_edges(
        "input_guardrail",
        route_after_guardrail,
        {
            "ask_question": "interview",
            "block_message": "block_message",
        },
    )
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
