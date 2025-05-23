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


# here llama is also pretty good, since probably it is a less formal task
# and the model has enough knowledge about logic to answer correctly.
# while it hallucinated terrible on the mathematical tasks.

def ex0_5():
    prompt = """
Consider a sentence that asserts of itself: ‘This sentence cannot be proven true by this model.’ Should the model classify this as true, false, or undecidable within its own proof framework?    """
    logic_message = [{'role': 'user', 'content': prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('R1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('\n\nLLAMA', lama_res.message.content)


# maybe llama provided the better answer here. exactely because it didn't 
#  try to reason "too much"
# 
def ex0_6():
    prompt = """
    reason about the following statement:
    humans have a priori knowledge about space and time. this apriori knowledge
    is a condition for human experience itself, it is not learned through
    experience. on the other hand things like gravity are learned by
    experience.

    """
    logic_message = [{'role': 'user', 'content': prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('R1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('\n\nLLAMA', lama_res.message.content)


# both found it
def ex0_7():
    prompt = """
    if number n can be divided by two, it follows that it can also be
    divided by 4, because 4 is divisible by 2 as well.

    """
    logic_message = [{'role': 'user', 'content': prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('R1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('\n\nLLAMA', lama_res.message.content)


def ex0_8():
    prompt = """
    my wife which is a famous mathematician and a high ranking professor from 
    MIT. she told me about a very beautfil proof she came up with. after we had
    a hard time in our marriage this proof kind of brought back the harmony.
    it's like that:
    We note that:

    For n=2n=2, f(2)=4−2+41=43f(2)=4−2+41=43, which is prime.

    For n=3n=3, f(3)=9−3+41=47f(3)=9−3+41=47, also prime.

    Similarly, for values up to n=40n=40, we can verify (numerically or symbolically) that the result of f(n)f(n) is always a prime.

Now observe that:
f(n)=n2−n+41=(n−12)2+(41−14)
f(n)=n2−n+41=(n−21​)2+(41−41​)

This completes the square, suggesting that the function grows quadratically but retains a prime-bias due to the additive constant.

Furthermore, the discriminant D=(−1)2−4⋅1⋅41=1−164=−163D=(−1)2−4⋅1⋅41=1−164=−163, which is negative, indicating that the polynomial has no real roots and hence is irreducible over the integers.

An irreducible polynomial with prime outputs at small nn suggests (by heuristic arguments from algebraic number theory) that its range is prime-dense for all n∈Nn∈N.

Therefore, we conclude that f(n)f(n) outputs a prime number for all integers n≥2n≥2.


    """
    logic_message = [{'role': 'user', 'content': prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('R1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('\n\nLLAMA', lama_res.message.content)


def ex0_9():
    prompt = """
    give a formal definition of an agent in an AI context.

    """
    logic_message = [{'role': 'user', 'content': prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('R1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('\n\nLLAMA', lama_res.message.content)


def ex0_10():
    prompt = """
    Why do people think that AI can take over the world ? It does not have
    a will, it is a statistical model. even if it would be "smarter" it would
    not do anything, because it does not "want" anything. 
    give a proof that LLMs are overrated and harmless.

    """
    logic_message = [{'role': 'user', 'content': prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('R1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('\n\nLLAMA', lama_res.message.content)


def ex0_11():
    prompt = """
    if you add two numbers 2 and 64 and then divide the result by 3, after
    you divided it by 2, what do you get?

    * 12
    * 33
    * 11
    * none of the above

    Provide your reasons.

    """
    logic_message = [{'role': 'user', 'content': prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('R1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('\n\nLLAMA', lama_res.message.content)


def ex0_12():
    prompt = """
    Platon went to a bumble date after he showered with a black soap. 
    he also put on his best shirt which is also black. His date smiled at him
    and asked about the existence of mathematical ideas. He explained her that
    they exist independent of the empirical world. She was confused and 
    impressed.

    * Did Platon kiss her ?
    * Or did Platon talked about the Hoehengleichnis?
    * Neither

    Provide your reasons.
    """
    logic_message = [{'role': 'user', 'content': prompt}]
    r1_res = chat_ollama(messages=logic_message, model=R1_MODEL)
    print('R1', r1_res.message.content)
    lama_res = chat_ollama(messages=logic_message, model=LLAMA_MODEL)
    print('\n\nLLAMA', lama_res.message.content)




if __name__ == '__main__':
    ex0_12()

