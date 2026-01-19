from translate.surface_code_mapping import create_all_surface_code_mapping_for_circuit
from translate.translation import translate

from mimiqcircuits import Circuit

from qnaasm.pretty_printer import PrettyPrinter

from verify.verification import verify

import sys


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <circuit-corrected.pb>", file=sys.stderr)
    sys.exit(1)

file = sys.argv[1]

c = Circuit.loadproto(sys.argv[1])

print(" * Mapping surface codes", file=sys.stderr)
qubits = create_all_surface_code_mapping_for_circuit(c)
print("\n======== Surface Code qubits mapping =======", file=sys.stderr)
for qubit, pos in qubits.items():
    print(f"  {qubit}: {pos}", file=sys.stderr)
print("============================================", file=sys.stderr)

print(" * Translating instructions", file=sys.stderr)
instructions = translate(c, qubits)

print(" * Verifying circuit", file=sys.stderr)
if verify(instructions):
    print("-> Circuit is valid", file=sys.stderr)

else:
    print("-> Circuit is not valid", file=sys.stderr)

printer = PrettyPrinter()

for instr in instructions:
    instr.accept(printer)
