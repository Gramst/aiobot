from dataclasses import dataclass, field

from .datamix import FromIncomeData

@dataclass
class A(FromIncomeData):
    KEY = ['data']
    data: int

    @classmethod
    def make_from_data(cls, data):
        obj = cls(data)
        return obj

@dataclass
class B:
    value  : int
    __obj  : str = field(repr=False)
    obj: int = field(init=False)

    def __post_init__(self):
        self.obj = A.make_list_from_data(self.__obj)

if __name__ == "__main__":
    h = B(1, [])
    print(h)
    print(h.obj)