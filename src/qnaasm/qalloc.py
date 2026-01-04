from qnaasm import QNAasm

from utils.position import Position


class Qalloc(QNAasm):
    def __init__(self, targets: list[Position]):
        self.targets = targets
