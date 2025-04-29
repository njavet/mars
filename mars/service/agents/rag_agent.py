import json
from fastapi.logger import logger

# project imports
from mars.service.agent import Agent
from mars.service.lm import LanguageModel
from mars.service.rag import RAG


class BaseRagAgent(Agent):
    def __init__(self, lm: LanguageModel, rag: RAG) -> None:
        super().__init__(lm)
        self.rag = rag

    def run_query(self, system_message: str, query: str) -> str:
        logger.info(f'[RAG Agent] Running query with {self.lm.name}')
        logger.debug(f'[RAG Agent] Query: {query}')

        docs = self.rag.retrieve_documents(query)
        logger.info(f'[RAG Agent] Retrieved docs...')
        doc_msg = '\n'.join([rag_doc.text for rag_doc in docs])
        system_message = '\n'.join([system_message, doc_msg])

        res = self.lm.chat(system_message=system_message, query=query)
        logger.debug(f'[RAG Agent] LLM response generated: {res}')
        return res


class RagAgent(BaseRagAgent):
    def __init__(self,
                 lm: LanguageModel,
                 rag: RAG,
                 judge_lm: LanguageModel,
                 max_iter: int = 3,
                 keep_top: int = 5,
                 target_score: int = 4) -> None:
        super().__init__(lm, rag)
        self.judge_lm = judge_lm
        self.max_iter = max_iter
        self.keep_top = keep_top
        self.target_score = target_score

    def _filter_docs(self, query: str, docs: list[str]) -> list[str]:
        """Ask LLM which passages matter; return best N."""
        prompt = (
            "Score each passage 0-3 for how useful it is to answer:\n"
            f"\"{query}\"\n\n"
            "Respond as JSON list of integers."
        )
        joined = "\n\n".join(
            f"[{i}] {d.replace(chr(10),' ')[:400]}" for i, d in enumerate(docs))
        scores = self.lm.chat(prompt, joined)
        kept   = [d for d, s in zip(docs, json.loads(scores)) if s >= 2]
        return kept[: self.keep_top]  # cap context size

    def _judge(self, query: str, answer: str) -> int:
        prompt = (
            "Rate the *Answer* to the *Question* 0-5.\n"
            "0 = wrong, 5 = perfect. Return **only** the integer."
        )
        text = f"Question: {query}\n\nAnswer: {answer}"
        return int(self.judge_lm.chat(prompt, text).strip())

    def run_query(self, system_message: str, query: str) -> str:
        logger.info("[RAG] query=%s", query)
        draft = ''

        for attempt in range(1, self.max_iter + 1):
            # 1) retrieve
            raw_docs = [d.text for d in self.rag.retrieve_documents(query)]
            good_docs = self._filter_docs(query, raw_docs) or raw_docs[:2]

            # 2) answer
            context = "\n".join(good_docs)
            draft   = self.lm.chat(f"{system_message}\n{context}", query)

            # 3) self-evaluate
            score = self._judge(query, draft)
            logger.debug("Attempt %d: judge=%d", attempt, score)
            if score >= self.target_score:
                return draft           # good enough 🎉

            # 4) improve (simple heuristics)
            query += " (more detail)"  # tiny re-query variation

        # after loops, return best we have
        return draft
