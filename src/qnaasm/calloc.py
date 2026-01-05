from typing import TYPE_CHECKING

from qnaasm.qnaasm import QNAasm

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class Calloc(QNAasm):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def accept(self, visitor: "Visitor"):
        visitor.visit_calloc(self)
