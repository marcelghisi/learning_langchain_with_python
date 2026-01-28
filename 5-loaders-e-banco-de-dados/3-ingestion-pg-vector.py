import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document

load_dotenv()

for k in ("PGVECTOR_URL", "OPENAI_API_KEY"):
    if not os.getenv(k):
        raise ValueError(f"{k} não configurado")

pdf_path = Path("/Users/marcel.ghisi/Projects/Cursos/Fullcycle/LivrosReferencias/Livro_FullCycle-12.pdf")

if not pdf_path.exists():
    raise FileNotFoundError(f"Arquivo {pdf_path} não encontrado")   

# Carregar documentos
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150,add_start_index=False).split_documents(docs)
if not text_splitter:
    raise ValueError("Não foi possível dividir o documento")

enriched_docs = [
    Document(
        page_content=doc.page_content,
        metadata={k: v for k, v in doc.metadata.items() if v not in ("", None)}
    ) for doc in text_splitter
]

ids = [f"doc-{doc}" for doc in range(len(enriched_docs))]

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = PGVector(
    embeddings=embeddings,
    connection=os.getenv("PGVECTOR_URL"),
    collection_name=os.getenv("PGVECTOR_COLLECTION"),
    use_jsonb=True
)

vector_store.add_documents(enriched_docs, ids=ids)