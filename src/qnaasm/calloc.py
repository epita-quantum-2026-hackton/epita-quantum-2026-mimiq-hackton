from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Calloc(QNAasm):
    """
    Allocate a classical register that can be used to measure qubits.
    """

    def __init__(self, name: str, size: int):
        """
        Construct a Calloc.

        Parameters:
        - name: the name of the register.
        - size: the size of the register.
        """
        self.name = name
        self.size = size

    def accept(self, visitor: "Visitor"):
        visitor.visit_calloc(self)
