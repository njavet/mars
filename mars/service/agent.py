# project imports
from mars.data.repo import Repository
from mars.service.lm import LanguageModel
from mars.service.rag import RAG


class Agent:
    def __init__(self, lm: LanguageModel):
        self.lm = lm
        self.rag = None

    def run_query(self,
                  enable_rag: bool,
                  preprompt: str,
                  query: str) -> str:

        if preprompt:
            if enable_rag:
                docs = self.rag.retrieve_documents(query)
                full_prompt = preprompt.format(doc_text=docs,
                                               query=query)

        if enable_rag and not preprompt:
            docs = self.rag.retrieve_documents(query)
            full_prompt = '\n'.join([docs, query])
        elif enable_rag:
        else:
            full_prompt = preprompt.format(doc_text=query)
        res = self.lm.generate(full_prompt)
        return res

    def set_rag(self, rag: RAG):
        self.rag = rag


def get_agent(base_url, lm_name, session):
    lm = LanguageModel(name=lm_name, base_url=base_url)
    agent = Agent(lm)
    repo = Repository(session=session)
    rag = RAG(repo)
    agent.set_rag(rag)
    return agent
