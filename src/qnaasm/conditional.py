from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

from utils.classical_register import ClassicalRegister

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Conditional(QNAasm):
    """
    Execute an instruction whether the value of a classical register matches a given value.
    """

    def __init__(self, creg: ClassicalRegister, value: int, instruction: QNAasm):
        """
        Construct a Conditional.

        Parameters:
        - creg: the classical register to test.
        - value: the value to match the register against.
        - instruction: the instruction to execute on match.
        """
        self.creg = creg
        self.value = value
        self.instruction = instruction

    def accept(self, visitor: "Visitor"):
        visitor.visit_conditional(self)
