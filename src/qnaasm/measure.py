from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

from utils.classical_register import ClassicalRegister
from utils.position import Position

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Measure(QNAasm):
    """
    Perform a measure on qubits inside a classical register.
    """

    def __init__(self, targets: list[Position], creg: ClassicalRegister):
        """
        Construct a Measure.

        Parameters:
        - targets: positions of the qubits to measure.
        - creg: the classical register inside which to store the result of the measure.
        """
        self.targets = targets
        self.creg = creg

    def accept(self, visitor: "Visitor"):
        visitor.visit_measure(self)
