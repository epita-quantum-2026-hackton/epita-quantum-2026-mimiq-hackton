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
    while last != q2:
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

    ideal_moves = [(positions[i], positions[i + 1]) for i in range(len(positions) - 2)]
    moves = []

    for i, move in enumerate(ideal_moves):
        if move[1] in qubits.values():
            moves.append(
                move_aside(move, i < len(ideal_moves) and ideal_moves[i] or None)
            )
        moves.append(move)

    return moves


def remove_useless_moves(instructions: list[QNAasm], idx: int) -> list[QNAasm]:
    current: Move = instructions[idx]
    next: Move = instructions[idx + 1]

    if current.start == next.end and current.end == next.start:
        return instructions[:idx] + instructions[idx + 2 :], max(0, idx - 1)

    return instructions, idx + 1


def optimize(instructions: list[QNAasm]) -> list[QNAasm]:
    idx = 0
    while idx < len(instructions):
        current = instructions[idx]
        if isinstance(current, Move):
            if idx + 1 >= len(instructions):
                idx += 1
                continue

            next = instructions[idx + 1]
            if not isinstance(next, Move):
                idx += 1
                continue

            instructions, idx = remove_useless_moves(instructions, idx)

        else:
            idx += 1

    return instructions


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

    optimized_instrs = optimize(instrs)

    return optimized_instrs
