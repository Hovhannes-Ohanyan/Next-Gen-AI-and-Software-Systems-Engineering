
class Vehicle:
    def __init__(self, make, model, year):
        self.model = model
        self.make = make
        self.year = year

    def start_engine(self):
        print("Start")

    def stop_engine(self):
        print("Stop")


class Car(Vehicle):
    def __init__(self, make, model, year, doors=4):
        super().__init__(make, model, year)
        self.doors = doors

    def start_engine(self):
        super().start_engine()
        print("Car engine start")

    def stop_engine(self):
        super().stop_engine()
        print("Car engine stop")

    @staticmethod
    def drive():
        print("drive Car")


class Motorcycle(Vehicle):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)

    def start_engine(self):
        super().start_engine()
        print("Motorcycle engine start")

    def stop_engine(self):
        super().stop_engine()
        print("Motorcycle engine stop")

    @staticmethod
    def ride():
        print("Motorcycle Riding")


class Bicycle(Vehicle):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)

    @staticmethod
    def start_pedaling():
        print("Pedaling the bicycle.")

    @staticmethod
    def stop_pedaling():
        print("Stopped pedaling the bicycle.")

    @staticmethod
    def ride():
        print("Riding the bicycle.")


car = Car("Bmw", "m6", 2022, 4)
car.start_engine()
car.drive()
car.stop_engine()

motorcycle = Motorcycle("Honda", "kawasaki", 2023)
motorcycle.start_engine()
motorcycle.ride()
motorcycle.stop_engine()

bicycle = Bicycle("Jump", "as 2", 2021)
bicycle.start_pedaling()
bicycle.ride()
bicycle.stop_pedaling()
