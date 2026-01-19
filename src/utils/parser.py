import json
import re

def parse_agent_response(full_text: str):
    """
    Parses the single JSON output from the LLM.
    """
    try:
        json_str = re.sub(r'```json', '', full_text)
        json_str = re.sub(r'```', '', json_str).strip()
        
        data = json.loads(json_str)
        return data
        
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        return {
            "answer": "PARSING_ERROR",
            "sources": [],
            "confidence": 0.0,
            "applied_filters": [],
            "conflict_resolution": None
        }


