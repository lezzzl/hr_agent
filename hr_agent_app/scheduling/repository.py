from dataclasses import dataclass
from datetime import datetime

from hr_agent_app.scheduling.db import get_connection, init_db


@dataclass(frozen=True)
class InterviewSlot:
    id: int
    starts_at: str
    ends_at: str
    timezone: str
    interviewer: str
    role: str | None
    status: str
    candidate_name: str | None = None
    candidate_contact: str | None = None
    chat_id: str | None = None


def _row_to_slot(row) -> InterviewSlot:
    return InterviewSlot(
        id=row["id"],
        starts_at=row["starts_at"],
        ends_at=row["ends_at"],
        timezone=row["timezone"],
        interviewer=row["interviewer"],
        role=row["role"],
        status=row["status"],
        candidate_name=row["candidate_name"],
        candidate_contact=row["candidate_contact"],
        chat_id=row["chat_id"],
    )


def create_slot(
    starts_at: str,
    ends_at: str,
    timezone: str,
    interviewer: str,
    role: str | None = None,
) -> int:
    init_db()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO interview_slots (starts_at, ends_at, timezone, interviewer, role)
            VALUES (?, ?, ?, ?, ?)
            """,
            (starts_at, ends_at, timezone, interviewer, role),
        )
        return int(cursor.lastrowid)


def list_available_slots(role: str | None = None, limit: int = 5) -> list[InterviewSlot]:
    init_db()
    limit = max(1, min(limit, 20))

    query = """
        SELECT *
        FROM interview_slots
        WHERE status = 'available'
    """
    params: list[object] = []

    if role:
        query += " AND (role IS NULL OR lower(role) = lower(?))"
        params.append(role)

    query += " ORDER BY starts_at ASC LIMIT ?"
    params.append(limit)

    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()
        return [_row_to_slot(row) for row in rows]


def book_slot(
    slot_id: int,
    candidate_name: str,
    candidate_contact: str,
    chat_id: str | None = None,
) -> InterviewSlot | None:
    init_db()
    now = datetime.utcnow().isoformat(timespec="seconds")

    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT *
            FROM interview_slots
            WHERE id = ? AND status = 'available'
            """,
            (slot_id,),
        ).fetchone()

        if row is None:
            return None

        connection.execute(
            """
            UPDATE interview_slots
            SET status = 'booked',
                candidate_name = ?,
                candidate_contact = ?,
                chat_id = ?,
                updated_at = ?
            WHERE id = ? AND status = 'available'
            """,
            (candidate_name, candidate_contact, chat_id, now, slot_id),
        )

        booked = connection.execute(
            "SELECT * FROM interview_slots WHERE id = ?",
            (slot_id,),
        ).fetchone()
        return _row_to_slot(booked)


def get_slot(slot_id: int) -> InterviewSlot | None:
    init_db()
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM interview_slots WHERE id = ?",
            (slot_id,),
        ).fetchone()
        return _row_to_slot(row) if row else None
