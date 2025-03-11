import psutil
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
# from fabric.hyprland.widgets import ActiveWindow, Workspaces, WorkspaceButton
from fabric.utils import (
    FormattedString,
    bulk_replace,
    invoke_repeater,
    get_relative_path,
    exec_shell_command,
)

from fabric.audio.service import Audio

from widgets.sidepanel import SidePanel
from widgets.battery import BatteryDisplay
from widgets.volume import VolumeWidget
from widgets.media import NowPlaying
from widgets.separator import Separator 
from widgets.cputemp import CPUTemp

class StatusBar(Window):
    def __init__(
        self,
        tray_instance: SystemTray | None = None,
    ):
        super().__init__(
            name="bar",
            layer="top",
            anchor="left bottom right",
            margin="-2px 10px 10px 10px", # top right bottom left
            exclusivity="auto",
            visible=False,
            all_visible=False,
        )

        self.start_menu = Button(
#            label=" ", 
            label="󰣇 ",
            name="bar-item-misc",
            on_clicked=self.show_panel,
            style="margin: 0px 0px 0px 0px; font-size: 12px",  # to center the icon glyph
        )

#         self.workspaces = Workspaces(
#             name="workspaces",
#             spacing=4,
#             buttons_factory=lambda ws_id: WorkspaceButton(id=ws_id, label=None),
#         )
# 
#         self.active_window = ActiveWindow(name="hyprland-window")
        
        if tray_instance == None:
            self.system_tray = SystemTray(name="system-tray", spacing=4)
            print("instantiating new tray because none provided")
        else:
            self.system_tray = tray_instance

        self.date_time = DateTime(name="date-time", formatters=("%H:%M"), h_align="center", v_align="center")
        self.cal_date = DateTime(name="date-time", formatters=("%a %m/%d/%Y"))

        self.now_playing = NowPlaying()


        
        self.cpu_temp = CPUTemp(name="widgets-container")

        self.ram_progress_bar = CircularProgressBar(
            name="ram-progress-bar", pie=False, size=24
        )
        self.cpu_progress_bar = CircularProgressBar(
            name="cpu-progress-bar", pie=False, size=24
        )
        self.ram_display = Overlay(
            child=self.ram_progress_bar,
            overlays=[
                Label("󰍛", style="margin: 0px 6px 0px 0px; font-size: 10px"),
            ],
        )

        self.cpu_display = Overlay(
            child=self.cpu_progress_bar,
            overlays=[
                Label("", style="margin: 0px 6px 0px 0px; font-size: 10px"),
            ],
        )

        self.battery_display = BatteryDisplay(name="widgets-container")

        self.status_container = Box(
            name="widgets-container",
            spacing=4,
            orientation="h",
            children=[
                self.cpu_temp,
                self.ram_display,
                self.cpu_display,
                VolumeWidget(),
            ]
        )

        self.noti_button = Button(
            label="hi", 
            name="bar-item-misc",
            spacing=4,
            on_clicked=lambda b, *_: exec_shell_command("swaync-client -t"),
        )


        self.children = CenterBox(
            name="bar-inner",
            start_children=Box(
                name="start-container",
                spacing=4,
                orientation="h",
                children=[
                    self.start_menu,
                    #                     self.workspaces,
                    #                     self.active_window,
                    self.now_playing,
                ]
            ),
            center_children=Box(
                name="center-container",
                spacing=4,
                orientation="h",
                children=[
                    self.cal_date,
                ],
            ),
            end_children=Box(
                name="end-container",
                spacing=4,
                orientation="h",
                children=[
                    self.system_tray,
                    self.battery_display,
                    self.status_container,
                    self.date_time,
                    self.noti_button,
                ],
            ),
        )


        invoke_repeater(1000, self.update_progress_bars)

        self.show_all()

        self.side_panel = SidePanel()
        self.side_panel.hide() 
    
    def show_panel(self, *args) -> None:
        if self.side_panel.is_visible(): self.side_panel.hide()
        else: self.side_panel.show()

    def update_progress_bars(self):
        self.ram_progress_bar.value = psutil.virtual_memory().percent / 100
        self.cpu_progress_bar.value = psutil.cpu_percent() / 100
        self.battery_display.update_percentage()

        self.cpu_temp.update_temps()
        return True
    
    def open_start_panel(self, b, *_):
        if self.side_panel_open:
            print("BYE BRO")
            self.side_panel.quit()
            self.side_panel_open = False

        else:
            print("HI BRO")
            self.side_panel.run()
            self.side_panel_open = True


if __name__ == "__main__":
    bar = StatusBar()
    app = Application("bar", bar)
    app.set_stylesheet_from_file(get_relative_path("./style.css"))

    app.run()
