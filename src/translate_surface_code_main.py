from translate.surface_code_mapping import create_all_surface_code_mapping_for_circuit
from translate.translation import translate

from mimiqcircuits import Circuit

from qnaasm.pretty_printer import PrettyPrinter


c = Circuit.loadproto("./ghz-corrected.pb")

qubits = create_all_surface_code_mapping_for_circuit(c)
print("#" * 40)
print("# Surface Code qubits mapping.")
print("#" * 40)
for qubit, pos in qubits.items():
    print(f"# {qubit}: {pos}")
print("#" * 40)

instructions = translate(c, qubits)

printer = PrettyPrinter()

for instr in instructions:
    instr.accept(printer)
