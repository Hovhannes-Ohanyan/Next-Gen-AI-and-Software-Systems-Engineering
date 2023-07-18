class TypeCheckMeta(type):
    def __new__(cls, name, bases, attrs):
        new_attrs = {}
        for attr, value in attrs.items():
            if attr.startswith("__"):
                new_attrs[attr] = value
            else:
                new_attrs[attr] = cls.wrap_attribute(attr, value)
        return super().__new__(cls, name, bases, new_attrs)

    @staticmethod
    def wrap_attribute(attr, value):
        def type_checked_setter(instance, new_value):
            if not isinstance(new_value, type(value)):
                raise TypeError(f"Invalid type assigned to '{attr}'. Expected '{type(value).__name__}', got '{type(new_value).__name__}'.")
            setattr(instance, f"_{attr}", new_value)

        def type_checked_getter(instance):
            return getattr(instance, f"_{attr}")

        return property(type_checked_getter, type_checked_setter)


class MyClass(metaclass=TypeCheckMeta):
    integer_attr = 0
    float_attr = 0.0
    string_attr = ""

    def __init__(self, integer_attr, float_attr, string_attr):
        self.integer_attr = integer_attr
        self.float_attr = float_attr
        self.string_attr = string_attr


obj = MyClass(1, 3.14, "Hello, world!")
