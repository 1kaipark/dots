from fabric.widgets.box import Box 
from fabric.widgets.datetime import DateTime

class Clock(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="v", **kwargs)
        self.time = DateTime(formatters=("%H %M"), name="clock-a")
        self.date = DateTime(formatters=("%m %d"), name="clock-b")
        self.day = DateTime(formatters=("%A, %B"))

        self.add(self.time)
        self.add(self.date)
        self.add(self.day)



