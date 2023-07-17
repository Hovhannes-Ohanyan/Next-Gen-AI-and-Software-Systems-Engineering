
class Resource:
    def __init__(self, name, manufacturer, total, allocated):
        self._name = name
        self._manufacturer = manufacturer
        self._total = total
        self._allocated = allocated

    @property
    def name(self):
        return self._name

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def total(self):
        return self._total

    @property
    def allocated(self):
        return self._allocated

    def __str__(self):
        return self._name

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self._name}', manufacturer='{self._manufacturer}'," \
               f" total={self._total}, allocated={self._allocated})"

    def claim(self, n):
        if (self._total - self._allocated) >= n:
            self._allocated += n
            print(f" Claimed {n} {self._name}")
        else:
            print(f"not enough {self._name}")

    def free_up(self, n):
        if self._allocated >= n:
            self._allocated -= n
            print(f"Free up {n} {self._name}")
        else:
            print(f"can't Free up more than allocated")

    def died(self, n):
        if self._total >= n:
            self._total -= n
            if self._allocated >= n:
                self._allocated -= n
            else:
                self._allocated = 0
            print(f"{n} {self._name} removed")
        else:
            print(f"not enough {self._name}")

    def purchased(self, n):
        self._total += n
        print(f"Purchased {n} new {self._name} ")

    @property
    def category(self):
        return self.__class__.__name__.lower()


class Storage(Resource):
    def __init__(self, name, manufacturer, total, allocated, capacity_GB):
        super().__init__(name, manufacturer, total, allocated)
        self._capacity_GB = capacity_GB

    @property
    def capacity_GB(self):
        return self._capacity_GB


def __repr__(self):
    return f"{self.__class__.__name__}(name='{self._name}', manufacturer='{self._manufacturer}'," \
           f" total={self._total}, allocated={self._allocated}, capacity_GB={self._capacity_GB})"


class CPU(Resource):
    def __init__(self, name, manufacturer, total, allocated, interface, socket, power_watts, cores):
        super().__init__(name, manufacturer, total, allocated)
        self._cores = cores
        self._interface = interface
        self._socket = socket
        self._power_watts = power_watts

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self._name}', manufacturer='{self._manufacturer}'," \
               f" total={self._total}, allocated={self._allocated}, cores={self._cores}, " \
               f"interface='{self._interface}', socket='{self._socket}', power_watts={self._power_watts})"


class HDD(Storage):
    def __init__(self, name, manufacturer, total, allocated, capacity_GB, size, rpm):
        super().__init__(name, manufacturer, total, allocated, capacity_GB)
        self._size = size
        self._rpm = rpm

    @property
    def size(self):
        return self._size

    @property
    def rpm(self):
        return self._rpm

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self._name}', manufacturer='{self._manufacturer}'," \
               f" total={self._total}, allocated={self._allocated}, capacity_GB={self._capacity_GB}, " \
               f"size='{self._size}', rpm={self._rpm})"


class SSD(Storage):
    def __init__(self, name, manufacturer, total, allocated, capacity_GB, interface):
        super().__init__(name, manufacturer, total, allocated, capacity_GB)
        self._interface = interface

    @property
    def interface(self):
        return self._interface

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self._name}', manufacturer='{self._manufacturer}', " \
               f"total={self._total}, allocated={self._allocated}, capacity_GB={self._capacity_GB}, " \
               f"interface='{self._interface}')"


cpu = CPU("Intel Core i9-9900K", "Intel", 5, 2, "LGA1151", "AM4", 95, 8)
hdd = HDD("Seagate Barracuda", "Seagate", 10, 3, 2000, "3.5", 7200)
ssd = SSD("Samsung 970 EVO Plus", "Samsung", 15, 5, 500, "PCIe NVMe")

print(cpu.name)
print(hdd.capacity_GB)
print(ssd.interface)

cpu.claim(1)
hdd.purchased(5)
ssd.free_up(2)

cpu.died(1)
hdd.free_up(4)
ssd.died(3)

print(cpu.category)
print(hdd.category)
print(ssd.category)
