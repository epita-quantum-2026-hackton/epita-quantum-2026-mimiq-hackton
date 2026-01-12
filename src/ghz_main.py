from translate.translation import translate

from mimiqcircuits import Circuit

from utils.position import Position

from qnaasm.pretty_printer import PrettyPrinter

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

c = Circuit.loadproto(f"{dir_path}/circuits/ghz.pb")
c.draw()

qubits = {q: Position(q, q) for q in range(c.num_qubits())}

instructions = translate(c, qubits)

printer = PrettyPrinter()

for instr in instructions:
    instr.accept(printer)
