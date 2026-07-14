import os
import json
import shutil
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_PATH = "data"
PERSIST_DIRECTORY = "chroma_db"


def load_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def load_docx(filepath):
    doc = Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])


def load_toon(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def load_documents():
    documents = []

    for filename in os.listdir(DATA_PATH):
        filepath = os.path.join(DATA_PATH, filename)

        if filename.endswith(".txt"):
            content = load_txt(filepath)
            file_type = "txt"
        elif filename.endswith(".docx"):
            content = load_docx(filepath)
            file_type = "docx"
        elif filename.endswith(".toon"):
            content = load_toon(filepath)
            file_type = "toon"
        else:
            continue

        documents.append({
            "content": content,
            "filename": filename,
            "file_type": file_type,
            "type": "initial"
        })

    return documents


def initialize_vectorstore(force_rebuild: bool = False):

    if force_rebuild and os.path.exists(PERSIST_DIRECTORY):
        shutil.rmtree(PERSIST_DIRECTORY)

    docs = load_documents()
    
    if not docs:
        return {"status": "error", "documents_indexed": 0}

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )

    # Split texts with metadata
    all_texts = []
    all_metadatas = []
    
    for doc in docs:
        split_texts = splitter.split_text(doc["content"])
        all_texts.extend(split_texts)
        
        for i, text in enumerate(split_texts):
            all_metadatas.append({
                "type": doc["type"],
                "filename": doc["filename"],
                "file_type": doc["file_type"],
                "chunk_index": i
            })

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding
    )
    
    # Add texts with metadata
    vectordb.add_texts(
        texts=all_texts,
        metadatas=all_metadatas
    )

    vectordb.persist()

    return {"status": "success", "documents_indexed": len(all_texts)}


if __name__ == "__main__":
    result = initialize_vectorstore(force_rebuild=False)
    print(f"Initialization complete: {result}")