from typing import Optional

from mimiqcircuits import (
    Circuit,
    Instruction,
    Operation,
    Measure as MimiqMeasure,
    IfStatement,
    Reset,
)

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

from qnaasm.classical_register import ClassicalRegister
from qnaasm.position import Position


def move_aside(
    m1: tuple[Position, Position], m2: Optional[tuple[Position, Position]]
) -> tuple[Position, Position]:
    current = m1[0]
    wanted = m1[1]
    if m2 is None:
        flee_from_x = wanted.x - current.x
        flee_from_y = wanted.y - current.y
        return wanted.clone(), wanted.translated(flee_from_x, flee_from_y)

    assert wanted == m2[0]
    future = m2[1]
    if current.x == future.x:
        return wanted.clone(), wanted.translated(1, 0)

    if current.y == future.y:
        return wanted.clone(), wanted.translated(0, 1)

    flee_from_x = wanted.x - future.x
    flee_from_y = wanted.y - future.y
    return wanted.clone(), wanted.translated(flee_from_x, flee_from_y)


def calculate_moves(
    q1: Position, q2: Position, qubits: dict[int, Position]
) -> list[Position]:
    positions = [q1]
    last = q1.clone()
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
        last = last.clone()

    ideal_moves = [(positions[i], positions[i + 1]) for i in range(len(positions) - 2)]
    moves = []

    for i, move in enumerate(ideal_moves):
        if move[1] in qubits.values():
            moves.append(
                move_aside(
                    move, i + 1 < len(ideal_moves) and ideal_moves[i + 1] or None
                )
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


def calculate_creg_size(c: Circuit) -> int:
    return (
        max(
            [
                max(instr.get_bits())
                for instr in c.instructions
                if isinstance(instr.get_operation(), MimiqMeasure)
            ]
        )
        + 1
    )


def translate_instruction(
    instr: Instruction, qubits: dict[int, Position]
) -> Optional[list[QNAasm]]:
    instrs = []

    used_qubits = [(q, qubits[q]) for q in instr.get_qubits()]
    operation: Operation = instr.get_operation()
    gate = str(operation)
    order = len(used_qubits)

    if isinstance(operation, MimiqMeasure):
        instrs.append(
            Measure([used_qubits[0][1]], ClassicalRegister("c", instr.get_bits()[0]))
        )

    elif isinstance(operation, Reset):
        at = used_qubits[0][1]
        instrs.extend(
            [
                Measure([at], ClassicalRegister("drop")),
                Qfree([at]),
                Qalloc([at]),
            ]
        )

    elif isinstance(operation, IfStatement):
        if_statement: IfStatement = operation
        operation: Operation = if_statement.get_operation()
        gate = str(operation)

        inner_instr = Instruction(operation, instr.get_qubits())
        res = translate_instruction(inner_instr, qubits)

        if len(res) == 1:
            res = res[0]

        else:
            res = Block(res)

        for bit, value in zip(instr.get_bits(), if_statement.get_bitstring().bits):
            res = Conditional(ClassicalRegister("c", bit), value, res)

        instrs.append(res)

    elif order == 1:
        instrs.append(Gate(gate, [used_qubits[0][1]]))

    elif order == 2:
        moves = calculate_moves(used_qubits[0][1], used_qubits[1][1], qubits)

        for p1, p2 in moves:
            instrs.append(Move(p1, p2))

        instrs.append(Gate(gate, [moves[-1][1], used_qubits[1][1]]))

        for p2, p1 in moves[::-1]:
            instrs.append(Move(p1, p2))

    else:
        return None

    return instrs


def translate(c: Circuit, qubits: dict[int, Position]) -> list[QNAasm]:
    instrs = []

    creg_size = calculate_creg_size(c)
    instrs.append(Calloc("c", creg_size))
    instrs.append(Calloc("drop", 1))

    for position in qubits.values():
        instrs.append(Qalloc([position]))

    for instr in c.instructions:
        translated_instr = translate_instruction(instr, qubits)
        if translated_instr is None:
            return []

        instrs.extend(translated_instr)

    for position in qubits.values():
        instrs.append(Qfree([position]))

    optimized_instrs = optimize(instrs)

    return optimized_instrs
