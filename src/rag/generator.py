from langchain_openai import ChatOpenAI
from src.config import settings
from src.rag.prompts import policy_precedence_prompt

def generate_decision(context_text: str, question: str):
    """
    Calls the LLM with the manually constructed context.
    """
    llm = ChatOpenAI(
        model_name=settings.openai_model,
        temperature=0,
        api_key=settings.OPENAI_API_KEY
    )
    
    final_prompt_value = policy_precedence_prompt.format(
        context=context_text,
        question=question 
    )
    
    response_message = llm.invoke(final_prompt_value)
    
    return response_message.content

