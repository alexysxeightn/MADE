from math import atan2

EPS = 1e-5


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Vector:
    def __init__(self, a, b):
        if isinstance(a, Point) and isinstance(b, Point):
            self.x = b.x - a.x
            self.y = b.y - a.y
        else:
            self.x = a
            self.y = b
        self.angle = self._angle()
        self.r = self._r()

    def __add__(self, other):
        """+ is sum of vectors"""
        return Vector(self.x + other.x, self.y + other.y)

    def __neg__(self):
        """- is a unary minus for vectors"""
        return Vector(-self.x, -self.y)

    def __mul__(self, other):
        """* is a dot product of vectors"""
        return self.x * other.x + self.y * other.y

    def __matmul__(self, other):
        """@ is a cross product of vectors"""
        return self.x * other.y - self.y * other.x

    def __xor__(self, other):
        """^ is the angle between vectors"""
        return atan2(self @ other, self * other)

    def _angle(self):
        """polar angle of vector"""
        return atan2(self.y, self.x)

    def _r(self):
        """length of vector"""
        return (self * self) ** 0.5


def point_on_segment(p, a, b):
    pa = Vector(p, a)
    pb = Vector(p, b)
    return pa * pb < EPS and abs(pa @ pb) < EPS


def main():
    N, a_x, a_y = map(int, input().split())
    a = Point(a_x, a_y)
    p_x, p_y = map(int, input().split())
    polygon = [None] * N
    polygon[0] = Point(p_x, p_y)

    point_on_border = False
    sum_angle = 0

    for i in range(1, N):
        p_x, p_y = map(int, input().split())
        polygon[i] = Point(p_x, p_y)
        point_on_border = point_on_border or point_on_segment(a, polygon[i - 1], polygon[i])
        sum_angle += Vector(a, polygon[i - 1]) ^ Vector(a, polygon[i])

    point_on_border = point_on_border or point_on_segment(a, polygon[N - 1], polygon[0])
    sum_angle += Vector(a, polygon[N - 1]) ^ Vector(a, polygon[0])

    print("YES" if abs(sum_angle) > EPS or point_on_border else "NO")


if __name__ == "__main__":
    main()
