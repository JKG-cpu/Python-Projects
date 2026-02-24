import math
from fractions import Fraction

class GeometryFormulas:
    def distance(self, coord1: tuple[int, int], coord2: tuple[int, int]) -> float | str:
        if not (isinstance(coord1, tuple) and isinstance(coord2, tuple)):
            return "You need to enter in two coordinate points (x, y), (x2, y2)"

        x1, y1 = coord1
        x2, y2 = coord2
        
        answer = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        return answer
    
    def midpoint(self, coord1: tuple[int, int], coord2: tuple[int, int]) -> tuple | str:
        if not (isinstance(coord1, tuple) and isinstance(coord2, tuple)):
            return "You need to enter in two coordinate points (x, y), (x2, y2)"

        x1, y1 = coord1
        x2, y2 = coord2

        first_point = (x2 + x1) / 2
        second_point = (y2 + y1) / 2
        
        return (first_point, second_point)

    def slope(self, coord1: tuple[int, int], coord2: tuple[int, int]) -> str:
        if not (isinstance(coord1, tuple) and isinstance(coord2, tuple)):
            return "You need to enter in two coordinate points (x, y), (x2, y2)"

        x1, y1 = coord1
        x2, y2 = coord2
        
        answer = Fraction(y2 - y1, x2 - x1)
        
        return answer
    
    def perimeter_of_triangle(self, coord1: tuple[int, int], coord2: tuple[int, int], coord3: tuple[int, int], decimal_point: int = 1) -> float:
        if not (isinstance(coord1, tuple) and isinstance(coord2, tuple)):
            return "You need to enter in two coordinate points (x, y), (x2, y2)"
        
        # Find first line (a -> b)
        fline = self.distance(coord1, coord2)
        
        # Find second line (b -> c)
        sline = self.distance(coord2, coord3)
        
        # Find third line (c -> a)
        tline = self.distance(coord3, coord1)

        # Add together and return
        answer = fline + sline + tline
        
        return round(answer, decimal_point)
