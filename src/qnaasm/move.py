from qnaasm.qnaasm import QNAasm

from utils.position import Position


class Move(QNAasm):
    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end
