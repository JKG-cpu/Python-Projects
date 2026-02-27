from .imports import *

class Shape:
    def __init__(self, sides: int | None = None, properties: list[str] | dict[dict] | None = None) -> None:
        # Properties
        self.sides = sides
        self.properties = properties

    def display_properties(self) -> None:
        if isinstance(self.properties, dict):
            # Shape Name
            print(f"{self.__class__.__qualname__} Properties")

            for i, key in enumerate(self.properties, 1):
                print(f"  {i}. {key}")

                for prop in self.properties[key]:
                    print(f"      - {prop} => {self.properties[key][prop]}")
                
                print()

        else:
            # Shape Name
            print(f"{self.__class__.__qualname__} Properties")

            # Properties
            for prop in self.properties:
                print(f"    - {prop}")
        
            print()

class Parallelogram(Shape):
    def __init__(self):
        super().__init__(4, [
            "Opposite Sides are congruent", 
            "Opposite Angles are congruent",
            "Consecutive Angles are supplementary",
            "Diagonals bisect each other"
        ])

class Kite(Shape):
    def __init__(self):
        super().__init__(4, [
            "Opposite Angles are congruent",
            "Diagonals are perpendicular angle bisectors"
        ])

class Triangle(Shape):
    def __init__(self):
        super().__init__(3, {
            "By Side": {
                "Equilateral": "3 Congruent Sides",
                "Isosceles": "2 Congruent Sides",
                "Scalene": "0 Congruent Sides"
            },
            "By Angle": {
                "Acute": "3 Angles < 90 degrees",
                "Right": "One angle is 90 degrees",
                "Obtuse": "Has one angle > 90 degrees"
            }
        })

class Trapezoid(Shape):
    def __init__(self):
        super().__init__(4, [
            "Base Angles are congruent",
            "Top Angles are congruent",
            "Diagonals are congruent"
        ])

class Rhombuse(Shape):
    def __init__(self):
        super().__init__(4, [
            "All four sides are congruent and opposite sides are parallel",
            "Diagonals are perpendiculr bisectors",
            "Diagonals bisect opposite angles"
        ])

class Rectangle(Shape):
    def __init__(self):
        super().__init__(4, [
            "Four right angles",
            "opposite sides are congruent to opposite sides",
            "Diagonals are congruent and bisectors"
        ])

class Square(Shape):
    def __init__(self):
        super().__init__(4, ["Has properties of Parallelograms, Rhombuses, and rectangles"])

