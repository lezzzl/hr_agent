from langchain_core.tools import tool

from hr_agent_app.rag.retriever import format_documents, search_hr_knowledge


@tool
def search_hr_documents(question: str) -> str:
    """
    Используй этот инструмент, чтобы искать информацию в базе знаний HR-бота.

    Инструмент подходит для вопросов о:
    - процессе найма;
    - этапах интервью;
    - сроках обратной связи;
    - политиках компании;
    - формате работы;
    - ролях в ML-команде;
    - требованиях к кандидатам;
    - FAQ по интервью.

    На вход передаётся вопрос кандидата.
    На выходе возвращаются релевантные фрагменты документов из базы знаний.
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
