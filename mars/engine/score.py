from collections import defaultdict
import matplotlib.pyplot as plt

# project imports
from mars.db.eval_repo import EvalRepository


class Score:
    def __init__(self):
        self.repo = EvalRepository()

    def filter_model_perf(self, run: int):
        scores = self.repo.get_scores(run)
        models = defaultdict(list)
        for score in scores:
            models[score.model_name].append(score.scores)
        return models

    def prepare_metrics(self, run: int):
        models = self.filter_model_perf(run)

        model_metrics = {}
        for model_name in models.keys():
            model_metrics[model_name] = {'true_positives': 0,
                                         'false_positives': 0,
                                         'true_negatives': 0,
                                         'false_negatives': 0,
                                         'irrelevant': 0,
                                         'concise': 0}
        for model_name, scores in models.items():
            for score in scores:
                for k, v in score.items():
                    model_metrics[model_name][k] += v
        return model_metrics

    def create_dia(self, run: int):
        mm = self.prepare_metrics(run)
        x_axis = mm.keys()
