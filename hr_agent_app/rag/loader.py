from pathlib import Path

from langchain_core.documents import Document

from hr_agent_app.rag.config import HR_DOCS_DIR

SUPPORTED_SUFFIXES = {".md", ".txt"}


def load_hr_documents(docs_dir: Path = HR_DOCS_DIR) -> list[Document]:
    if not docs_dir.exists():
        raise FileNotFoundError(f"HR docs directory does not exist: {docs_dir}")

    documents: list[Document] = []
    for path in sorted(docs_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue

        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": str(path.relative_to(docs_dir)),
                    "path": str(path),
                },
            )
        )

    return documents
