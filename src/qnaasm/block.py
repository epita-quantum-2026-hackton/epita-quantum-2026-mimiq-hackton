from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Block(QNAasm):
    def __init__(self, instructions: list[QNAasm]):
        self.instructions = instructions

    def accept(self, visitor: "Visitor"):
        visitor.visit_block(self)
