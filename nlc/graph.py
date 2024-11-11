from langgraph.graph import StateGraph, END
from urllib.request import urlopen

from nlc.state import StrategyAgentState
from nlc.planner import NLCPlanner
from nlc.responder import NLCResponder
from nlc.toolmgr import NLCToolMgr
from nlc import nlcllm, nlctools


def route(state:StrategyAgentState):
    """A conditional route based on number of steps completed or end anounced by any other node,
    this will either end the execution or will be sent to tools for planning"""
    steps = state["steps"]
    step_no = state["step_no"]
    end = state["end"]
    if end:
        # We have executed all tasks
        return "respond"
    else:
        # We are still executing tasks, loop back to the "tool" node
        return "plan"

def getpintdoc()->str:
    target_url="https://raw.githubusercontent.com/hgrecco/pint/refs/heads/master/pint/default_en.txt"
    html = urlopen(target_url).read()
    return html.decode('utf-8')


def init(modelType: nlcllm.ModelType, modelName: str = "gemini-1.5-pro", debug: bool = False, tool_call_log: bool = False): 
    graph = StateGraph(StrategyAgentState)
    llm = nlcllm.init(modelType, modelName)
    pintdoc = getpintdoc()
    (tools, tools_dict) = nlctools.init()

    plan = NLCPlanner(llm = llm, pintdoc=pintdoc, tools=tools, debug=debug)
    graph.add_node("plan", plan)
    tool_execution = NLCToolMgr(tool_dict=tools_dict, debug=tool_call_log)
    graph.add_node("tool_execution", tool_execution)
    responder = NLCResponder(llm = llm, debug=debug)
    graph.add_node("responder", responder)
    #--------------------------------------------------------
    graph.add_edge("plan", "tool_execution")
    graph.add_edge("responder", END)
    graph.add_conditional_edges("tool_execution", route, {"respond":"responder", "plan":"plan"})
    graph.set_entry_point("plan")
    agent = graph.compile()
    return agent