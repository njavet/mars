import ollama

# project imports
from mars.schema.eval import Message


def ex3():
    with open('data/texts/en_missing_substanzamnese.txt') as f:
        text = f.read()
    text = 'How to split this document:' + '\n\n' + text

    scenario = """
    The user is interacting with a system that can split documents.
    the system can tokenize a document and count the resulting tokens.
    The user wants to receive a split document such that each split is smaller
    than 2024 tokens.
    Use the available functions to solve this task reliably.
    
    """

    r1_prompt = f"""
    
    Scenario:
    {scenario}

    You are the planner, that plans how to solve the user query using the available functions.

    User query: {text}

    To solve this problem, we have access to functions that 
    counts the tokens of a tokenized text and one that splits a text
    into sections.

    1. **count_tokens(text: str):** This function takes a document text,
    tokenizes it and returns the number of tokens.
    2. **split_document(text: str, stop: int):** This function takes a document text,
    and an integer such that the document is split into 'stop' characters and
    the rest.
    3. After each split, check token count of the result.
    4. If any section exceeds 2023 tokens, repeat the split process on that section.
    5. Repeat until all parts are under token limit
    6. output all sections

    The document contains sections separated by a blank line. Those MUST be 
    remain intact during splitting. 
    Only split the document at section boundaries.
    Given this functions, describe a step-by-step plan 
    to split the document into sections that use less than 2024 tokens.

    """
    r1_response = ollama.chat(
        R1_MODEL,
        messages=[{'role': 'user', 'content': r1_prompt}],
    )
    plan = r1_response.message.content

    # print(f"Plan: {plan}")

    # 4.
    llama_prompt = f"""
    Scenario:
    {scenario}

    You are the executor, that executes the plan of a smarter model.
    You should blindly follow the proposed plan step-by-step. 
    When calling split_document(text: str, stop: int) you ALWAYS must input
    the whole text, not just a placeholder.
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
        LLAMA_MODEL,
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
