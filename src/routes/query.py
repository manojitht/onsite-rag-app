import uuid
import time
from fastapi import APIRouter, HTTPException
from src.schemas.query import QueryRequest, QueryResponse
from src.rag.retriever import retrieve_documents
from src.rag.generator import generate_decision
from src.core.logger import log_audit_event, logger
from src.utils.parser import parse_agent_response

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def reasoning(request: QueryRequest):
    try:
        trace_id = str(uuid.uuid4())
        logger.info(f"Processing Request {trace_id}: {request.question}")
        
        evidence_list = retrieve_documents(request.question)

        if evidence_list:
            logger.info(f"Retrieved {len(evidence_list)} documents for Request {trace_id}.")
            for score in evidence_list:
                computed_confidence = 0.4 * score['score']
                if computed_confidence < 0.7:
                    score['confidence'] = "Insufficient policy certainty"


        context_str = "\n\n".join(
            [f"[Source: {doc['source_id']}]\n{doc['content']}" for doc in evidence_list]
        )
        
        raw_llm_output = generate_decision(context_text=context_str, question=request.question)
        
        agent_data = parse_agent_response(raw_llm_output)
        
        agent_data["trace_id"] = trace_id
        agent_data["actor"] = "api_user"
        agent_data["processing_time"] = time.time()

        log_audit_event(agent_data)

        return QueryResponse(
            answer=agent_data.get("answer", "No Answer"),
            intent=agent_data.get("intent", "UNKNOWN"),
            sources=agent_data.get("sources", []),
            confidence=agent_data.get("confidence", 0.0),
            applied_filters=agent_data.get("applied_filters", []),
            conflict_resolution=agent_data.get("conflict_resolution", None)
        )
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
