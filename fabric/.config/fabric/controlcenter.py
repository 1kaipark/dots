"""
a basic and minimal control center made in fabric/Gtk.

TODO : desparately needs a refactor but who cares lmao
"""

from fabric.widgets.box import Box
from fabric.widgets.wayland import WaylandWindow as Window

from fabric.utils import invoke_repeater

from fabric import Application
from fabric.utils import get_relative_path

from widgets.media import MediaWidget
from widgets.profile import Profile
from widgets.clock import Clock
from widgets.power_menu import PowerMenu
from widgets.hw_monitor import HWMonitor
from widgets.controls import Controls
from widgets.weather import Weather
from widgets.launchers import Launchers 
from widgets.quote_display import QuoteDisplay
from widgets.network_controls import NetworkControls
# from widgets.notis import NotificationCenter
from widgets.calendar import CalendarWidget
from widgets.todos import Todos


from loguru import logger

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


"""
CSS CLASSES
* profile-pic
* button-icon-large
* button-icon-small-a through c
* button-icon-smallest
* clock-a
* clock-b
* clock-c
* progress-bar-red, green, yellow, etc
* label-red, ...
* scale-a through c
* label-a through c (colors)
"""

class ControlCenter(Window):

    def on_key_press(self, _, event):
        if event.keyval == 65307:  # ESC key
            focused_widget = self.get_focus()
            if not isinstance(focused_widget, Gtk.Entry):
                self.hide()
                return True  
        return False  

    

    def __init__(self, **kwargs):
        super().__init__(
            layer="overlay",
            title="control-center",
            anchor="top left",
            margin="10px 10px 10px 10px",
            exclusivity="none",
            visible=False,
            all_visible=False,
            keyboard_mode="on-demand",
            **kwargs,
        )

        self.connect("key-press-event", self.on_key_press)

        #  ____  _____ _____ ___ _   _ _____
        # |  _ \| ____|  ___|_ _| \ | | ____|
        # | | | |  _| | |_   | ||  \| |  _|
        # | |_| | |___|  _|  | || |\  | |___
        # |____/|_____|_|   |___|_| \_|_____|
        #
        # __        _____ ____   ____ _____ _____ ____
        # \ \      / /_ _|  _ \ / ___| ____|_   _/ ___|
        #  \ \ /\ / / | || | | | |  _|  _|   | | \___ \
        #   \ V  V /  | || |_| | |_| | |___  | |  ___) |
        #    \_/\_/  |___|____/ \____|_____| |_| |____/
        #
        self.profile = Profile(name="profile")


        self.hwmon = HWMonitor(name="hw-mon")  # this goes in center_widgets

        self.controls = Controls(name="controls", size=(300, -1))  # sliders for vol, brightness

        self.power_menu = PowerMenu()
        self.media = MediaWidget(name="media")

        self.header = Box(orientation="h", children=[self.profile])
        self.row_1 = Box(orientation="h", children=[self.hwmon], name="outer-box")
        self.row_2 = Box(
            orientation="h",
            children=[
                self.controls
            ], 
            name="outer-box"
        )
#        self.row_3 = Box(
#            orientation="h", children=[self.fetch], name="outer-box"
#        )
        self.row_4 = Box(
            orientation="h", children=[self.power_menu], name="outer-box"
        )

        self.todos = Todos(name="todos", h_expand=True, size=(366, 120))
        self.row_3 = Box(
            orientation="h", children=[self.todos], name="outer-box", h_expand=True
        )
        
        self.row_5 = Box(
            orientation="h", children=[self.media], name="outer-box", h_expand=True
        )
        

        self.widgets = [self.header, self.row_1, self.row_2, self.row_3, self.row_4, self.row_5]

        self.add(
            Box(
                name="window",
                orientation="v",
                spacing=24,
                children=self.widgets,
            ),
        )
        self.show_all()

    def toggle_visible(self) -> None:
        self.set_visible(not self.is_visible())

if __name__ == "__main__":
    control_center = ControlCenter()
    app = Application("control-center", control_center)
    app.set_stylesheet_from_file(get_relative_path("./style.css"))

    app.run()
