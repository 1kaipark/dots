from fabric import Application
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.eventbox import EventBox
from fabric.widgets.datetime import Button, DateTime
from fabric.widgets.centerbox import CenterBox
from fabric.system_tray.widgets import SystemTray
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.utils import (
    get_relative_path,
)


from .controlcenter import ControlCenter

from .user.icons import Icons

class StatusBar(Window):
    def __init__(
        self,
    ):
        super().__init__(
            name="bar",
            title="top-left-bar",
            layer="top",
            anchor="top left",
            margin="-35px 10px 10px 15px", # top right bottom left
            exclusivity="auto",
            visible=False,
            all_visible=False,
        )

        self.start_menu = Button(
#            label=" ", 
            label=Icons.SEND.value,
            on_clicked=self.show_panel,
            style="margin: 0px 0px 0px 10px; font-size: 14px",  # to center the icon glyph
        )

        self.system_tray = SystemTray(name="system-tray", spacing=4)

        self.date_time = DateTime(name="date-time", formatters=("%H:%M"), h_align="center", v_align="center")
        self.cal_date = DateTime(name="date-time", formatters=("%a %m/%d/%Y"))

        self.children = CenterBox(
            name="bar",
            start_children=Box(
                name="bar-inner",
                spacing=4,
                orientation="v",
                children=[
                    self.start_menu
                ]
            ),

            center_children=Box(
                name="bar-inner",
                spacing=4,
                orientation="v",
                children=[
                ]
            ),
            
            end_children=Box(
                name="bar-inner",
                spacing=4,
                orientation="v",
                children=[
                    self.system_tray
                ]
            ),
        )


        self.show_all()

if __name__ == "__main__":
    bar = StatusBar()
    app = Application("bar", bar)
    app.set_stylesheet_from_file(get_relative_path("../style.css"))

    app.run()
