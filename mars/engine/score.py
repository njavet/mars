from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

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

    def prepare_exec_times(self, run: int):
        eval_docs = self.repo.get_eval_docs(run)
        model_exec_times = defaultdict(float)
        for doc in eval_docs:
            for m, t in doc.exec_times.items():
                model_exec_times[m] += t
        for m in model_exec_times:
            model_exec_times[m] /= len(eval_docs)
        dix = {}
        for model_name in sorted(model_exec_times.keys()):
            dix[model_name] = model_exec_times[model_name]
        return dix

    def prepare_metrics(self, run: int):
        models = self.filter_model_perf(run)

        model_metrics = {}
        for model_name in models.keys():
            model_metrics[model_name] = {'true_positives': 0,
                                         #'false_positives': 0,
                                         #'true_negatives': 0,
                                         'false_negatives': 0,
                                         #'prompt_alignment': 0,
                                         'irrelevant': 0}
        for model_name, scores in models.items():
            for score in scores:
                for k, v in score.items():
                    if k == 'true_positives' or k == 'false_negatives':
                        model_metrics[model_name][k] += v
                    elif k == 'irrelevant':
                        model_metrics[model_name][k] = 0

        dix = {}
        for model_name in sorted(model_metrics.keys()):
            dix[model_name] = model_metrics[model_name]
        return dix

    def create_exec_times_dia(self, run: int, dtype: str, agentic: bool = False):
        mt = self.prepare_exec_times(run)
        df = pd.DataFrame({
            'LLM': mt.keys(),
            'Seconds': mt.values()
        }).set_index('LLM')
        trunc_purples = truncated_colormap(minval=0.3)  # skip lightest 30%
        colors = trunc_purples(np.linspace(0.3, 1.0, len(df)))
        df.plot(kind='bar', legend=False, rot=0, figsize = (8, 6), color=colors)
        plt.xlabel('LLM')
        plt.xticks(rotation=30)
        plt.tight_layout(pad=1.5, rect=[0, 0, 1, 0.95])
        plt.grid(True)
        plt.ylabel('Seconds')
        if agentic:
            title = 'Agentic' + ' ' + dtype + ' ' + 'Execution Time'
            fname = 'agentic_' + dtype + 'execution_time.png'
        else:
            title = 'Baseline' + ' ' + dtype + ' ' + 'Execution Time'
            fname = 'baseline_' + dtype + 'execution_time.png'
        plt.title(title)
        plt.savefig(fname)

    def create_dia(self, run: int, dtype: str, agentic: bool = False):
        mm = self.prepare_metrics(run)
        df = pd.DataFrame(mm)
        df = df.T
        trunc_purples = truncated_colormap(minval=0.3)  # skip lightest 30%
        df.plot(kind='bar', rot=0, figsize = (8, 6), colormap=trunc_purples)
        plt.xlabel('LLM')
        plt.xticks(rotation=30)
        plt.tight_layout(pad=1.5, rect=[0, 0, 1, 0.95])
        plt.grid(True)
        plt.ylabel('Score')
        if agentic:
            title = 'Agentic' + ' ' + dtype + ' ' + 'Evaluation'
            fname = 'agentic_' + dtype + '.png'
        else:
            title = 'Baseline' + ' ' + dtype + ' ' + 'Evaluation'
            fname = 'baseline_' + dtype + '.png'
        plt.title(title)
        plt.savefig(fname)

def truncated_colormap(cmap_name='Purples', minval=0.4, maxval=1.0, n=100):
    cmap = cm.get_cmap(cmap_name)
    new_cmap = cm.colors.LinearSegmentedColormap.from_list(
        f'{cmap_name}_trunc',
        cmap(np.linspace(minval, maxval, n))
    )
    return new_cmap

