from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from nlc.state import StrategyAgentState
import json 

class NLCResponder:
    def __init__(self, llm: Runnable, debug = False):
        self.llm = llm
        self.DEBUG = debug
        self.model = self.get_model()

    def get_model(self):
        SYSTEM_PROMT = "Generate final response by looking at the results and original user question."
        prompt_template = ChatPromptTemplate.from_messages(
                        [("system", SYSTEM_PROMT),
                        ("user", "{user_question}"),
                        ("user", "{results}")])
        if self.DEBUG:
            print("get_model PROMPT:", prompt_template.to_json())
        return prompt_template | self.llm

    def __call__(self, state: StrategyAgentState):
        if self.DEBUG:
            print("--RESP::>", state)
        user_question = state["user_query"]
        results = state["results"]
        invoke_inputs = {"user_question": user_question, "results": json.dumps(results)}
        if self.DEBUG:
            print("REQ TO LLM-final:", invoke_inputs)    
        response = self.model.invoke(invoke_inputs)
        if self.DEBUG:
            print("Response from LLM-final:", response)
        return {"final_response": response.content}
