from datetime import datetime, timedelta

from hr_agent_app.scheduling.db import init_db
from hr_agent_app.scheduling.repository import create_slot

TIMEZONE = "Europe/Moscow"


def seed_slots() -> None:
    init_db()

    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    base_day = now + timedelta(days=1)

    slots = [
        (base_day.replace(hour=11), "Анна", "Data Scientist"),
        (base_day.replace(hour=15), "Иван", "Data Analyst"),
        ((base_day + timedelta(days=1)).replace(hour=12), "Мария", "Data Engineer"),
        ((base_day + timedelta(days=1)).replace(hour=16), "Дмитрий", "MLOps Engineer"),
        ((base_day + timedelta(days=2)).replace(hour=10), "Ольга", "Project Manager"),
    ]

    for starts_at, interviewer, role in slots:
        ends_at = starts_at + timedelta(hours=1)
        slot_id = create_slot(
            starts_at=starts_at.isoformat(timespec="minutes"),
            ends_at=ends_at.isoformat(timespec="minutes"),
            timezone=TIMEZONE,
            interviewer=interviewer,
            role=role,
        )
        print(f"created slot {slot_id}: {starts_at.isoformat(timespec='minutes')} {role}")


def main() -> None:
    seed_slots()


if __name__ == "__main__":
    main()
