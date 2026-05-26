import uuid

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from hr_agent_app.config import LANGSMITH_PROJECT
from hr_agent_app.graph import build_graph

active_sessions: dict[str, str] = {}
graph = build_graph(checkpointer=MemorySaver())


def get_or_create_thread_id(chat_id: str) -> str:
    if chat_id not in active_sessions:
        session_id = str(uuid.uuid4())
        active_sessions[chat_id] = f"{chat_id}:{session_id}"

    return active_sessions[chat_id]


def finish_interview(chat_id: str) -> None:
    active_sessions.pop(chat_id, None)


def handle_message(chat_id: str, text: str) -> str:
    thread_id = get_or_create_thread_id(chat_id)

    result = graph.invoke(
        {
            "chat_id": chat_id,
            "messages": [HumanMessage(content=text)],
        },
        config={
            "configurable": {
                "thread_id": thread_id,
            },
            "metadata": {
                "chat_id": chat_id,
                "thread_id": thread_id,
                "project": LANGSMITH_PROJECT,
            },
            "run_name": "hr_agent_graph_guard_reask",
        },
    )

    if result.get("final_answer", False):
        finish_interview(chat_id)

    return result["assistant_response"]
