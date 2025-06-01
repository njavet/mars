import ollama

# project imports
from mars.schema.eval import Message


def planner(text):

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

    To solve this problem, we have access to functions that 
    decide if a section is complete or not and another one that can 
    justify why a section is not complete.

    1. **is_complete(title: str, section: str):** 
    This function takes a section title and the content of the section and
    it determines if it is complete or not.
    2. **justify(decision: bool, title: str, content: str):** 
    This function takes a a section title, the content of the section and the 
    decision if it is complete or not. It returns a justification for being
    incomplete OR it returns that the section is complete.

    The document contains section headers that are markdown formatted and start
    with '##' after a newline there is some (possibly empty) text content.
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
    # llm1 = OllamaLLM(base_url='localhost:11434', model='llama3.1:8b')
    # response = llm1.chat([Message(role='user', content=llama_prompt)])
    response = ollama.chat(
        'llama3.1:8b',
        messages=[{'role': 'user', 'content': llama_prompt}],
        options={'temperature': 0.1},
        tools=[count_tokens, split_document],
    )

    available_functions = {
        'count_tokens': count_tokens,
        'split_document': split_document
    }
    sections = []
    print('LLAMA response', response.message)

    for tool in response.message.tool_calls or []:
        print('TOOL', tool)
        function_to_call = available_functions.get(tool.function.name)
        if function_to_call:
            result = function_to_call(**tool.function.arguments)
            # print('Function output:', function_to_call(**tool.function.arguments))
            print('LAMA Function output:', result)
            if tool.function.name == 'split_document':
                sections.append(result[0])  
                try:
                    sections.append(result[1])  
                except IndexError:
                    pass
        else:
            print('Function not found:', tool.function.name)

    print('LLAMA END')
    print('sections', sections)
    with open('result.md', 'w') as f:
        for i, section in enumerate(sections):
            print('section', section)
            f.write(f'\n=== Section {i+1} ===\n{section}\n')

if __name__ == '__main__':
    ex3()
