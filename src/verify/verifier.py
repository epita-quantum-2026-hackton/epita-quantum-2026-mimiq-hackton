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

import sys


class Verifier(Visitor):
    """
    A visitor to verify QNAasm instructions.
    """

    def __init__(self):
        self.cregs = {}
        self.qubits = set()
        self.error = False

    def set_error(self, msg: str):
        print(msg, file=sys.stderr)
        self.error = True

    def visit_block(self, e: "Block"):
        super().visit_block(e)

    def visit_calloc(self, e: "Calloc"):
        if e.name in self.cregs.keys():
            return self.set_error(f"creg {e.name} already allocated")

        self.cregs[e.name] = e.size

    def visit_conditional(self, e: "Conditional"):
        # For now, we consider that a conditional is valid if and only if the
        # qubits are at the same postion before and after the conditional so
        # that if we do not enter the body the grid is in the same
        # configuration as if it enters the block.
        if e.creg.name not in self.cregs.keys():
            return self.set_error(f"creg {e.creg.name} does not exist")

        size = self.cregs[e.creg.name]
        if e.creg.idx is not None:
            if not (0 <= e.creg.idx < size):
                return self.set_error(
                    f"invalid index {e.creg.idx} for register {e.creg.name} of size {size}"
                )

            if e.value > 1:
                return self.set_error(
                    "cannot use indexed access with value greater than one"
                )

        if e.creg.idx is None and (e.value >= 2**size):
            return self.set_error(
                f"invalid value {e.value} for register {e.creg.name} of size {size}"
            )

        old_cregs = self.cregs.copy()
        old_qubits = self.qubits.copy()

        e.instruction.accept(self)

        if old_cregs != self.cregs:
            self.set_error("cregs have been modified inside conditional body")

        if old_qubits != self.qubits:
            self.set_error("qubits have been modified inside conditional body")

    def visit_gate(self, e: "Gate"):
        if not e.targets:
            return self.set_error(f"missing targets for gate {e.name}")

        if len(e.targets) > 2:
            return self.set_error(f"too much targets for gate {e.name}")

        for target in e.targets:
            if target not in self.qubits:
                self.set_error(f"target {target} is not present on the grid")

        if self.error:
            return

        if len(e.targets) == 2:
            dx = e.targets[0].x - e.targets[1].x
            dy = e.targets[0].y - e.targets[1].y
            if dx**2 + dy**2 != 1:
                return self.set_error(
                    f"targets {e.targets[0]} and {e.targets[1]} are not neighbors"
                )

    def visit_measure(self, e: "Measure"):
        for target in e.targets:
            if target not in self.qubits:
                self.set_error(f"target {target} is not present on the grid")

        if self.error:
            return

        if e.creg.name not in self.cregs.keys():
            return self.set_error(f"creg {e.creg.name} does not exist")

        size = self.cregs[e.creg.name]
        ntargets = len(e.targets)
        if e.creg.idx is not None:
            if not (0 <= e.creg.idx < size):
                return self.set_error(
                    f"invalid index {e.creg.idx} for register {e.creg.name} of size {size}"
                )

            if ntargets != 1:
                return self.set_error("cannot use indexed access with multiple targets")

        if e.creg.idx is None and (ntargets != size):
            return self.set_error(
                f"invalid number of targets {ntargets} for register {e.creg.name} of size {size}"
            )

    def visit_move(self, e: "Move"):
        if e.start not in self.qubits:
            self.set_error(f"target is not present at position {e.start}")

        if e.end in self.qubits:
            self.set_error(f"qubit is already present at position {e.start}")

        if self.error:
            return

        dx = e.start.x - e.end.x
        dy = e.start.y - e.end.y
        if dx**2 + dy**2 != 1:
            return self.set_error(
                f"start position {e.start} and end position {e.end} are not neighbors"
            )

        self.qubits.remove(e.start)
        self.qubits.add(e.end.clone())

    def visit_qalloc(self, e: "Qalloc"):
        for target in e.targets:
            if target in self.qubits:
                self.set_error(f"qubit already present at position {target}")
                continue

            self.qubits.add(target.clone())

    def visit_qfree(self, e: "Qfree"):
        for target in e.targets:
            if target not in self.qubits:
                self.set_error(f"target {target} is not present on the grid")
                continue

            self.qubits.remove(target)

    def visit_qnaasm(self, e: "QNAasm"):
        super().visit_qnaasm(e)
