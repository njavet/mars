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


def ex2_1():
    user_prompt = 'What is 10 + 10?'              


def ex2_2():
    user_prompt = 'What is 42 + 23 + 56 + 33?'    

# 3. (hidden inside Ollama)
response = ollama.chat(
    LLAMA_MODEL,
    messages=[{'role': 'user', 'content': user_prompt}],
    tools=[add_two_numbers],  # 2. here we pass the tool to ollama
)

# 4. Here we execute the predicted tool calls
available_functions = {
    'add_two_numbers': add_two_numbers,
}
for tool in response.message.tool_calls or []:
    print(tool)
    function_to_call = available_functions.get(tool.function.name)
    if function_to_call:
        print('Function output:', function_to_call(**tool.function.arguments))
    else:
        print('Function not found:', tool.function.name)
if __name__ == '__main__':
    ex1()

