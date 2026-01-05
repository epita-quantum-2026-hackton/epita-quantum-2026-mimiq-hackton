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
    def visit_block(self, e: "Block"):
        print("{")
        super().visit_block(e)
        print("}")

    def visit_calloc(self, e: "Calloc"):
        print(f"calloc {e.name} [{e.size}]")

    def visit_conditional(self, e: "Conditional"):
        print(f"if {e.classical_register} then {{}}")

    def visit_gate(self, e: "Gate"):
        print(f"{e.name} ", end="")
        for target in e.targets[:-1]:
            print(f"{target},", end="")
        print(f"{e.targets[-1]}")

    def visit_measure(self, e: "Measure"):
        print("measure ", end="")
        for target in e.targets[:-1]:
            print(f"{target},", end="")
        print(f"{e.targets[-1]} to {e.creg}")

    def visit_move(self, e: "Move"):
        print(f"move {e.start} to {e.end}")

    def visit_qalloc(self, e: "Qalloc"):
        print("qalloc ", end="")
        for target in e.targets[:-1]:
            print(f"{target},", end="")
        print(f"{e.targets[-1]}")

    def visit_qfree(self, e: "Qfree"):
        print("qfree ", end="")
        for target in e.targets[:-1]:
            print(f"{target},", end="")
        print(f"{e.targets[-1]}")

    def visit_qnaasm(self, e: "QNAasm"):
        super().visit_qnaasm(e)
