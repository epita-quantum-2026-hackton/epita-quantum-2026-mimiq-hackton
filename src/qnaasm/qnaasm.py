from typing import TYPE_CHECKING

from abc import ABC

if TYPE_CHECKING:
    from qnaasm.visitor import Visitor


class QNAasm(ABC):
    """
    Base class to represent QNAasm instructions.
    """

    def accept(self, visitor: "Visitor"):
        pass
