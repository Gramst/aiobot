from typing import List

class FromIncomeData:

    @classmethod
    def make_from_data(cls, data: dict) -> 'cls':
        if data and cls.KEYS:
            _ = [data.get(i) for i in cls.KEYS]
            return cls(*_)

    @classmethod
    def make_list_from_data(cls, data: list) -> List['cls']:
        if data and isinstance(data, list):
            return [cls.make_from_data(i) for i in data]
        return None

