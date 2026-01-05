from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

from utils.classical_register import ClassicalRegister
from utils.position import Position

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Measure(QNAasm):
    def __init__(self, targets: list[Position], creg: ClassicalRegister):
        self.targets = targets
        self.creg = creg

    def accept(self, visitor: "Visitor"):
        visitor.visit_measure(self)
