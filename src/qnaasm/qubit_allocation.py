from qnaasm import QNAasm

from utils.position import Position


class QubitAllocation(QNAasm):
    def __init__(self, targets: list[Position]):
        self.targets = targets
