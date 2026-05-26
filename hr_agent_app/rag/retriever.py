from langchain_core.documents import Document

from hr_agent_app.rag.config import DEFAULT_SEARCH_K, VECTORSTORE_DIR
from hr_agent_app.rag.hyde import build_hyde_query
from hr_agent_app.rag.vectorstore import get_vectorstore


def search_hr_knowledge(query: str, k: int = DEFAULT_SEARCH_K) -> list[Document]:
    if not VECTORSTORE_DIR.exists():
        raise FileNotFoundError(
            "Vector store is not initialized. Run: python -m hr_agent_app.rag.ingest"
        )

    vectorstore = get_vectorstore()
    return vectorstore.similarity_search(query, k=k)


def search_hr_knowledge_hyde(query: str, k: int = DEFAULT_SEARCH_K) -> list[Document]:
    try:
        expanded_query = build_hyde_query(query)
    except Exception:
        expanded_query = query

    return search_hr_knowledge(expanded_query, k=k)


def format_documents(documents: list[Document]) -> str:
    if not documents:
        return "В базе знаний не найдено релевантных фрагментов."

    parts = []
    for index, document in enumerate(documents, start=1):
        source = document.metadata.get("source", "unknown")
        content = document.page_content.strip()
        parts.append(f"[{index}] Источник: {source}\nФрагмент:\n{content}")

    return "\n\n".join(parts)
