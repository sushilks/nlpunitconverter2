from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os
import getpass
from enum import Enum

class ModelType(Enum):
    OpenAI = 1
    Gemini = 2

def init(modelType: ModelType, modelName: str):
    openai=True
    if modelType == ModelType.OpenAI:
        if "OPENAI_API_KEY" not in os.environ:
            os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your openapi API key: ")
        #modelName="gpt-4o"
        #modelName="gpt-3.5-turbo"
        #modelName="o1-mini"
        llm = ChatOpenAI(model=modelName, temperature=0) # OpenAI()
    elif modelType == ModelType.Gemini:
        if "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")
        # modelName="gemini-1.5-pro"
        # modelName="gemini-1.0-pro"
        llm = ChatGoogleGenerativeAI(
            model=modelName,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )
    else:
        raise Exception(f"Sorry, Unknown Model Type {modelType}")
    return llm
    