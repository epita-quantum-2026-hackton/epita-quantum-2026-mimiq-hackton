from qnaasm import QNAasm

from utils.position import Position


class Gate(QNAasm):
    def __init__(self, name: str, targets: list[Position]):
        self.name = name
        self.targets = targets
