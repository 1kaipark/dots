from fabric import Application
from fabric.widgets.box import Box
from fabric.widgets.datetime import Button
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.hyprland.widgets import ActiveWindow
from fabric.utils import (
    get_relative_path,
)


from leftbar.controlcenter import ControlCenter
from utils.monitors import get_all_monitors, get_current_gdk_monitor_id

from leftbar.user.icons import Icons

class StatusBar(Window):
    def __init__(
        self,
    ):
        super().__init__(
            name="bar",
            title="top-left-bar",
            layer="top",
            anchor="left top",
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

        self.active_window = ActiveWindow(name="hyprland-window")

        self.children = Box(
                spacing=4,
                orientation="h",
                children=[
                    self.start_menu,
                    self.active_window,
                ]
        )

        self.show_all()

        self.control_center = ControlCenter()
        self.control_center.hide() 
        self.control_center_open = False

    
    def show_panel(self, *args) -> None:
        if self.control_center.is_visible(): self.control_center.hide()
        else: self.control_center.show()

if __name__ == "__main__":
    monitors = get_all_monitors()

    for monitor in monitors.keys():
        bar = StatusBar()
        bar.monitor = monitor 
        app = Application(f"bar{str(monitor)}", bar)
        app.set_stylesheet_from_file(get_relative_path("./style.css"))
        app.run()
