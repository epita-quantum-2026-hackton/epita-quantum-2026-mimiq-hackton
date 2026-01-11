from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

from utils.position import Position

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Qalloc(QNAasm):
    """
    Allocate qubits on the QPU grid.
    """

    def __init__(self, targets: list[Position]):
        """
        Construct a Qalloc.

        Parameters:
        - targets: positions where a qubit must be allocated.
        """
        self.targets = targets

    def accept(self, visitor: "Visitor"):
        visitor.visit_qalloc(self)
