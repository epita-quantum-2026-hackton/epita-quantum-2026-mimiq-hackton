from mimiqcircuits import Circuit, Instruction, Operation

from qnaasm.nodes import (
    Block,
    Calloc,
    Conditional,
    Gate,
    Measure,
    Move,
    Qalloc,
    Qfree,
    QNAasm,
)

from utils.position import Position


def translate(c: Circuit, qubits: dict[int, Position]) -> list[QNAasm]:
    instrs = []

    for position in qubits.values():
        instrs.append(Qalloc([position]))

    for instr in c.instructions:
        instr: Instruction
        used_qubits = [(q, qubits[q]) for q in instr.get_qubits()]
        operation: Operation = instr.get_operation()
        gate = str(operation)
        instrs.append(Gate(gate, [p for _, p in used_qubits]))

    for position in qubits.values():
        instrs.append(Qfree([position]))

    return instrs
