from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

from utils.position import Position

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Move(QNAasm):
    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end

    def accept(self, visitor: "Visitor"):
        visitor.visit_move(self)
