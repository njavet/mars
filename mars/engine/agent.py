import re
import json
import ollama

# project imports
from mars.engine.llm.ollama_llm import OllamaLLM
from mars.schema.eval import Message


class Agent:
    def __init__(self, llm: OllamaLLM, messages: list[Message]):
        self.llm = llm
        self.messages = messages
        self.text = messages[1].content
        self.sections = self.extract_sections()
        self.sections_json = json.dumps(self.sections)

    def extract_sections(self) -> dict[str, str]:
        sections = {}
        for section in self.text.split('\n\n'):
            m = re.match(r'##(?: [^\n]+){1,3}\n', section + '\n')
            tlen = len(m.group(0))
            sections[m.group(0).strip()[3:]] = section[tlen:]
        return sections

    def generate_res(self) -> str:
        return planner(self.sections_json)


def analyze_section(header: str, content: str) -> dict[str, int]:
    print('I got called for ', header)
    return {header: 0}


def planner(text):
    scenario = """
    The user sends a medical discharge report in a json format.
    The system can loop through all the sections and decide if the section 
    is complete.
    Use the available functions to solve this task reliably.
    """

    r1_prompt = f"""
    Scenario:
    {scenario}

    You are the planner, that plans how to solve the user query using the 
    available functions.

    User query: {text}

    To solve this problem, we have access to a function:

    1. **analyze_section(header: str, content: str):** 

    Given this, describe a step-by-step plan to analyze the query.

    """
    r1_response = ollama.chat(
        'deepseek-r1:7b',
        messages=[{'role': 'user', 'content': r1_prompt}],
    )
    plan = r1_response.message.content

    print(f"Plan: {plan}")

    # 4.
    llama_prompt = f"""
    Scenario:
    {scenario}

    You are the executor, that executes the plan of a smarter model.
    You should blindly follow the proposed plan step-by-step. 
    Do not skip a step. 
    Do not forget to execute a step. 
    Use your tools to execute each steps.

    User query: {text}

    Plan: {plan}
    """

    print('LLAMA START')
    response = ollama.chat(
        'llama3.1:8b',
        messages=[{'role': 'user', 'content': llama_prompt}],
        tools=[analyze_section],
    )

    available_functions = {
        'analyze_section': analyze_section,
    }
    print('LLAMA response', response.message)

    for tool in response.message.tool_calls or []:
        print('TOOL', tool)
        function_to_call = available_functions.get(tool.function.name)
        if function_to_call:
            result = function_to_call(**tool.function.arguments)
            # print('Function output:', function_to_call(**tool.function.arguments))
            print('LAMA Function output:', result)
        else:
            print('Function not found:', tool.function.name)

    print('LLAMA END')
    return response.message.content
