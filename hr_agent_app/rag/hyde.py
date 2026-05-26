from langchain_core.messages import HumanMessage, SystemMessage

from hr_agent_app.config import get_llm


def generate_hypothetical_answer(question: str) -> str:
    llm = get_llm()
    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "Ты создаёшь HyDE-запрос для RAG-поиска по HR-базе знаний. "
                    "Напиши короткий вероятный ответ на вопрос кандидата так, "
                    "как он мог бы быть сформулирован в документации компании. "
                    "Не выдумывай конкретные факты, даты, имена и цифры, если они не следуют из вопроса. "
                    "Верни только текст гипотетического ответа без markdown."
                )
            ),
            HumanMessage(content=question),
        ]
    )

    return response.content.strip()


def build_hyde_query(question: str) -> str:
    hypothetical_answer = generate_hypothetical_answer(question)
    if not hypothetical_answer:
        return question

    return (
        f"Вопрос кандидата:\n{question}\n\n"
        f"Гипотетический ответ из HR-документации:\n{hypothetical_answer}"
    )
