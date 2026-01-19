import shutil
import os
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from src.config import settings
from src.processing.ingest import ingest_document
from src.core.logger import logger

router = APIRouter()

@router.post("/ingest", summary="Upload and ingest multiple documents")
async def ingest_documents(files: List[UploadFile] = File(...)):
    """
    Ingests a list of files (PDF, TXT) into the Vector DB.
    """
    logger.info(f"Received batch ingestion request for {len(files)} files.")

    results = {
        "succeeded": [],
        "failed": [],
        "total_chunks": 0
    }

    for file in files:
        try:
            file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            num_chunks = ingest_document(file_path)
            
            results["succeeded"].append(file.filename)
            results["total_chunks"] += num_chunks
            
        except Exception as e:
            logger.error(f"Failed to ingest {file.filename}: {str(e)}")
            results["failed"].append({"filename": file.filename, "error": str(e)})
    
    logger.info(f"Batch complete. Added {results['total_chunks']} chunks.")
    
    return {
        "message": "Batch ingestion complete",
        "processed_files": len(results["succeeded"]),
        "total_chunks_added": results["total_chunks"],
        "details": results
    }


            