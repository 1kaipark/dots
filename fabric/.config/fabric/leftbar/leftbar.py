"""
a basic and minimal control center made in fabric/Gtk.

TODO : desparately needs a refactor but who cares lmao
"""

from fabric.widgets.box import Box
from fabric.widgets.wayland import WaylandWindow as Window

from fabric.utils import invoke_repeater

from .widgets.media import NowPlaying
from .widgets.profile import Profile
from .widgets.clock import Clock
from .widgets.power_menu import PowerMenu
from .widgets.hw_monitor import HWMonitor
from .widgets.controls import Controls
from .widgets.fetch import Fetch
from .widgets.launchers import Launchers 
from .widgets.quote_display import QuoteDisplay


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
    def __init__(self, **kwargs):
        super().__init__(
            layer="overlay",
            title="control-center",
            anchor="top left",
            margin="8px 8px 8px 8px",
            exclusivity="none",
            visible=False,
            all_visible=False,
            keyboard_mode="on-demand",
            on_key_press_event=lambda _, event: self.hide()
            if event.keyval == 65307
            else True,  # handle ESC = exit
            **kwargs,
        )

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

        self.profile = Profile(name="outer-box")

        self.power_menu = PowerMenu()

        self.clock = Clock()

        self.hwmon = HWMonitor(name="hw-mon")  # this goes in center_widgets

        self.controls = Controls(name="controls")  # sliders for vol, brightness

        self.fetch = Fetch(name="fetch")  # idea: cool neofetch polling

        self.media = NowPlaying(
            name="inner-box", max_len=25, cava_bars=24
        )  
        
        self.launchers = Launchers(name="launchers")

        self.quote_display = QuoteDisplay(name="quote-display")

        self.top_right = Box(
            children=[self.power_menu, self.clock],
            orientation="v",
            name="outer-box"
        )

        self.header = Box(
            orientation="h",
            children=[self.profile, self.top_right],
        )

        self.row_1 = Box(orientation="h", children=[self.hwmon], name="outer-box")
        self.row_2 = Box(orientation="h", children=[self.controls], name="outer-box")
        self.row_3 = Box(
            orientation="h", children=[self.fetch, self.media], name="outer-box"
        )
        self.row_4 = Box(
            orientation="h", children=[self.launchers], name="outer-box"
        )

        self.row_5 = Box(
            orientation="h", children=[self.quote_display], name="outer-box"
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

        invoke_repeater(2000, self.update_status)

    def update_status(self) -> bool:
        self.hwmon.update_status()
        return 1


