
from typing import Annotated, Union
from typing import Union
from langchain.tools import tool
from pint import UnitRegistry



@tool
def addition(x:Annotated[Union[int, float] , "The first number to add"],
             y:Annotated[Union[int, float] , "The second number to add"]
            ) -> Union[int, float]:
    """Addition of two number"""

    return x+y

@tool
def subtraction(x:Annotated[Union[int, float] , "The first number to subtract"],
             y:Annotated[Union[int, float] , "The second number to subtract"]
            ) -> Union[int, float]:
    """Subtration of two number"""

    return x-y

@tool
def multiplication(x:Annotated[Union[int, float] , "The first number to multiply"],
             y:Annotated[Union[int, float] , "The second number to multiply"]
            ) -> Union[int, float]:
    """Multiplication of two number"""
    return x*y

@tool
def division(x:Annotated[Union[int, float] , "The first number to divide"],
             y:Annotated[Union[int, float] , "The second number to multdivideiply"]
            ) -> Union[int, float]:
    """Division of two number"""
    return x/y
    
@tool 
def unit_convert(a_number: Annotated[Union[int, float] , "The number that needs to be converted"],
             a_unit: Annotated[str, "Unit of the number that needs to be converted"],
             b_unit: Annotated[str, "Unit of the result"]) -> Union[int, float]:
    "Convert a number from unit a_unit to b_unit"
    ureg = UnitRegistry()
    return ureg.Quantity(a_number, a_unit).to(b_unit).magnitude



def init()->(list, dict):
    tools = [addition, subtraction, multiplication, division, unit_convert]
    tool_dict =  {} # this is going to be required during tool execution
    for tool in tools:
        tool_dict[tool.name]= tool
    return (tools, tool_dict)