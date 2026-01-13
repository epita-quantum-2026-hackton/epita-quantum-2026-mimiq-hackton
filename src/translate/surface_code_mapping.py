from mimiqcircuits import Circuit

from qnaasm.position import Position

from math import ceil, sqrt


def create_surface_code_mapping(qubit: int, position: Position) -> dict[int, Position]:
    return {
        qubit: position.clone(),
        qubit + 1: position.translated(-2, 0),
        qubit + 2: position.translated(-4, 0),
        qubit + 3: position.translated(0, 2),
        qubit + 4: position.translated(-2, 2),
        qubit + 5: position.translated(-4, 2),
        qubit + 6: position.translated(0, 4),
        qubit + 7: position.translated(-2, 4),
        qubit + 8: position.translated(-4, 4),
        qubit + 9: position.translated(-1, 1),
        qubit + 10: position.translated(-3, 3),
        qubit + 11: position.translated(-3, -1),
        qubit + 12: position.translated(-1, 5),
        qubit + 13: position.translated(-3, 1),
        qubit + 14: position.translated(-1, 3),
        qubit + 15: position.translated(1, 1),
        qubit + 16: position.translated(-5, 3),
    }


def create_all_surface_code_mapping(qubits_count: int) -> dict[int, Position]:
    logical_qubits_count = qubits_count // 17
    square_size = ceil(sqrt(logical_qubits_count))

    res = {}
    for qubit in range(logical_qubits_count):
        x = qubit % square_size
        y = qubit // square_size
        res |= create_surface_code_mapping(qubit * 17, Position(x * 8 + 6, y * 8 + 6))

    return res


def create_all_surface_code_mapping_for_circuit(c: Circuit) -> dict[int, Position]:
    return create_all_surface_code_mapping(c.num_qubits())
