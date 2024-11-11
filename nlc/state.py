
from typing import Annotated, TypedDict
from typing import List
import operator

class StrategyAgentState(TypedDict):
    user_query: str
    steps: Annotated[List, operator.add]
    step_no: int
    results: dict
    final_response: str
    end:bool
