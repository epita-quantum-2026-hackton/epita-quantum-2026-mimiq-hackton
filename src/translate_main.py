from translate.translation import translate

from mimiqcircuits import Circuit, GateH, GateCX

from utils.position import Position

from qnaasm.pretty_printer import PrettyPrinter


c = Circuit()
c.push(GateH(), 0)
c.push(GateCX(), 0, 1)
c.push(GateCX(), 0, 2)
c.draw()

qubits = {
    0: Position(0, 0),
    1: Position(3, 0),
    2: Position(3, 3),
    3: Position(3, 1),
}

instructions = translate(c, qubits)

printer = PrettyPrinter()

for instr in instructions:
    instr.accept(printer)
