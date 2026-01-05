from typing import TYPE_CHECKING

from abc import ABC

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class QNAasm(ABC):
    def accept(self, visitor: "Visitor"):
        pass
