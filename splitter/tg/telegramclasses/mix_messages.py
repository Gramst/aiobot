from typing import List, Union
from dataclasses import is_dataclass

class FromIncomeData:
    KEYS = []

    @classmethod
    def make_from_data(cls, data: Union[dict, 'dataclass']) -> 'cls':
        if is_dataclass(data):
            return data
        if data and cls.KEYS:
            _ = [data.get(i) for i in cls.KEYS]
            return cls(*_)
        return None

    @classmethod
    def make_list_from_data(cls, data: list) -> List['cls']:
        if data and isinstance(data, list):
            return [cls.make_from_data(i) for i in data]
        return None

