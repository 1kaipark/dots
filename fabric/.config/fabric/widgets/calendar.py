from gi.repository import Gtk 

from fabric.widgets.box import Box 
from fabric.widgets.wayland import WaylandWindow as Window
from .weather import Weather
from .quote_display import QuoteDisplay

class CalendarWidget(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.calendar = Gtk.Calendar() 
        self.add(self.calendar)

class CalendarWindow(Window):
    def __init__(
        self, **kwargs
    ):

        super().__init__(
            layer="overlay",
            title="calendar-popup",
            anchor="center left",
            margin="10px 10px 10px 10px",
            exclusivity="none",
            visible=False,
            all_visible=False,
            keyboard_mode="on-demand",
            **kwargs,
        )

        self.connect("key-press-event", self.on_key_press)
        self._container = Box(orientation="v")

        self._container.add(CalendarWidget())
        self._container.add(Weather())
        self._container.add(QuoteDisplay())
        self.add(self._container)
        self.show_all()

    def toggle_visible(self) -> None:
        self.set_visible(not self.is_visible())

    def on_key_press(self, _, event):
        if event.keyval == 65307:  # ESC key
            focused_widget = self.get_focus()
            if not isinstance(focused_widget, Gtk.Entry):
                self.hide()
                return True  
        return False  




