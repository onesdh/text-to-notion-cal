from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from config import GPT_API_KEY, OLLAMA_URL

def get_ollama_llm_custom(model_id, 
                          temperature,
                          top_p,
                          format_schema):
    return ChatOllama(
        base_url=OLLAMA_URL,
        model=model_id,
        reasoning=False,
        temperature=temperature,
        top_p=top_p,
        format=format_schema
    )
def get_gpt_llm_custom(model_id, 
                       temperature,
                       top_p,
                       format_schema=None):
    if not GPT_API_KEY:
        return None

    if format_schema:
        return ChatOpenAI(
            model=model_id,
            temperature=temperature,
            # top_p=top_p,
            api_key=GPT_API_KEY,
            model_kwargs={
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "format_schema", 
                        "schema": format_schema 
                    }
                }
            }
        )
    else:
        return ChatOpenAI(
            model=model_id,
            temperature=temperature,
            # top_p=top_p,
            api_key=GPT_API_KEY
        )

def llm_custom_build(model_id, temperature, top_p, format_model = None):

    if model_id.lower().startswith("gpt"):
        print(f"Using GPT model: {model_id}")
        llm_custom = get_gpt_llm_custom(model_id = model_id,
                                        temperature=temperature,
                                        top_p=top_p,
                                        format_schema=format_model)

    else :
        print(f"Using Ollama model: {model_id}")
        llm_custom = get_ollama_llm_custom(model_id = model_id,
                                        temperature=temperature,
                                        top_p=top_p,
                                        format_schema=format_model)
    return llm_custom