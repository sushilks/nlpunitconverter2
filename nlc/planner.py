
from typing import Annotated, TypedDict, Union, Any, Literal
from typing import List
import json
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_tools import JsonOutputToolsParser

from nlc.state import StrategyAgentState


class NLCPlanner:
    def __init__(self, llm: Runnable, pintdoc: str, tools: list, debug = False):
        self.llm = llm
        self.pintdoc = pintdoc
        self.DEBUG = debug
        self.tools = tools
        self.prePlanner = self.get_pre_planner()
        self.donePlanner = self.get_done_planner()
        self.stepPlanner = self.get_step_planner()

    def get_pre_planner(self):
        SYSTEM_PROMT = "You are a helpful assitant who is good is mathematics and can convert quntaties from one unit to another unit.\
            Do not calculate yourself let the tool do the calculation. Call one tool at a time. Here is the details of all the units that are available for conversion\n"
        SYSTEM_PROMT += self.pintdoc
        prompt_template = ChatPromptTemplate.from_messages(
                        [("system", SYSTEM_PROMT),
                        ("user", "{user_question}")])
        if self.DEBUG:
            print("Pre Planner PROMPT:", prompt_template.to_json())
        return prompt_template | self.llm.bind_tools(self.tools)| JsonOutputToolsParser()

    def get_done_planner(self):
        SYSTEM_PROMT = "You need to decide whether a problem is solved or not. Just return ##YES if propblem is solved and ##NO \
        if problem is not solved. Make sure you use same template of ##YES and ##NO in final answer.\
        Do not calculate the solution yourself let the tool do the calculation."
        prompt_template = ChatPromptTemplate.from_messages(
                        [("system", SYSTEM_PROMT),
                        ("user", "{user_question}"), 
                        ("user", "{results}"),
                        ("user", "{steps}")])
        if self.DEBUG:
            print("done Planner PROMPT:", prompt_template.to_json())
        return prompt_template | self.llm

    def get_step_planner(self):
        SYSTEM_PROMT = "You are a helpful assitant who is good is mathematicsand can convert quntaties from one unit to another unit.\
            You are replanner assistant.\
        If you are given previous steps and previous results. Do not start again. Call one function at a time.\
            Do not calculate yourself let the tool do the calculation. Here is the details of all the units that are available for conversion\n"
        SYSTEM_PROMT += self.pintdoc
        prompt_template = ChatPromptTemplate.from_messages(
                        [("system", SYSTEM_PROMT),
                        ("user", "{user_question}"), 
                        ("user", "{steps}"),
                        ("user", "{results}")])
        if self.DEBUG:
            print("Step Planner PROMPT:", prompt_template.to_json())
        return prompt_template | self.llm.bind_tools(self.tools)| JsonOutputToolsParser()


    def __call__(self, state: StrategyAgentState):
        """The planner node, this is the brain of the system"""
        if self.DEBUG:
            print("--PLAN::>", state)
        user_question = state["user_query"]
        steps = state["steps"]
        results = state["results"]
        end = state["end"]
        if results is None:  # If result has not been populated yet we will start planning 
            invoke_inputs = {"user_question": user_question}
            if self.DEBUG:
                print("REQ TO LLM1:", invoke_inputs)
            steps = self.prePlanner.invoke(invoke_inputs)
            if self.DEBUG:
                print("Response from LLM1:", steps)
            if self.DEBUG:        
                print(f"Generated plans : {steps}")

            return {'steps': steps}
        elif results and not end: # If result has been populated and end is not true we will go to end detector
            invoke_inputs = {"user_question": user_question, "steps":json.dumps(steps), "results":json.dumps(results)}
            if self.DEBUG:
                print("REQ TO LLM2:", invoke_inputs)
            response = self.donePlanner.invoke(invoke_inputs)
            if self.DEBUG:
                print("Response from LLM2:", response)
                print(f"End detector response : {response.content}")

            if  "##YES" in response.content:
                return {'end': True}

        # If not done then ask for next steps

    

        invoke_inputs = {"user_question": user_question, "steps":json.dumps(steps), "results":json.dumps(results)}
        if self.DEBUG:        
            print("REQ TO LLM3:", invoke_inputs)
        steps = self.stepPlanner.invoke(invoke_inputs)
        if self.DEBUG:
            print("Response from LLM3:", steps)
            print(f"Pending  plans : {steps}")

        return {'steps': steps, 'end': False}



