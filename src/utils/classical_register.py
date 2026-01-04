from typing import Optional


class ClassicalRegister:
    def __init__(self, name: str, idx: Optional[int] = None):
        self.name = name
        self.idx = idx
