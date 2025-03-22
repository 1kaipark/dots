from fabric import Application
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.eventbox import EventBox
from fabric.widgets.datetime import Button, DateTime
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.utils import (
    get_relative_path,
    exec_shell_command_async,
)


from fabric.hyprland.widgets import ActiveWindow, Workspaces, WorkspaceButton

from controlcenter import ControlCenter

from user.icons import Icons
from user.commands import Commands
from widgets.battery_single import BatterySingle
from widgets.systray import SystemTray
from widgets.calendar import CalendarWindow

class StatusBar(Window):
    def __init__(
        self,
    ):
        super().__init__(
            name="bar",
            title="left-bar",
            layer="top",
            anchor="top left bottom left",
            margin="10px 0px 10px 15px", # top right bottom left
            exclusivity="auto",
            visible=False,
            all_visible=False,
        )

        self.start_menu = Button(
#            label=" ", 
            label=Icons.SEND.value,
            on_clicked=self.show_control_center,
            name="bar-icon",
            style="margin: 15px 10px 10px 5px;",  # to center the icon glyph
        )

        self.control_center = ControlCenter()
        self.control_center.hide()

        self.calendar_window = CalendarWindow(name="window")
        self.calendar_window.hide()

        self.workspaces = Workspaces(
             name="workspaces",
             orientation="v",
             h_align="center",
             spacing=4,
             buttons_factory=lambda ws_id: WorkspaceButton(id=ws_id, label=['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'][ws_id - 1]),
        )
 
        self.battery = BatterySingle(name="battery", h_align="center")

        self.system_tray = Box(name="system-tray", children=[SystemTray(pixel_size=18)], h_align="center")


        self.date_time = DateTime(
            style_classes="bar-clock",
            formatters=("%H\n%M")
        )
        self.date_time.connect(
            "clicked",
            self.show_calendar_window
        )

        self.notification_button = Button(
            label=Icons.NOTIFICATIONS.value,
            name="bar-icon",
            style="margin: 10px 10px 15px 5px;",  # to center the icon glyph
        )
        self.notification_button.connect(
            "clicked",
            self.toggle_notifications,
        )


        self.children = CenterBox(
            name="bar",
            orientation="v",
            start_children=Box(
                name="bar-inner",
                spacing=4,
                orientation="v",
                children=[
                    self.start_menu,
                    self.workspaces
                ]
            ),

            center_children=Box(
                name="bar-inner",
                spacing=4,
                orientation="v",
                children=[
                    self.date_time,
                ]
            ),

            
            end_children=Box(
                name="bar-inner",
                spacing=4,
                orientation="v",
                children=[
                    self.system_tray,
                    self.battery,
                    self.notification_button,
                ]
            ),
        )


        self.show_all()

    def show_control_center(self, *_):
        self.control_center.set_visible(not self.control_center.is_visible())
        self.calendar_window.hide()

    def show_calendar_window(self, *_):
        self.calendar_window.set_visible(not self.calendar_window.is_visible())
        self.control_center.hide()

    def toggle_notifications(self, *_):
        exec_shell_command_async(Commands.NOTIFICATIONS.value)

if __name__ == "__main__":
    bar = StatusBar()
    app = Application("bar", bar)
    app.set_stylesheet_from_file(get_relative_path("./style.css"))

    app.run()
