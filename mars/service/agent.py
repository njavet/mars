# project imports
from mars.data.repo import Repository
from mars.service.lm import LanguageModel
from mars.service.rag import RAG


class Agent:
    def __init__(self, lm: LanguageModel):
        self.lm = lm
        self.rag = None

    def run_query(self, query: str, preprompt: str) -> str:
        if not preprompt:
            preprompt = f'{query}'
            full_prompt = query

        if self.rag and preprompt:
            docs = self.rag.retrieve_documents(query)
            full_prompt = preprompt.format(doc_text=docs,
                                           query=query)
        else:
            full_prompt = preprompt.format(doc_text=query)
        res = self.lm.generate(full_prompt)
        print('res', res)
        return res

    def set_rag(self, rag: RAG):
        self.rag = rag


def get_agent(base_url, lm_name, enable_rag, session):
    lm = LanguageModel(name=lm_name, base_url=base_url)
    agent = Agent(lm)
    if enable_rag:
        repo = Repository(session=session)
        rag = RAG(repo)
        agent.set_rag(rag)
    return agent
