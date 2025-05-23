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


def add_two_numbers(a: int, b: int) -> int:
    return int(a) + int(b)


def ex2_0():
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
    

if __name__ == '__main__':
    lst = []
    for i in range(10):
        dix = ex2_0()
        lst.append(dix)

    for item in lst:
        for k, v in item.items():
            print('key', k)
            print('v', v)


