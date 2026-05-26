from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class InterviewState(TypedDict, total=False):
    chat_id: str

    interview_started: bool
    interview_finished: bool
    input_status: str | None

    current_step_id: int
    candidate_profile: dict

    extracted_skills: dict
    predicted_role: str

    intent: str | None
    retrieved_docs: list

    messages: Annotated[list[AnyMessage], add_messages]

    assistant_response: str | None
    final_answer: str | None
