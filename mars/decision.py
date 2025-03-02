from pydantic import BaseModel


class UtilityMatrix(BaseModel):
    # D = 0, Y = 0
    u00: float
    # D = 0, Y = 1
    u01: float
    # D = 1, Y = 0
    u10: float
    # D = 1, Y = 1
    u11: float


class BinaryDecision:
    def __init__(self):
        self.u00 = None # D = 0, Y = 0
        self.u01 = None # D = 0, Y = 1
        self.u10 = None # D = 1, Y = 0
        self.u11 = None # D = 1, Y = 1
        self.p0 = None

    def set_utility_matrix(self, u00, u01, u10, u11):
        self.u00 = u00
        self.u01 = u01
        self.u10 = u10
        self.u11 = u11

    def determine_threshold(self):
        a = self.u00 - self.u10
        b = self.u00 + self.u11 - self.u01 - self.u10
        self.p0 = a / b

    def utility_expectation(self, p):
        e0 = (1 - p) * self.u00 + p * self.u01 # D = 0
        e1 = (1 - p) * self.u10 + p * self.u11 # D = 1
        return e0 + e1

    def decide(self, p):
        return 1 if p > self.p0 else 0
