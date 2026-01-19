from typing import List, Dict, Any
from src.config import settings
from src.rag.vectorstore import get_vectorstore

def retrieve_documents(question: str, top_k: int = 5) -> List[Dict[str, Any]]:
    
    store = get_vectorstore()
    
    results = store.similarity_search_with_score(question, k=top_k)

    evidence = []
    for doc, score in results:
        md = doc.metadata or {}
        evidence.append({
            "source_id": md.get("source", "unknown"),
            "content": doc.page_content,
            "score": float(score)
        })
        
    return evidence

#sample eveidence_list structure
# evidence_list = [
#     {
#         "source_id": "source1",
#         "content": "document content",
#         "score": 0.8
#     },
#     {
#         "source_id": "source2",
#         "content": "document content",
#         "score": 0.7
#     }
# ]