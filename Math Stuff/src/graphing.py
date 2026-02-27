from .imports import *
from .geometric_formulas import GeometryFormulas

gf = GeometryFormulas()

class Line:
    def __init__(self, 
        coord1: tuple[int, int], 
        coord2: tuple[int, int],
        name: str) -> None:
        self.coord1 = coord1
        self.coord2 = coord2
        self.name = name

        # Properites
        self.slope = self._calculate_slope()

    def __str__(self) -> str:
        return f"Line {self.name}"

    def _calculate_slope(self) -> Fraction:
        return gf.slope(self.coord1, self.coord2)
    
    def get_slope(self) -> Fraction:
        return self.slope

class Point:
    def __init__(self, coord: tuple[int, int], name: str) -> None:
        self.coord = coord
        self.pname = name
    
    def __str__(self) -> str:
        return f"Point {self.pname}"

    @property
    def name(self) -> str:
        return self.pname

    @property
    def position(self) -> tuple[int, int]:
        return self.coord
