import numpy as np


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def to_tuple(self) -> tuple:
        """Converts object point to tuple."""
        return self.x, self.y


class Line:

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f"Line(p1={self.p1}, p2={self.p2})"

    def to_tuple(self) -> tuple:
        """Converts object Line to tuple of tuples."""
        return self.p1.to_tuple(), self.p2.to_tuple()

    def is_vertical_line(self) -> bool:
        """Checks if the line is vertical."""
        if self.p1.x == self.p2.x:
            return True

        return False

    def is_horizontal_line(self) -> bool:
        """Checks if the line is horizontal."""
        if self.p1.y == self.p2.y:
            return True

        return False

    def find_segment_points(self, include_diagonal: bool):
        """Finds all the points that compose the segment, including the end points that initialize the Line object."""
        points = []
        if self.is_vertical_line():
            y_coords = sorted([self.p1.y, self.p2.y])

            # Ensure that larger coord is included
            y_coords[1] += 1
            for y in range(*y_coords):
                points.append(Point(self.p1.x, y))
        elif self.is_horizontal_line():
            x_coords = sorted([self.p1.x, self.p2.x])

            # Ensure that larger coord is included
            x_coords[1] += 1
            for x in range(*x_coords):
                points.append(Point(x, self.p1.y))
        else:
            if include_diagonal:
                # Switch point to have easier code
                if self.p2.x < self.p1.x:
                    self.p1, self.p2 = self.p2, self.p1

                x_coords = sorted([self.p1.x, self.p2.x])
                y_coords = sorted([self.p1.y, self.p2.y])

                # Ensure that larger coords are included
                x_coords[1] += 1
                y_coords[1] += 1
                if self.p1.y < self.p2.y:
                    for x, y in zip(range(*x_coords), range(*y_coords)):
                        points.append(Point(x, y))
                else:
                    for x, y in zip(range(*x_coords), reversed(range(*y_coords))):
                        points.append(Point(x, y))

        return points


def read_input() -> list[Line]:
    """Reads input data."""
    def clean_point(point: str) -> tuple:
        x, y = tuple([int(i) for i in point.strip().split(',')])

        # Invert coordinates for how the grid is defined
        return x, y

    with open("Day 5 - Hydrothermal Venture/input.txt", 'r') as f:
        ends = []
        for line in f:
            point_1_str, point_2_str = line.split(' -> ')
            point_1 = Point(*clean_point(point_1_str))
            point_2 = Point(*clean_point(point_2_str))

            ends.append(Line(point_1, point_2))

    return ends


def build_diagram(ends: list[Line]) -> np.ndarray:
    """Builds a starting diagram to fill with lines."""
    max_x = -1
    max_y = -1
    for end in ends:
        if end.p1.x > max_x:
            max_x = end.p1.x
        if end.p2.x > max_x:
            max_x = end.p2.x

        if end.p1.y > max_y:
            max_y = end.p1.y
        if end.p2.y > max_y:
            max_y = end.p2.y

    return np.zeros((max_x + 1, max_y + 1), dtype=int)


def updates_diagram(diagram: np.ndarray, points: list[Point]) -> np.ndarray:
    """Updates a diagram given a list of points."""
    for p in points:
        diagram[p.to_tuple()] += 1

    return diagram


def fill_diagram(diagram: np.ndarray, ends: list[Line], include_diagonal: bool) -> np.ndarray:
    """Fills a diagram given a list of segment lines."""
    for line in ends:
        seg_points = line.find_segment_points(include_diagonal)
        diagram = updates_diagram(diagram, seg_points)

    return diagram


def find_points_overlap(diagram: np.ndarray, n_lines: int):
    """Finds in how many points there are at least `n_lines` that overlap."""
    return (diagram >= n_lines).sum()


ends = read_input()


# Part 1
diagram = build_diagram(ends)
diagram = fill_diagram(diagram, ends, include_diagonal=False)
points_overlap = find_points_overlap(diagram, n_lines=2)

print(f"The number of points where at least two vertical or horizontal lines overlap is equal two: {points_overlap}")

# Part 2
diagram = build_diagram(ends)
diagram = fill_diagram(diagram, ends, include_diagonal=True)
points_overlap = find_points_overlap(diagram, n_lines=2)

print(f"The number of points where at least two lines overlap is equal two: {points_overlap}")
