from abc import ABC, abstractmethod

class AbstractRepository(ABC):
    @abstractmethod
    def get_all(self, sort_field=None, sort_descending=False):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def create(self, obj):
        pass

    @abstractmethod
    def update(self, obj):
        pass

    @abstractmethod
    def delete(self, obj):
        pass