from gi.repository import Gtk 

from fabric.widgets.box import Box 


class CalendarWidget(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.calendar = Gtk.Calendar() 
        self.add(self.calendar)

