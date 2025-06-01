from fastapi.logger import logger

# project imports
from mars.schema.eval import Message
from mars.schema.req import LLMRequest
from mars.db.chat_repo import ChatRepository
from mars.engine.llm.ollama_llm import OllamaLLM
from mars.engine.parsing import parse_text_to_llm_input


def run_chat(llm_req: LLMRequest,
             username: str,
             repo: ChatRepository) -> str:

    logger.info(f'Running query with {llm_req.model_name}')
    llm = OllamaLLM(base_url=llm_req.base_url, model=llm_req.model_name)

    system_message = parse_text_to_llm_input(llm_req.system_message)
    history = repo.get_messages(username)
    if history:
        history[0].content = system_message
        history.append(Message(role='user', content=llm_req.user_message))
    else:
        history = [Message(role='system', content=system_message)]
        repo.save_chat(history, username)
    res = llm.chat(history)
    repo.append_turn(system_message, llm_req.user_message, res, username)
    logger.info(f'LLM response generated...')
    return res

