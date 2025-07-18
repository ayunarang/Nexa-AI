import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openrouter/auto"

# Initialize the LLM once
llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=OPENROUTER_API_KEY,
    model=MODEL,
    temperature=0.3,
    max_tokens=400
)

def call_openrouter(prompt: str) -> str:
    """
    Calls OpenRouter using LangChain and returns the response content.
    """
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip() if response and response.content else "No response from model."
    except Exception as e:
        return f"Exception: {e}"
