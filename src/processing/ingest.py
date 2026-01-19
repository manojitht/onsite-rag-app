import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.rag.vectorstore import get_vectorstore
from src.config import settings
from src.core.logger import logger

def ingest_document(file_path: str):

    try:
        filename = os.path.basename(file_path)
        
        logger.info(f"[{filename}] Starting loader...")
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
            
        documents = loader.load()
        logger.info(f"[{filename}] Loaded {len(documents)} pages/documents.")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"[{filename}] Split into {len(chunks)} chunks.")
        
        if not chunks:
            logger.warning(f"[{filename}] No chunks created. File might be empty.")
            return 0
        
        logger.info(f"[{filename}] Generating embeddings and storing in ChromaDB...")
        vectorstore = get_vectorstore()
        
        for chunk in chunks:
            chunk.metadata["source"] = filename
            
        vectorstore.add_documents(chunks)
        
        logger.info(f"[{filename}] Ingestion complete.")
        
        return len(chunks)

    except Exception as e:
        logger.error(f"[{filename}] Error during processing: {str(e)}")
        raise e
    




      

    
