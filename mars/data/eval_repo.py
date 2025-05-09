from pathlib import Path
from tinydb import TinyDB, Query

# project imports
from mars.conf.conf import RESULT_DB_URL


class EvalRepository:
    def __init__(self, db_path: Path = RESULT_DB_URL):
        self.db = TinyDB(db_path)
        self.runs = self.db.table('runs')

    def get_latest_run(self):
        return len(self.runs.all())
