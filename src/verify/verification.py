from verify.verifier import Verifier

from qnaasm.nodes import QNAasm


def verify(instructions: list[QNAasm]) -> bool:
    """
    Check that a QNAasm circuit can be executed in nearest neighbors.

    Parameters:
    - instructions: all the instructions thaat compose the circuit.
    """
    verifier = Verifier()

    for instr in instructions:
        instr.accept(verifier)

    if verifier.qubits:
        verifier.set_error(
            "all qubits have not been deallocated at the end of the circuit"
        )

    return not verifier.error
