from fabric.widgets.box import Box 
from fabric.widgets.label import Label

from fabric import Fabricator

from fabric.utils import get_relative_path

from widgets.circular_indicator import CircularIndicator
from user.icons import Icons

import gi 
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import psutil

from fabric.utils import invoke_repeater

class BatterySingle(Box):
    def __init__(self, size=24, **kwargs) -> None:
        super().__init__(orientation="h", **kwargs)

        self.battery_progress_bar = CircularIndicator(
            size=size,
            name="battery",
            icon=Icons.BAT.value,
            style="margin: 12px;"
        )

        self.add(self.battery_progress_bar)

        invoke_repeater(1000, self.update_status)

    def update_status(self) -> bool:
        if not (bat_sen := psutil.sensors_battery()):
            self.battery_progress_bar.progress_bar.value = 0.42
            self.battery_progress_bar.label.set_label("INF%")
        else:
            if psutil.sensors_battery().power_plugged:
                self.battery_progress_bar.icon.set_label(Icons.CHARGING.value)
            else:
                self.battery_progress_bar.icon.set_label(Icons.BAT.value)
            self.battery_progress_bar.progress_bar.value = bat_sen.percent / 100
            self.battery_progress_bar.label.set_label(str(int(bat_sen.percent)) + "%")


        return 1

