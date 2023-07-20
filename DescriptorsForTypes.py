
class ValidTypeDescriptor:
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def validate_type(self, value):
        if not isinstance(value, self.expected_type):
            raise ValueError(f"Expected type  {self.expected_type.__name__}, but got {type(value).__name__}")

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        self.validate_type(value)
        instance.__dict__[self.name] = value


class Person:
    age = ValidTypeDescriptor(int)
    height = ValidTypeDescriptor(float)
    tags = ValidTypeDescriptor(list)
    favorite_foods = ValidTypeDescriptor(tuple)
    name = ValidTypeDescriptor(str)

    def __init__(self, age, height, tags, favorite_foods, name):
        self.age = age
        self.height = height
        self.tags = tags
        self.favorite_foods = favorite_foods
        self.name = name


try:
    person = Person(age=30, height=175.5, tags=['friendly', 'adventurous'], favorite_foods=('pizza', 'sushi'),
                    name='John Doe')

    

    person.age = "jdn"
    person.height = '175.5'
    person.tags = {'friendly', 'adventurous'}
    person.favorite_foods = 'burger'
    person.name = 100

except ValueError as e:
    print(e)
