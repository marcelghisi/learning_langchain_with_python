from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader(file_path="/Users/marcel.ghisi/Projects/Cursos/Fullcycle/LivrosReferencias/Livro_FullCycle-12.pdf")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(docs)

for chunk in chunks:
    print(chunk.page_content)
    print("-"*100)
