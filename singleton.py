class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Hundred(metaclass=SingletonMeta):
    def __init__(self):
        setattr(self, 'name', 'hundred')
        setattr(self, 'value', 100)


h1 = Hundred()
h2 = Hundred()

print(h1 is h2)  
print(h1.value)  
print(h2.name)
