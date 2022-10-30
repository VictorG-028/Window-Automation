from __future__ import annotations

class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        assert type(x) == type(y) == int
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    # Allow iterate over atribute values (in this case, x and y)
    def __iter__(self) -> int:
        for value in self.__dict__.values():
            yield value

    def __add__(self, other: Point) -> Point:
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)
