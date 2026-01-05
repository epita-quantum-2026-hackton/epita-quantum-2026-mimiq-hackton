from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

from utils.classical_register import ClassicalRegister

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Conditional(QNAasm):
    def __init__(self, creg: ClassicalRegister, value: int, instruction: QNAasm):
        self.creg = creg
        self.value = value
        self.instruction = instruction

    def accept(self, visitor: "Visitor"):
        visitor.visit_conditional(self)
