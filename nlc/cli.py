"""This module provides the natural language convertor CLI."""
# nlc/cli.py

from typing import Annotated
from typing import Optional

import typer

from nlc import __app_name__, __version__, graph, nlcllm

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

def runquery(query, agent, verbose=True):
    final = []
    for s in agent.stream({"user_query": query, "results": {}, "end":False, "step_no":0}):
        if verbose:
            print("task ::   ", s)
        final.append(s)
        if verbose:
            print("--------------------")
    if verbose:
        print("----FINAL ANSWER----")
        print(final[-1])
        print("--------------------")
    return final


@app.command()
def process(
    input_text: Annotated[str, typer.Option("--text", "-t", help="Input query to process")],
    tool_call_log: Annotated[bool , typer.Option("-l", "--tool_call_log", help="Enable tool call logging")] = False,
    verbose: Annotated[bool , typer.Option("-v", "--verbose", help="Enable verbose logging")] = False,
    model_type: Annotated[str, typer.Option("-p", "--model_type", help="Model type [OpenAI, Gemini]")] = "OpenAI",
    model_name: Annotated[str, typer.Option("-m", "--model", 
                                            help="model name [gemini-1.5-pro, gemini-1.0-pro] or [gpt-4o,gpt-3.5-turbo] ")] = "gpt-4o",
) -> None:
    agent = graph.init(nlcllm.ModelType[model_type], model_name, verbose, tool_call_log)
    r = runquery(input_text, agent, verbose)
    print("\nResponse > ", r[-1]['responder']['final_response'])
    return 0

@app.command()
def file(
    input_file: Annotated[str, typer.Option("--file", "-f", help="Input query will be read from this file")],
    tool_call_log: Annotated[bool , typer.Option("-l", "--tool_call_log", help="Enable tool call logging")] = False,
    verbose: Annotated[bool , typer.Option("-v", "--verbose", help="Enable verbose logging")] = False,
    model_type: Annotated[str, typer.Option("-p", "--model_type", help="Model type [OpenAI, Gemini]")] = "OpenAI",
    model_name: Annotated[str, typer.Option("-m", "--model", help="model name gemini-1.5-pro, gemini-1.0-pro")] = "gpt-4o",
) -> None:
    agent = graph.init(nlcllm.ModelType[model_type], model_name, verbose, tool_call_log)
    # r = runquery(input_text, agent, verbose)
    # print("\nResponse > ", r[-1]['responder']['final_response'])
    # return 0
    file = open(input_file, "r")
    txtline = file.read().split("\n")
    for txt in txtline:
        if len(txt) == 0:
            continue
        print("Processing: ", txt)
        r = runquery(txt, agent, verbose)
        print("\nResponse > ", r[-1]['responder']['final_response'])
        print("-------------\n")
    return 0


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return