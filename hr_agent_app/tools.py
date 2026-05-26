from langchain_core.tools import tool

from hr_agent_app.rag.retriever import format_documents, search_hr_knowledge
from hr_agent_app.scheduling.repository import book_slot, list_available_slots


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
def list_interview_slots(role: str | None = None, limit: int = 5) -> str:
    """
    Используй этот инструмент, когда кандидат хочет посмотреть доступные слоты для интервью.

    role можно передать, если кандидат спрашивает слот для конкретной роли.
    limit ограничивает количество возвращаемых слотов.
    """
    slots = list_available_slots(role=role, limit=limit)
    if not slots:
        return "Свободных слотов для интервью сейчас нет."

    lines = ["Свободные слоты для интервью:"]
    for slot in slots:
        role_text = f", роль: {slot.role}" if slot.role else ""
        lines.append(
            f"{slot.id}. {slot.starts_at}-{slot.ends_at} {slot.timezone}, "
            f"интервьюер: {slot.interviewer}{role_text}"
        )

    return "\n".join(lines)


@tool
def book_interview_slot(
    slot_id: int,
    candidate_name: str,
    candidate_contact: str,
    chat_id: str | None = None,
) -> str:
    """
    Используй этот инструмент, когда кандидат выбрал конкретный слот и хочет записаться на интервью.

    Нужны slot_id, имя кандидата и контакт для связи.
    """
    booked = book_slot(
        slot_id=slot_id,
        candidate_name=candidate_name,
        candidate_contact=candidate_contact,
        chat_id=chat_id,
    )

    if booked is None:
        return (
            "Не удалось забронировать слот: он уже занят или не существует. "
            "Попросите кандидата выбрать другой свободный слот."
        )

    return (
        "Слот успешно забронирован.\n"
        f"Слот: {booked.id}\n"
        f"Время: {booked.starts_at}-{booked.ends_at} {booked.timezone}\n"
        f"Интервьюер: {booked.interviewer}\n"
        f"Кандидат: {booked.candidate_name}\n"
        f"Контакт: {booked.candidate_contact}"
    )
