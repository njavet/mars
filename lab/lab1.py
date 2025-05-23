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


def ex0_0():
    test_content = 'Explain deep learning as if I am a 10 year old, in one to two sentences.'
    test_message = [{'role': 'user', 'content': test_content}]
    r1_response = chat_ollama(messages=test_message, model=R1_MODEL)
    print('r1', r1_response.message.content)

    llama_response = chat_ollama(messages=test_message, model=LLAMA_MODEL)
    print('\n\nllama', llama_response.message.content)


def ex0_1():
    logic_prompt = """
    lets define A and B as two variables from the propositional logic calculus.
    can you prove that 'A -> B' <==> '~A OR B' ?
    """

    logic_message = [{'role': 'user', 'content': logic_prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('r1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('\n\nllama', lama_res.message.content)


def ex0_2():
    prompt = """
    given the peano axioms of the set of natural numbers. prove or prove the
    negation of the following statements:
    * There exists a number n that is larger than any other number.
    * every natural number has a unique faktorization into prime numbers.
    """
    logic_message = [{'role': 'user', 'content': prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('r1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('\n\nllama', lama_res.message.content)


def ex0_3():
    prompt = """
    given the peano axioms of the set of natural numbers. prove or prove the
    negation of the following statements and show the formal deduction of your
    proves!
    * There exists a number n that is larger than any other number.
    * every natural number has a unique faktorization into prime numbers.
    """
    logic_message = [{'role': 'user', 'content': prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('r1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('\n\nllama', lama_res.message.content)


def ex0_4():
    prompt = """
    Is the predicate logic first order decidable ?
    """
    logic_message = [{'role': 'user', 'content': prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('R1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('\n\nLLAMA', lama_res.message.content)


def ex0_5():
    prompt = """
Consider a sentence that asserts of itself: ‘This sentence cannot be proven true by this model.’ Should the model classify this as true, false, or undecidable within its own proof framework?    """
    logic_message = [{'role': 'user', 'content': prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('R1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('\n\nLLAMA', lama_res.message.content)



if __name__ == '__main__':
    ex0_5()

