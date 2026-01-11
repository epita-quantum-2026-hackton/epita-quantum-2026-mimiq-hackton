from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

from utils.position import Position

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Move(QNAasm):
    """
    Move a qubit from a position to another.
    """

    def __init__(self, start: Position, end: Position):
        """
        Construct a Move.

        Parameters:
        - start: the initial position of the qubit.
        - end: the new position of the qubit.
        """
        self.start = start
        self.end = end

    def accept(self, visitor: "Visitor"):
        visitor.visit_move(self)
