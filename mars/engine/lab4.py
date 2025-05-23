import ollama
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig


R1_MODEL = 'deepseek-r1:7b'
LLAMA_MODEL = 'llama3.2:3b'
stack = []


def chat_ollama(messages,model,tools=None):
    response = ollama.chat(
        model=model,
        messages=messages,
        tools=tools
    )
    return response

tokenizer = AutoTokenizer.from_pretrained('teknium/OpenHermes-2.5-Mistral-7B')


def split_document(text: str, stop: int) -> tuple[str, str]:
    return text[:stop], text[stop:]


def count_tokens(doc):
    encoded = tokenizer.apply_chat_template(
        [{'role': 'user', 'content': doc}],
        add_generation_prompt=True,
        return_tensors='pt',
        truncation=True,
        max_length=4096
    )
    return encoded.shape[-1]


def ex3():
    with open('data/texts/en_missing_substanzamnese.txt') as f:
        text = f.read()
    user_prompt = 'how can the following document be split ?' + '\n' + text

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

    User query: {user_prompt}

    To solve this problem, we have access to functions that 
    counts the tokens of a tokenized text and one that splits a text
    into sections.

    1. **count_tokens(text: str):** This function takes a document text,
    tokenizes it and returns the number of tokens.
    2. **split_document(text: str, stop: int):** This function takes a document text,
    and an integer such that the document is split into 'stop' characters and
    the rest.

    Given this functions, describe a step-by-step plan 
    to split the document into sections that use less than 2024 tokens.
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
    You should blindly follow the proposed plan step-by-step. 
    Do not skip a step. 
    Do not forget to execute a step. 
    Use your tools to execute each steps.

    User query: {user_prompt}

    Plan: {plan}
    """

    response = ollama.chat(
        LLAMA_MODEL,
        messages=[{'role': 'user', 'content': llama_prompt}],
        tools=[count_tokens, split_document],
    )

    available_functions = {
        'count_tokens': count_tokens,
        'split_document': split_document
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
    ex3()
