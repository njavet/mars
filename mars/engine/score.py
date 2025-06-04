from collections import defaultdict
import pandas as pd
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
                                         'false_negatives': 0,
                                         'irrelevant': 0}
        for model_name, scores in models.items():
            for score in scores:
                for k, v in score.items():
                    model_metrics[model_name][k] += v
        return model_metrics

    def create_dia(self, run: int, dtype: str):
        mm = self.prepare_metrics(run)
        df = pd.DataFrame(mm)
        df = df.T
        df.plot(kind='bar', rot=0, figsize = (8, 10))
        plt.xlabel('LLM')
        plt.xticks(rotation=30)
        plt.ylabel('Score')
        title = 'Baseline' + ' ' + dtype + ' ' + 'Evaluation'
        plt.title(title)
        plt.savefig('baseline.png')
