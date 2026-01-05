from typing import Optional


class ClassicalRegister:
    def __init__(self, name: str, idx: Optional[int] = None):
        self.name = name
        self.idx = idx

    def __repr__(self) -> str:
        return self.name if self.idx is None else f"{self.name}[{self.idx}]"
