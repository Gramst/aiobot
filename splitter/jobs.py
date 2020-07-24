import asyncio

class Job:
    ticker: int
    current_tick: int

    def __init__(self, ticker_value):
        self.ticker = ticker_value
        self.current_tick = 0

    def update_timer(self):
        self.current_tick += 1

    @property
    def is_ready(self) -> bool:
        if self.current_tick >= self.ticker:
            self.current_tick = self.current_tick - self.ticker
            return True
        else:
            return False

    @classmethod
    def get_job(cls, function, ticker_value: int) -> 'Job':
        res = cls(ticker_value)
        res.run = function
        return res
