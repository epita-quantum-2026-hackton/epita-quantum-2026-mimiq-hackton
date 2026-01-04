from qnaasm import QNAasm

from utils.classical_register import ClassicalRegister


class Conditional(QNAasm):
    def __init__(self, cl_reg: ClassicalRegister):
        self.classical_register = cl_reg
