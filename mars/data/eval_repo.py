from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

# project imports
from mars.data.tables import EvalDocTable, EvalScoreTable


class EvalRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_latest_run(self):
        stmt = select(func.max(EvalDocTable.run))
        result = self.session.execute(stmt).scalar_one_or_none()
        if result is None:
            result = 0
        return result

    def get_eval(self, run):
        stmt = (select(EvalDocTable)
                .where(EvalDocTable.run == run)
                .options(selectinload(EvalDocTable.scores)))
        results = self.session.execute(stmt).scalars().all()
        return results

    def save_eval(self, eval_doc):
        self.session.add(eval_doc)
        self.session.commit()
