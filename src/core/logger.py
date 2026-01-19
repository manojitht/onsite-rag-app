import json
import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("policy-agent")

def log_audit_event(audit_data: dict):
    """
    Writes the structured agent decision to the audit log.
    Overwrites timestamp with server time for accuracy.
    """
    try:
        audit_data["server_timestamp"] = datetime.now().isoformat()
        
        with open("logs/audit.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_data) + "\n")
            
    except Exception as e:
        print(f"FAILED TO WRITE AUDIT LOG: {e}")

