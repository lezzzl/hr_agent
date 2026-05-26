INTERVIEW_STEPS = [
    {
        "field": "name",
        "question": "Как вас зовут?",
    },
    {
        "field": "target_role",
        "question": "На какую роль в ML-команде вы претендуете?",
    },
    {
        "field": "experience",
        "question": "Расскажите кратко о своём опыте работы в IT, аналитике, данных или ML.",
    },
    {
        "field": "technical_skills",
        "question": (
            "С какими техническими навыками и инструментами вы работали? "
            "Например: Python, SQL, ML, Airflow, Docker, BI, Kubernetes."
        ),
    },
    {
        "field": "previous_company",
        "question": "Где вы работали раньше и чем занимались на прошлом месте работы?",
    },
    {
        "field": "education",
        "question": (
            "Расскажите о своём образовании: вуз, направление, курсы "
            "или дополнительное обучение."
        ),
    },
    {
        "field": "city",
        "question": "В каком городе вы сейчас находитесь?",
    },
    {
        "field": "work_format",
        "question": "Какой формат работы вам подходит: офис, гибрид или удалённо?",
    },
    {
        "field": "salary_expectations",
        "question": "Какие у вас зарплатные ожидания?",
    },
]

ALLOWED_ROLES = [
    "Project Manager",
    "Data Analyst",
    "Data Engineer",
    "Data Scientist",
    "MLOps Engineer",
    "Not Suitable",
]

EMPTY_SKILLS = {
    "project_management": [],
    "data_analysis": [],
    "data_engineering": [],
    "data_science": [],
    "mlops": [],
}
