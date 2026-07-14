from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import Session
from math import ceil
import uuid
import os
import logging
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.database import get_db
from app.models import (
    PaketWisata, HargaTiket, Hotel, TempatPenting,
    NomorPenting, Wisata, Transportasi
)
from app.schemas import QAInput, QAResponse
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/data", tags=["Data"])


def get_paginated_response(items, total, page, limit):
    """Helper function to create paginated response"""
    total_pages = ceil(total / limit) if total > 0 else 1
    return {
        "data": items,
        "meta": {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    }


# Paket Wisata Endpoints
@router.get("/paket-wisata")
def get_all_paket_wisata(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=10, description="Items per page (max 10)"),
    db: Session = Depends(get_db)
):
    """Get all paket wisata with pagination"""
    total = db.query(PaketWisata).count()
    offset = (page - 1) * limit
    
    paket_list = db.query(PaketWisata).offset(offset).limit(limit).all()
    
    return get_paginated_response(paket_list, total, page, limit)


@router.get("/paket-wisata/{paket_id}")
def get_paket_wisata_by_id(paket_id: str, db: Session = Depends(get_db)):
    """Get paket wisata by ID"""
    paket = db.query(PaketWisata).filter_by(data_id=paket_id).first()
    if not paket:
        raise HTTPException(status_code=404, detail="Paket wisata not found")
    return paket


# Harga Tiket Endpoints
@router.get("/harga-tiket")
def get_all_harga_tiket(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=10, description="Items per page (max 10)"),
    db: Session = Depends(get_db)
):
    """Get all harga tiket with pagination"""
    total = db.query(HargaTiket).count()
    offset = (page - 1) * limit
    
    tiket_list = db.query(HargaTiket).offset(offset).limit(limit).all()
    
    items = [
        {
            "id": tiket.id,
            "group_name": tiket.group_name,
            "item_name": tiket.item_name,
            "price": tiket.price
        }
        for tiket in tiket_list
    ]
    
    return get_paginated_response(items, total, page, limit)


@router.get("/harga-tiket/{tiket_id}")
def get_harga_tiket_by_id(tiket_id: int, db: Session = Depends(get_db)):
    """Get harga tiket by ID"""
    tiket = db.query(HargaTiket).filter_by(id=tiket_id).first()
    if not tiket:
        raise HTTPException(status_code=404, detail="Harga tiket not found")
    return tiket


# Hotel Endpoints
@router.get("/hotel")
def get_all_hotel(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=10, description="Items per page (max 10)"),
    db: Session = Depends(get_db)
):
    """Get all hotel with pagination"""
    total = db.query(Hotel).count()
    offset = (page - 1) * limit
    
    hotel_list = db.query(Hotel).offset(offset).limit(limit).all()
    return get_paginated_response(hotel_list, total, page, limit)


@router.get("/hotel/{hotel_id}")
def get_hotel_by_id(hotel_id: str, db: Session = Depends(get_db)):
    """Get hotel by ID"""
    hotel = db.query(Hotel).filter_by(data_id=hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel


# Tempat Penting Endpoints
@router.get("/tempat-penting")
def get_all_tempat_penting(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=10, description="Items per page (max 10)"),
    db: Session = Depends(get_db)
):
    """Get all tempat penting with pagination"""
    total = db.query(TempatPenting).count()
    offset = (page - 1) * limit
    
    tempat_list = db.query(TempatPenting).offset(offset).limit(limit).all()
    return get_paginated_response(tempat_list, total, page, limit)


@router.get("/tempat-penting/{tempat_id}")
def get_tempat_penting_by_id(tempat_id: str, db: Session = Depends(get_db)):
    """Get tempat penting by ID"""
    tempat = db.query(TempatPenting).filter_by(data_id=tempat_id).first()
    if not tempat:
        raise HTTPException(status_code=404, detail="Tempat penting not found")
    return tempat


# Nomor Penting Endpoints
@router.get("/nomor-penting")
def get_all_nomor_penting(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=10, description="Items per page (max 10)"),
    db: Session = Depends(get_db)
):
    """Get all nomor penting with pagination"""
    total = db.query(NomorPenting).count()
    offset = (page - 1) * limit
    
    nomor_list = db.query(NomorPenting).offset(offset).limit(limit).all()
    return get_paginated_response(nomor_list, total, page, limit)


@router.get("/nomor-penting/{nomor_id}")
def get_nomor_penting_by_id(nomor_id: str, db: Session = Depends(get_db)):
    """Get nomor penting by ID"""
    nomor = db.query(NomorPenting).filter_by(data_id=nomor_id).first()
    if not nomor:
        raise HTTPException(status_code=404, detail="Nomor penting not found")
    return nomor


# Wisata Endpoints
@router.get("/wisata")
def get_all_wisata(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=10, description="Items per page (max 10)"),
    db: Session = Depends(get_db)
):
    """Get all wisata with pagination"""
    total = db.query(Wisata).count()
    offset = (page - 1) * limit
    
    wisata_list = db.query(Wisata).offset(offset).limit(limit).all()
    return get_paginated_response(wisata_list, total, page, limit)


@router.get("/wisata/{wisata_id}")
def get_wisata_by_id(wisata_id: str, db: Session = Depends(get_db)):
    """Get wisata by ID"""
    wisata = db.query(Wisata).filter_by(data_id=wisata_id).first()
    if not wisata:
        raise HTTPException(status_code=404, detail="Wisata not found")
    return wisata


# Transportasi Endpoints
@router.get("/transportasi")
def get_all_transportasi(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=10, description="Items per page (max 10)"),
    db: Session = Depends(get_db)
):
    """Get all transportasi with pagination"""
    total = db.query(Transportasi).count()
    offset = (page - 1) * limit
    
    trans_list = db.query(Transportasi).offset(offset).limit(limit).all()
    return get_paginated_response(trans_list, total, page, limit)


@router.get("/transportasi/{trans_id}")
def get_transportasi_by_id(trans_id: int, db: Session = Depends(get_db)):
    """Get transportasi by ID"""
    trans = db.query(Transportasi).filter_by(id=trans_id).first()
    if not trans:
        raise HTTPException(status_code=404, detail="Transportasi not found")
    return trans


# Vector Database Q&A Endpoints
@router.post("/qa/add", response_model=QAResponse)
def add_qa_to_vectordb(request: QAInput):
    """Add question-answer pair to vector database"""
    try:
        # Initialize embedding model
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        # Load existing vector store
        vectordb = Chroma(
            persist_directory="chroma_db",
            embedding_function=embedding
        )
        
        # Combine question and answer
        combined_text = f"Pertanyaan: {request.question}\n\nJawaban: {request.answer}"
        
        # Generate a unique ID for this document
        doc_id = str(uuid.uuid4())
        
        # Add to vector database
        ids = vectordb.add_texts(
            texts=[combined_text],
            ids=[doc_id],
            metadatas=[{
                "type": "qa",
                "question": request.question,
                "answer": request.answer
            }]
        )
        
        # Persist changes
        vectordb.persist()
        
        return QAResponse(
            message=f"Q&A pair successfully added to vector database",
            status="success",
            id=doc_id
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error adding Q&A to vector database: {str(e)}"
        )


@router.post("/qa/add-batch")
def add_batch_qa_to_vectordb(requests: list[QAInput]):
    """Add multiple question-answer pairs to vector database"""
    try:
        # Initialize embedding model
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        # Load existing vector store
        vectordb = Chroma(
            persist_directory="chroma_db",
            embedding_function=embedding
        )
        
        combined_texts = []
        doc_ids = []
        metadatas = []
        
        for req in requests:
            # Combine question and answer
            combined_text = f"Pertanyaan: {req.question}\n\nJawaban: {req.answer}"
            doc_id = str(uuid.uuid4())
            
            combined_texts.append(combined_text)
            doc_ids.append(doc_id)
            metadatas.append({
                "type": "qa",
                "question": req.question,
                "answer": req.answer
            })
        
        # Add all to vector database
        vectordb.add_texts(
            texts=combined_texts,
            ids=doc_ids,
            metadatas=metadatas
        )
        
        # Persist changes
        vectordb.persist()
        
        return {
            "message": f"Successfully added {len(requests)} Q&A pairs to vector database",
            "status": "success",
            "count": len(requests),
            "ids": doc_ids
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error adding batch Q&A to vector database: {str(e)}"
        )


# Helper functions for file loading
def load_txt(filepath):
    """Load text from .txt file"""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def load_docx(filepath):
    """Load text from .docx file"""
    try:
        doc = Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        logger.error(f"Error loading DOCX file: {str(e)}")
        raise


def load_toon(filepath):
    """Load text from .toon file (custom format)"""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


# File Upload Endpoint
@router.post("/upload-file")
async def upload_file_to_vectordb(file: UploadFile = File(...)):
    """Upload file (txt, docx, toon) to data folder and add to vector database"""
    
    DATA_PATH = "data"
    PERSIST_DIRECTORY = "chroma_db"
    
    # Ensure data directory exists
    os.makedirs(DATA_PATH, exist_ok=True)
    
    try:
        # Validate file extension
        allowed_extensions = {".txt", ".docx", ".toon"}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save file to data folder
        file_path = os.path.join(DATA_PATH, file.filename)
        
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        logger.info(f"File saved to {file_path}")
        
        # Load content based on file type
        if file_ext == ".txt":
            content = load_txt(file_path)
        elif file_ext == ".docx":
            content = load_docx(file_path)
        elif file_ext == ".toon":
            content = load_toon(file_path)
        
        logger.info(f"Content loaded from {file.filename}, length: {len(content)}")
        
        # Split content into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=200
        )
        split_docs = splitter.split_text(content)
        
        logger.info(f"Content split into {len(split_docs)} chunks")
        
        # Initialize embedding model
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        # Load existing vector store
        vectordb = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=embedding
        )
        
        # Generate IDs and metadata for chunks
        doc_ids = [str(uuid.uuid4()) for _ in split_docs]
        metadatas = [{
            "type": "file",
            "filename": file.filename,
            "file_type": file_ext[1:],  # Remove dot
            "chunk_index": i
        } for i in range(len(split_docs))]
        
        # Add to vector database
        vectordb.add_texts(
            texts=split_docs,
            ids=doc_ids,
            metadatas=metadatas
        )
        
        # Persist changes
        vectordb.persist()
        
        logger.info(f"Added {len(split_docs)} chunks to vector database from {file.filename}")
        
        return {
            "message": f"File '{file.filename}' successfully uploaded and added to vector database",
            "status": "success",
            "filename": file.filename,
            "file_path": file_path,
            "chunks_created": len(split_docs),
            "chunk_ids": doc_ids
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}", exc_info=True)
        # Clean up file if something went wrong
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
        
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}"
        )


@router.get("/files")
def list_files():
    """List all files in data folder"""
    DATA_PATH = "data"
    
    try:
        if not os.path.exists(DATA_PATH):
            return {
                "status": "success",
                "files": [],
                "total": 0
            }
        
        files = []
        for filename in os.listdir(DATA_PATH):
            filepath = os.path.join(DATA_PATH, filename)
            if os.path.isfile(filepath):
                file_size = os.path.getsize(filepath)
                files.append({
                    "filename": filename,
                    "size": file_size,
                    "size_mb": round(file_size / (1024 * 1024), 2)
                })
        
        return {
            "status": "success",
            "files": files,
            "total": len(files)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing files: {str(e)}"
        )


@router.delete("/files/{filename}")
def delete_file(filename: str):
    """Delete file from data folder"""
    DATA_PATH = "data"
    file_path = os.path.join(DATA_PATH, filename)
    
    try:
        # Security check - prevent directory traversal
        if not os.path.abspath(file_path).startswith(os.path.abspath(DATA_PATH)):
            raise HTTPException(
                status_code=400,
                detail="Invalid filename"
            )
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail=f"File '{filename}' not found"
            )
        
        os.remove(file_path)
        logger.info(f"File deleted: {filename}")
        
        return {
            "message": f"File '{filename}' successfully deleted",
            "status": "success",
            "filename": filename
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting file: {str(e)}"
        )
