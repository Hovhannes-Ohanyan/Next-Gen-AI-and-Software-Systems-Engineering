class Int:
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def validate_value(self, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Value must be greater than or equal to {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Value must be less than or equal to {self.max_value}")
        if not isinstance(value, int):
            raise ValueError("Value must be an integer")

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        self.validate_value(value)
        instance.__dict__[self.name] = value


class Point2D:
    def __init__(self, x_min=None, x_max=None, y_min=None, y_max=None):
        self.x = Int(x_min, x_max)
        self.y = Int(y_min, y_max)

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        if not isinstance(value, tuple) or len(value) != 2:
            raise ValueError(f"{self.name} must be a tuple of length 2")
        x, y = value
        self.x.__set__(instance, x)
        self.y.__set__(instance, y)


class Point2DSequence:
    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length
        self.max_length = max_length

    def validate_sequence(self, value):
        if not isinstance(value, (list, tuple)):
            raise ValueError("Vertices must be a list or tuple")
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError(f"Polygon must have at least {self.min_length} vertices")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f"Polygon can have at most {self.max_length} vertices")
        for vertex in value:
            if not isinstance(vertex, Point2D):
                raise ValueError("Each vertex must be an instance of Point2D")

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        self.validate_sequence(value)
        instance.__dict__[self.name] = value


class Polygon:
    vertices = Point2DSequence(min_length=3, max_length=10)

    def __init__(self, *vertices):
        self.vertices = list(vertices)

    def append(self, point):
        self.vertices.append(point)
        self.vertices = self.vertices[:10]  # Limit the number of vertices to 10

    def __repr__(self):
        return f"Polygon({repr(self.vertices)})"
