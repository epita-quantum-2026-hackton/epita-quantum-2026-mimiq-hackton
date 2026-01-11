from typing import TYPE_CHECKING

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

from qnaasm.visitor import Visitor


class PrettyPrinter(Visitor):
    def __init__(self):
        self.level = 0

    def visit_block(self, e: "Block"):
        print(' ' * self.level, "{", sep='')
        self.level += 2
        super().visit_block(e)
        self.level -= 2
        print(' ' * self.level, "}", sep='')

    def visit_calloc(self, e: "Calloc"):
        print(' ' * self.level, f"calloc {e.name}[{e.size}]", sep='')

    def visit_conditional(self, e: "Conditional"):
        print(' ' * self.level, f"if {e.creg} = {e.value} then", sep='')
        self.level += 2
        super().visit_qnaasm(e.instruction)
        self.level -= 2

    def visit_gate(self, e: "Gate"):
        print(' ' * self.level, f"gate {e.name} ", end="", sep='')
        for target in e.targets[:-1]:
            print(f"{target},", end="", sep='')
        print(f"{e.targets[-1]}", sep='')

    def visit_measure(self, e: "Measure"):
        print(' ' * self.level, "measure ", end="", sep='')
        for target in e.targets[:-1]:
            print(f"{target},", end="", sep='')
        print(f"{e.targets[-1]} to {e.creg}", sep='')

    def visit_move(self, e: "Move"):
        print(' ' * self.level, f"move {e.start} to {e.end}", sep='')

    def visit_qalloc(self, e: "Qalloc"):
        print(' ' * self.level, "qalloc ", end="", sep='')
        for target in e.targets[:-1]:
            print(f"{target},", end="", sep='')
        print(f"{e.targets[-1]}", sep='')

    def visit_qfree(self, e: "Qfree"):
        print(' ' * self.level, "qfree ", end="", sep='')
        for target in e.targets[:-1]:
            print(f"{target},", end="", sep='')
        print(f"{e.targets[-1]}", sep='')

    def visit_qnaasm(self, e: "QNAasm"):
        super().visit_qnaasm(e)
