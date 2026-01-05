from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

from utils.position import Position

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Qfree(QNAasm):
    def __init__(self, targets: list[Position]):
        self.targets = targets

    def accept(self, visitor: "Visitor"):
        visitor.visit_qfree(self)
