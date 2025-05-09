from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

# project imports
from mars.conf.conf import PDF_DIR
from mars.data.tables import (EvaluationDocument,
                              EvaluationResult,
                              EvaluationScore)


class EvalRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_latest_run(self):
        stmt = select(func.max(EvaluationDocument.run))
        result = self.session.execute(stmt).scalar_one_or_none()
        if result is None:
            result = 0
        return result

    def get_eval(self, run):
        stmt = (select(EvaluationDocument)
                .where(EvaluationDocument.run == run)
                .options(selectinload(EvaluationDocument.results)
                         .selectinload(EvaluationResult.scores)))
        results = self.session.execute(stmt).scalars().all()
        return results

    def save_eval(self, eval_doc, eval_results):
        self.session.add(eval_doc)
        self.session.commit()
        for result in eval_results:
            result.fk_doc = eval_doc.key
        self.session.add_all(eval_results)
        self.session.commit()
