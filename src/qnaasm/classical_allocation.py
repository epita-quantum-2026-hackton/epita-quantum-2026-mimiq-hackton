from qnaasm import QNAasm


class ClassicalAllocation(QNAasm):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
