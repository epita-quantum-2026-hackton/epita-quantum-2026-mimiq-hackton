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

from utils.classical_register import ClassicalRegister
from utils.position import Position

from qnaasm.pretty_printer import PrettyPrinter


printer = PrettyPrinter()

program = [
    Calloc("c", 2),
    Qalloc(
        [
            Position(0, 0),
            Position(0, 5),
        ]
    ),
    Gate("H", [Position(0, 0)]),
    Block(
        [Move(Position(0, i), Position(0, i + 1)) for i in range(4)],
    ),
    Gate(
        "CX",
        [
            Position(0, 4),
            Position(0, 5),
        ],
    ),
    Block(
        [Move(Position(0, i), Position(0, i - 1)) for i in range(4, 0, -1)],
    ),
    Measure(
        [
            Position(0, 0),
            Position(0, 5),
        ],
        ClassicalRegister("c"),
    ),
    Qfree(
        [
            Position(0, 0),
            Position(0, 5),
        ]
    ),
]

for instruction in program:
    instruction.accept(printer)
