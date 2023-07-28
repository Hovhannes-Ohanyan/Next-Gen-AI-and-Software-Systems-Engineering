class SlottedStruct(type):
    def __new__(cls, name, bases, dct):
        if name != 'Point':
            dct['__slots__'] = ('_coords',)

        cls_instance = super().__new__(cls, name, bases, dct)
        return cls_instance


class Point(metaclass=SlottedStruct):
    def __init__(self, *coords):
        self._coords = coords

    def __eq__(self, other):
        if isinstance(other, Point):
            return self._coords == other._coords
        return False

    def __hash__(self):
        return hash(self._coords)

    def __repr__(self):
        return f"{self.__class__.__name__}{self._coords}"


class Point2D(Point):
    def __init__(self, x, y):
        super().__init__(x, y)


class Point3D(Point):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)


class Point4D(Point):
    def __init__(self, x, y, z, w):
        super().__init__(x, y, z, w)


p1 = Point2D(1, 2)
p2 = Point2D(1, 2)
p3 = Point3D(1, 2, 3)
p4 = Point4D(1, 2, 3, 4)

print(p1)  
print(p3 == p2)  
print(hash(p1) == hash(p2))  
