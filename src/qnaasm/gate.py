from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

from utils.position import Position

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Gate(QNAasm):
    def __init__(self, name: str, targets: list[Position]):
        self.name = name
        self.targets = targets

    def accept(self, visitor: "Visitor"):
        visitor.visit_gate(self)
