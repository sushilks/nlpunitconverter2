
from nlc.state import StrategyAgentState


class NLCToolMgr:
    def __init__(self, tool_dict, debug = False):
        self.tool_dict = tool_dict
        self.DEBUG = debug

    def __call__(self, state: StrategyAgentState):
        """ Worker node that executes the tools of a given plan. Plan is json arguments
        which can be sent to tools directly"""
        #if self.DEBUG:
        #    print("--TOOL::>", state)
            
        steps = state["steps"]
        step_no = state["step_no"] or 0
        _results = state["results"] or {}
        j=0
        for tool in steps[step_no: ]:
            tool_name = tool['type']
            args = tool["args"]
            res = self.tool_dict[tool_name].invoke(args)
            _results[tool_name+"_step_"+str(step_no+j)] = res
            if self.DEBUG:
                print(f"\tstep[{step_no+j}] ::: {tool_name} is called with arguments {args} and got result {res}")
            j=j+1

        return {"results": _results, "step_no": step_no+j, }

