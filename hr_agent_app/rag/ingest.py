import shutil

from hr_agent_app.rag.config import VECTORSTORE_DIR
from hr_agent_app.rag.loader import load_hr_documents
from hr_agent_app.rag.splitter import split_documents
from hr_agent_app.rag.vectorstore import get_vectorstore


def ingest(reset: bool = True) -> None:
    if reset and VECTORSTORE_DIR.exists():
        print(f"Removing existing vector store: {VECTORSTORE_DIR}", flush=True)
        shutil.rmtree(VECTORSTORE_DIR)

    print("Loading HR documents...", flush=True)
    documents = load_hr_documents()
    print(f"Loaded documents: {len(documents)}", flush=True)

    print("Splitting documents...", flush=True)
    chunks = split_documents(documents)
    print(f"Created chunks: {len(chunks)}", flush=True)

    if not chunks:
        raise RuntimeError("No HR document chunks found to ingest.")

    print("Indexing chunks...", flush=True)
    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)

    print(f"Indexed chunks: {len(chunks)}", flush=True)
    print(f"Vector store: {VECTORSTORE_DIR}", flush=True)


def main() -> None:
    ingest()


if __name__ == "__main__":
    main()
