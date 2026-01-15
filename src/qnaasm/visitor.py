from typing import TYPE_CHECKING

from abc import ABC

if TYPE_CHECKING:
    from qnaasm.block import Block
    from qnaasm.calloc import Calloc
    from qnaasm.conditional import Conditional
    from qnaasm.gate import Gate
    from qnaasm.measure import Measure
    from qnaasm.move import Move
    from qnaasm.qalloc import Qalloc
    from qnaasm.qfree import Qfree
    from qnaasm.qnaasm import QNAasm


class Visitor(ABC):
    """
    Base class to implement a visitor design pattern on QNAasm instructions.
    """

    def visit_block(self, e: "Block"):
        for instruction in e.instructions:
            instruction.accept(self)

    def visit_calloc(self, e: "Calloc"):
        pass

    def visit_conditional(self, e: "Conditional"):
        pass

    def visit_gate(self, e: "Gate"):
        pass

    def visit_measure(self, e: "Measure"):
        pass

    def visit_move(self, e: "Move"):
        pass

    def visit_qalloc(self, e: "Qalloc"):
        pass

    def visit_qfree(self, e: "Qfree"):
        pass

    def visit_qnaasm(self, e: "QNAasm"):
        e.accept(self)
