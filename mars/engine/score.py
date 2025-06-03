import matplotlib.pyplot as plt

# project imports
from mars.db.eval_repo import EvalRepository


class Score:
    def __init__(self):
        self.repo = EvalRepository()

    def create_dias(self, run: int):
        scores = self.repo.get_scores(run)
