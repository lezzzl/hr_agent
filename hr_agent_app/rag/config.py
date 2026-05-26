from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

HR_DOCS_DIR = PROJECT_ROOT / "data" / "hr_docs"
VECTORSTORE_DIR = PROJECT_ROOT / ".vectorstore" / "chroma"
HF_HOME_DIR = PROJECT_ROOT / ".cache" / "huggingface"
COLLECTION_NAME = "hr_agent_knowledge"

EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-small"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
DEFAULT_SEARCH_K = 4
