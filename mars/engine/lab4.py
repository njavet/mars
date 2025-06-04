import ollama
from rich.console import Console

# project imports
from mars.core.prompts import baseline
from mars.schema.eval import Message
console = Console()


def planner(text):
    def is_complete(section: str, content: str) -> bool:
        console.print('iscomplete got called for', section, style='green')
        content = f'section: {section}, content: {content}\n'
        res = ollama.chat(
            'meditron:7b',
            messages=[{'role': 'user', 'content': section},
                      {'role': 'user', 'content': content}],
        )
        return res.message.content

    scenario = """
    The user is interacting with a system that can analyze medical discharge 
    reports from a psychiatry. The system can find missing parts in the 
    sections of the documents.
    Use the available functions to solve this task reliably.
    """

    r1_prompt = f"""
    Scenario:
    {scenario}

    You are the planner, that plans how to solve the user query using the available functions.

    User query: {text}

    To solve this problem, we have access to a function that 
    decide if a section is complete or not and another one that can 
    justify why a section is not complete:
    
    1. **is_complete(title: str, section: str):** 
    This function takes a section title and the content of the section and
    it determines if it is complete or not.
    
    Given these functions, describe a step-by-step plan to decide if the
    sections are complete.

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
    # response = llm1.chat([Message(role='user', content=llama_prompt)])
    response = ollama.chat(
        'llama3.1:8b',
        messages=[{'role': 'user', 'content': llama_prompt}],
        tools=[is_complete],
    )

    available_functions = {
        'is_complete': is_complete,
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
