from abc import ABC, abstractmethod
import os


class DataStorage(ABC):
    @abstractmethod
    def save(self, data, identifier):
        pass

    @abstractmethod
    def load(self, identifier):
        pass

    @abstractmethod
    def delete(self, identifier):
        pass


class FileStorage(DataStorage):
    def save(self, data, identifier: str):
        file_name = f"data_{identifier}.txt"
        with open(file_name, "w") as file:
            file.write(data)

    def load(self, identifier: str):
        file_name = f"data_{identifier}.txt"
        with open(file_name, "r") as file:
            print(file.read())

    def delete(self, identifier: str):
        file_name = f"data_{identifier}.txt"
        os.remove(file_name)
        print("file deleted")


class DatabaseStorage(DataStorage):
    def save(self, data, identifier):
        print("Saving data to database:", data)

    def load(self, identifier):
        print("Loading data from  identifier:", identifier)

    def delete(self, identifier):
        print("Deleting data from  identifier:", identifier)





