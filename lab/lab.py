import ollama


R1_MODEL = 'deepseek-r1:7b'
LLAMA_MODEL = 'llama3.2:3b'


def chat_ollama(messages,model,tools=None):
    response = ollama.chat(
        model=model,
        messages=messages,
        tools=tools
    )
    return response


def ex1():
    logic_prompt = """
    lets define A and B as two variables from the propositional logic calculus.
    can you prove that 'A -> B' <==> '~A OR B' ?
    """


    logic_message = [{'role': 'user', 'content': logic_prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('r1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('llama', lama_res.message.content)


def add_two_numbers(a: int, b: int) -> int:
    return int(a) + int(b)


def ex2():
    user_prompt = 'What is 10 + 10?'              
    user_prompt = 'What is 42 + 23 + 56 + 33?'    
    response = ollama.chat(
        LLAMA_MODEL,
        messages=[{'role': 'user', 'content': user_prompt}],
        tools=[add_two_numbers],  
    )

    # 4. Here we execute the predicted tool calls
    available_functions = {
        'add_two_numbers': add_two_numbers,
    }
    dix = {}
    for tool in response.message.tool_calls or []:
        print(tool)
        function_to_call = available_functions.get(tool.function.name)
        if function_to_call:
            r = function_to_call(**tool.function.arguments)
            dix[str(tool)] = r
            print('Function output:', function_to_call(**tool.function.arguments))
        else:
            dix[str(tool)] = 'function not found:' + ' ' + tool.function.name
            print('Function not found:', tool.function.name)
    return dix
    

stack = []


def sum_stack():
    sum = 0.0
    while len(stack) > 0:
      sum += int(stack.pop())
    return sum


def put_on_stack(a: int):
    stack.append(a)
    return


def ex3():
    user_prompt = "What is 42 + 23 + 56 + 33?"

    scenario = """
    The user is interacting with a system that can perform calculations using a stack-based approach.
    The system has two primary functions: 'put_on_stack' which adds a number to a temporary memory stack, and 'sum_stack' which calculates the sum of all numbers currently on the stack and then clears the stack.
    The user wants to find the total of a series of numbers.
    Use the available functions to solve this task reliably.
    """

    r1_prompt = f"""
    Scenario:
    {scenario}

    You are the planner, that plans how to solve the user query using the available functions.

    User query: {user_prompt}

    To solve this problem, we have access to two functions that operate on a stack data structure:

    1.  **put_on_stack(value: int):** This function takes an integer as input and adds it to the top of the stack.

    2.  **sum_stack():** This function calculates and returns the sum of all integer values currently present on the stack. Importantly, after calculating the sum, this function will empty the stack.

    Given these functions, describe a step-by-step plan to calculate the sum of the user query.
    """
    r1_response = ollama.chat(
        R1_MODEL,
        messages=[{'role': 'user', 'content': r1_prompt}],
    )
    plan = r1_response.message.content

    print(f"Plan: {plan}")

    # 4.
    llama_prompt = f"""
    Scenario:
    {scenario}

    You are the executer, that executes the plan of a smarter model.
    You should blindly follow the proposed plan step-by-step. Do not skip a step. Do not forget to execute a step. Use your tools to execute each steps.

    User query: {user_prompt}

    Plan: {plan}
    """

    response = ollama.chat(
        LLAMA_MODEL,
        messages=[{'role': 'user', 'content': llama_prompt}],
        tools=[put_on_stack, sum_stack],  # 2. here we pass the tool to Ollama
    )

    available_functions = {
        'sum_stack': sum_stack,
        'put_on_stack': put_on_stack,
    }
    print(response.message)
    for tool in response.message.tool_calls or []:
        print(tool)
        function_to_call = available_functions.get(tool.function.name)
        if function_to_call:
            print('Function output:', function_to_call(**tool.function.arguments))
        else:
            print('Function not found:', tool.function.name)


if __name__ == '__main__':
    dix = ex3()

