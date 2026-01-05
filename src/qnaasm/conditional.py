from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

from utils.classical_register import ClassicalRegister

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Conditional(QNAasm):
    def __init__(self, cl_reg: ClassicalRegister):
        self.classical_register = cl_reg

    def accept(self, visitor: "Visitor"):
        visitor.visit_conditional(self)
