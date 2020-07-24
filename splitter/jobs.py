import asyncio

class Job:
    ticker: int
    current_tick: int

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
    def get_job(cls, function, ticker_value: int) -> Job:
        res = cls()
        res.current_tick = 0
        res.run = function
        return res