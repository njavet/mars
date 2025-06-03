import ollama
from rich.console import Console

# project imports
from mars.core.prompts import baseline
from mars.schema.eval import Message
console = Console()

binary = """
Du bist ein Evaluator für medizinische Austrittsberichte einer Psychiatrie.
Prüfe den Abschnitt auf fehlende medizinische Informationen und gib
nur '1' wenn der Abschnitt medizinisch vollständig ist oder '0' wenn nicht aus.
"""


justification = """
Du bist ein Evaluator für medizinische Austrittsberichte einer Psychiatrie.
Du bekommst einen Abschnitt mit Inhalt und eine Entscheidung ob der Abschnitt
komplett ist. Wenn du denkst er sei nicht komplett, gib einen kurzen Satz 
zurueck.

"""

def planner(text):
    def is_complete(section: str, content: str) -> bool:
        console.print('iscomplete got called for', section, style='green')
        content = f'section: {section}, content: {content}\n'
        res = ollama.chat(
            'mars-executor',
            messages=[{'role': 'system', 'content': binary},
                      {'role': 'user', 'content': content}],
            options={'temperature': 0.1},
        )
        return res.message.content

    def justify(section: str, content: str, decision: bool) -> str:
        console.print('justiy for', section, style='cyan')
        content = f'Entscheidung: {decision}, section: {section}, content: {content}\n'
        res = ollama.chat(
            'mars-executor',
            messages=[{'role': 'system', 'content': justification},
                      {'role': 'user', 'content': content}],
            options={'temperature': 0.1},
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
    
    2. **justify(title: str, content: str, decision: bool):** 
    This function takes a a section title, the content of the section and the 
    decision if it is complete or not. It returns a justification for being
    incomplete OR it returns that the section is complete.
    
    The document contains section headers that are markdown formatted and start
    with '##' after a newline there is some (possibly empty) text content.
    
    Given these functions, describe a step-by-step plan to decide if the
    sections are complete.

    """
    r1_response = ollama.chat(
        'mars-planner',
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
        'mars-executor',
        messages=[{'role': 'user', 'content': llama_prompt}],
        options={'temperature': 0.1},
        tools=[is_complete, justify],
    )

    available_functions = {
        'is_complete': is_complete,
        'justify': justify,
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

