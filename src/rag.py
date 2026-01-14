# src/rag.py
from pathlib import Path
import numpy as np
import ollama
import re

# ---- Configuração ----
EMBED_MODEL = "nomic-embed-text"
BASE_DIR = Path(__file__).resolve().parents[1]
KB_DIR = BASE_DIR / "kb"
INDEX_PATH = BASE_DIR / "kb_index.npz"

# ---- Utilitários ----
def _clean_text(s: str) -> str:
    # normaliza quebras e espaços
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()

def _chunk_text(text: str, size: int = 500, overlap: int = 100):
    text = _clean_text(text)
    if len(text) <= size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0
    return chunks

def _embed(text: str) -> np.ndarray:
    res = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return np.array(res["embedding"], dtype="float32")

# ---- Indexação ----
def build_index() -> int:
    texts, metas, vecs = [], [], []

    for path in sorted(KB_DIR.glob("*.txt")):
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            raw = path.read_text(errors="ignore")
        chunks = _chunk_text(raw, size=700, overlap=120)
        for i, ch in enumerate(chunks):
            meta = {"source": str(path.name), "chunk": i}
            emb = _embed(ch)
            texts.append(ch)
            metas.append(meta)
            vecs.append(emb)

    if not vecs:
        raise RuntimeError("No .txt files found in kb/.")

    M = np.vstack(vecs).astype("float32")
    norms = np.linalg.norm(M, axis=1, keepdims=True)
    # evita divisão por zero
    norms[norms == 0] = 1.0

    np.savez_compressed(
        INDEX_PATH,
        vectors=M,
        norms=norms,
        texts=np.array(texts, dtype=object),
        sources=np.array([m["source"] for m in metas], dtype=object),
        chunks=np.array([m["chunk"] for m in metas], dtype=np.int32),
    )
    return len(texts)

def _load_index():
    if not INDEX_PATH.exists():
        raise RuntimeError("Index not found. Run build_index() first.")
    data = np.load(INDEX_PATH, allow_pickle=True)
    return (
        data["vectors"],
        data["norms"],
        data["texts"],
        data["sources"],
        data["chunks"],
    )

# ---- Busca ----
def retrieve(query: str, top_k: int = 5):
    V, Vnorms, texts, sources, chunks = _load_index()
    q = _embed(query).astype("float32")
    qnorm = np.linalg.norm(q)
    if qnorm == 0:
        qnorm = 1.0
    sims = (V @ q) / (Vnorms.squeeze() * qnorm)
    idx = np.argsort(sims)[-top_k:][::-1]

    results = []
    for i in idx.tolist():
        results.append(
            {
                "text": str(texts[i]),
                "source": str(sources[i]),
                "chunk": int(chunks[i]),
                "score": float(sims[i]),
            }
        )
    return results
