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


def calculate_moves(q1: Position, q2: Position) -> list[Position]:
    positions = [q1]
    last = Position(q1.x, q1.y)
    while last.x != q2.x or last.y != q2.y:
        if last.x < q2.x:
            last.x += 1
        elif last.x > q2.x:
            last.x -= 1
        elif last.y < q2.y:
            last.y += 1
        else:
            last.y -= 1

        positions.append(last)
        last = Position(last.x, last.y)

    return [(positions[i], positions[i + 1]) for i in range(len(positions) - 2)]


def translate(c: Circuit, qubits: dict[int, Position]) -> list[QNAasm]:
    instrs = []

    for position in qubits.values():
        instrs.append(Qalloc([position]))

    for instr in c.instructions:
        instr: Instruction
        used_qubits = [(q, qubits[q]) for q in instr.get_qubits()]
        operation: Operation = instr.get_operation()
        gate = str(operation)
        order = len(used_qubits)

        if order == 1:
            instrs.append(Gate(gate, [used_qubits[0][1]]))

        elif order == 2:
            moves = calculate_moves(used_qubits[0][1], used_qubits[1][1])

            for p1, p2 in moves:
                instrs.append(Move(p1, p2))

            instrs.append(Gate(gate, [moves[-1][1], used_qubits[1][1]]))

            for p2, p1 in moves[::-1]:
                instrs.append(Move(p1, p2))

        else:
            return []

    for position in qubits.values():
        instrs.append(Qfree([position]))

    return instrs
