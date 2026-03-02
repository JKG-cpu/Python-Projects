from .imports import *

class GeometryFormulas:
    def __init__(self, rounding_number: int = 1) -> None:
        self.rounding_number = rounding_number

    # Reset
    def reset_rounding_number(self, new_number: int) -> None:
        self.rounding_number = new_number

    # Formulas
    def distance(self, coord1: tuple[int, int], coord2: tuple[int, int]) -> float | str:
        if not (isinstance(coord1, tuple) and isinstance(coord2, tuple)):
            return "You need to enter in two coordinate points (x, y), (x2, y2)"

        x1, y1 = coord1
        x2, y2 = coord2
        
        return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), self.rounding_number)
    
    def midpoint(self, coord1: tuple[int, int], coord2: tuple[int, int]) -> tuple | str:
        if not (isinstance(coord1, tuple) and isinstance(coord2, tuple)):
            return "You need to enter in two coordinate points (x, y), (x2, y2)"

        x1, y1 = coord1
        x2, y2 = coord2

        first_point = (x2 + x1) / 2
        second_point = (y2 + y1) / 2
        
        return (round(first_point, 1), round(second_point, self.rounding_number))

    def slope(self, coord1: tuple[int, int], coord2: tuple[int, int]) -> Fraction | str:
        if not (isinstance(coord1, tuple) and isinstance(coord2, tuple)):
            return "You need to enter in two coordinate points (x, y), (x2, y2)"

        x1, y1 = coord1
        x2, y2 = coord2
        
        return Fraction(round(y2 - y1, self.rounding_number), round(x2 - x1, self.rounding_number))
    
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

    def point_on_circle(self, center: tuple[int, int], radius: int | float, coord: tuple[int, int]) -> bool | str:
        if not (isinstance(center, tuple) and (isinstance(radius, int) or isinstance(radius, float)) and isinstance(coord, tuple)):
            return "You must provide valid arguments."

        k, h = -center[0], -center[1]
        x, y = coord
        r2 = radius ** 2

        left_side = (x + k) ** 2 + (y + h) ** 2
        right_side = r2

        if math.isclose(left_side, right_side, rel_tol=1e-9):
            return True
    
        return False
