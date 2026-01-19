from langchain_core.prompts import PromptTemplate

POLICY_LOGIC_TEMPLATE = """
Policy Precedence & Conflict Logic (RULES OF THE GAME)
Implement rules:
•	If status = DEPRECATED, down-rank by 0.6
•	If superseded_by or replaced_by exists, hard-exclude old doc
•	If query = "database encryption", system must return Doc 7 only, never Doc 8
•	If region = EMEA + production:
    o	Merge Doc 4 (global security) + Doc 5 (regional extension)
•	Environment filter:
    o	production excludes dev/staging-only docs

Intent Detection:
Classify query into:
•	SECURITY
•	COMPLIANCE
•	COST
•	AVAILABILITY
•	INCIDENT
•	IRRELEVANT
 
Routing:
•	SECURITY → boost docs with compliance_tags
•	COST → boost doc 9
•	IRRELEVANT → cafeteria/party downrank to near zero

Contradiction Detection
Example:
•	If one doc says "optional backups" (Doc 1)
•	Another says "mandatory backups" (Doc 2)
System must return:
Conflict:
Doc 1: DEPRECATED
Doc 2: CURRENT (supersedes 1)
Resolution: Doc 2 enforced


STUDENT CONTEXT (Retrieved Documents):
{context}

QUESTION:
{question}

OUTPUT FORMAT (STRICT JSON ONLY)
Generate a single valid JSON object containing both the decision logic and the final summary. Do not include markdown formatting (```json).

Required JSON Structure as Output:
{{
  "answer": "...",
  "intent": "...",
  "sources": [
    {{"id": 7, "relevance": 0.00}} //use float value for relevance eg. 0.85
  ],
  "confidence": 0.00, //use float value for confidence eg. 0.85
  "applied_filters": ["CURRENT", "production", "EMEA", "security>=confidential"],
  "conflict_resolution": {{
    "excluded": [8],
    "reason": "Superseded by 7"
  }}
}}
""" 

policy_precedence_prompt = PromptTemplate(
    template=POLICY_LOGIC_TEMPLATE,
    input_variables=["context", "question"]
)
