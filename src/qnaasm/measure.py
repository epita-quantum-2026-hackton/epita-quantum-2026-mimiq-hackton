from qnaasm import QNAasm

from utils.classical_register import ClassicalRegister
from utils.position import Position


class Measure(QNAasm):
    def __init__(self, targets: list[Position], creg: ClassicalRegister):
        self.targets = targets
        self.creg = creg
