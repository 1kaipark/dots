
import os, psutil

from fabric import Application
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.wayland import WaylandWindow as Window

from widgets.battery import BatteryDisplay

from fabric.utils import get_relative_path, invoke_repeater


class CPUTemp(Box):
    def __init__(self, sensor: str = "thinkpad", **kwargs) -> None:
        super().__init__(**kwargs)

        self.sensor = sensor

        self.icon_label = Label(" ", style="color: @red;")

        self.temp_label = Label("󰔄")

        self.add(self.icon_label)
        self.add(self.temp_label)


    def update_temps(self) -> bool:
        curr_temp = psutil.sensors_temperatures()[self.sensor][0].current 
        
        self.temp_label.set_label(str(int(curr_temp)) + "󰔄")

        return True

