import os

from hr_agent_app.rag.config import HF_HOME_DIR

os.environ["HF_HOME"] = str(HF_HOME_DIR)
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from huggingface_hub import snapshot_download
from sentence_transformers import SentenceTransformer

from hr_agent_app.rag.config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    VECTORSTORE_DIR,
)


class E5HuggingFaceEmbeddings(Embeddings):
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME) -> None:
        print(f"Loading embedding model: {model_name}", flush=True)
        local_files_only = os.getenv("HF_LOCAL_FILES_ONLY", "1") == "1"
        model_path = snapshot_download(
            model_name,
            cache_dir=str(HF_HOME_DIR / "hub"),
            local_files_only=local_files_only,
            allow_patterns=[
                "config.json",
                "modules.json",
                "sentence_bert_config.json",
                "1_Pooling/config.json",
                "tokenizer.json",
                "tokenizer_config.json",
                "special_tokens_map.json",
                "sentencepiece.bpe.model",
                "model.safetensors",
            ],
        )
        self.model = SentenceTransformer(
            model_path,
            device="cpu",
            local_files_only=local_files_only,
        )
        print("Embedding model loaded.", flush=True)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        prefixed = [f"passage: {text}" for text in texts]
        return self._encode(prefixed)

    def embed_query(self, text: str) -> list[float]:
        return self._encode([f"query: {text}"])[0]

    def _encode(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embeddings.tolist()


def get_embeddings() -> E5HuggingFaceEmbeddings:
    return E5HuggingFaceEmbeddings()


def get_vectorstore(embedding_function: Embeddings | None = None) -> Chroma:
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Opening Chroma vector store: {VECTORSTORE_DIR}", flush=True)
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTORSTORE_DIR),
        embedding_function=embedding_function or get_embeddings(),
    )
