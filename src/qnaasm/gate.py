from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm
from qnaasm.position import Position

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Gate(QNAasm):
    """
    Represent a gate that can accept one or multiple qubits.
    """

    def __init__(self, name: str, targets: list[Position]):
        """
        Construct a Gate.

        Parameters:
        - name: the name of the gate.
        - targets: the positions of the qubits on which to apply the gate.
        """
        self.name = name
        self.targets = targets

    def accept(self, visitor: "Visitor"):
        visitor.visit_gate(self)
