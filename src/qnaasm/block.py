from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Block(QNAasm):
    """
    Store multiple instructions inside a single instruction.
    """

    def __init__(self, instructions: list[QNAasm]):
        """
        Construct a Block.

        Parameters:
        - instructions: the instructions to execute inside the block.
        """
        self.instructions = instructions

    def accept(self, visitor: "Visitor"):
        visitor.visit_block(self)
