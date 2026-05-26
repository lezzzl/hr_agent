from langchain_core.tools import tool

from hr_agent_app.rag.retriever import format_documents, search_hr_knowledge


@tool
def search_hr_documents(question: str) -> str:
    """
    Use this tool to answer questions about hiring process, interview stages,
    company policies, work format, ML team roles, interview timelines and FAQ.
    """
    try:
        documents = search_hr_knowledge(question)
    except FileNotFoundError:
        return (
            "База знаний ещё не проиндексирована. "
            "Запустите команду: python -m hr_agent_app.rag.ingest"
        )
    except Exception as exc:
        return f"Не удалось выполнить поиск по базе знаний: {exc}"

    return format_documents(documents)


@tool
def book_interview_slot(request: str) -> str:
    """
    Use this tool when candidate wants to book, schedule or reserve an interview slot.
    """
    return (
        f"Я зафиксировал запрос на слот: {request}. "
        "Пока интеграция с календарём не подключена, поэтому реальное бронирование "
        "не выполнено. Позже здесь будет проверка свободных слотов и создание события."
    )
