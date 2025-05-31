from fastapi.logger import logger
import json

# project imports
from mars.engine.llm.ollama_llm import OllamaLLM


class Agent:
    def __init__(self,
                 base_url: str,
                 lm_name: str):
        self.lm = LanguageModel(name=lm_name, base_url=base_url)
        self.judge_lm = LanguageModel(name=lm_name, base_url=base_url)
        self.max_iter: int = 3
        self.keep_top: int = 5
        self.target_score: int = 4

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
        logger.info(f'[RAG Agent] Running query with {self.lm.name}')
        draft = ''

        for attempt in range(1, self.max_iter + 1):
            logger.info(f'[RAG Agent] attempt {attempt}')
            # 1) retrieve
            raw_docs = [d.text for d in self.rag.retrieve_documents(query)]
            good_docs = self._filter_docs(query, raw_docs) or raw_docs[:2]

            # 2) answer
            context = "\n".join(good_docs)
            draft   = self.lm.chat(f"{system_message}\n{context}", query)

            # 3) self-evaluate
            score = self._judge(query, draft)
            logger.info("Attempt %d: judge=%d", attempt, score)
            if score >= self.target_score:
                return draft           # good enough 🎉

            # 4) improve (simple heuristics)
            query += " (more detail)"

        # after loops, return best we have
        return draft
