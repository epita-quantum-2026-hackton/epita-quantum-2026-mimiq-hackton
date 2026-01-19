from typing import Self


class Position:
    """
    2D integer coordinate used to locate a physical qubit on the neutral-atom grid.
    """
    
    def __init__(self, x: int, y: int):
        """
        Construct a Position.
        
        Parameters:
        - x: x-axis coordinate.
        - y: y-axis coordinate.
        """
        self.x = x
        self.y = y

    def __eq__(self, other: Self) -> bool:
        """
        Compare two positions for equality (same x and y).
        """
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        """
        Return a compact string representation of this Position: {x,y}.
        """
        return f"{{{self.x},{self.y}}}"

    def __hash__(self) -> int:
        return self.x + self.y * 65536

    def clone(self) -> Self:
        """
        Return a copy of this position.
        """
        return Position(self.x, self.y)

    def translated(self, dx: int, dy: int) -> Self:
        """
        Return a new position translated by the given offsets.
        
        Parameters:
        - dx: delta to apply on x.
        - dy: delta to apply on y.
        """
        return Position(self.x + dx, self.y + dy)
