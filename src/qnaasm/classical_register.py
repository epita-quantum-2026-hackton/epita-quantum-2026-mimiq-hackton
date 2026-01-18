from typing import Optional


class ClassicalRegister:
    """
    Represent a classical register
    """

    def __init__(self, name: str, idx: Optional[int] = None):
        """
        Docstring for __init__
        
        Parameters:
        - name: register name.
        - idx: optional bit index within the register.
        """
        self.name = name
        self.idx = idx

    def __repr__(self) -> str:
        return self.name if self.idx is None else f"{self.name}[{self.idx}]"
