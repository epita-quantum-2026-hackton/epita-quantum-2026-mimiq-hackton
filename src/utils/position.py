from typing import Self


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: Self) -> bool:
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"{{{self.x},{self.y}}}"
