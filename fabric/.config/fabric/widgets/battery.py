import psutil 

from loguru import logger
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.circularprogressbar import CircularProgressBar




class BatteryDisplay(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.battery_percentage = Label(
            name="battery-percentage",
        label="test",
            justification="left",
        ellipsization="end",
        )

        self.charging = psutil.sensors_battery().power_plugged

        self.battery_progress = CircularProgressBar(
            name="battery-progress-bar", pie=False, size=24,        )

        self.icon = Label(
            "󰁹", style="margin: 0px 6px 0px 6px; font-size: 12px;",
        )

        self.battery_overlay = Overlay(
            child=self.battery_progress,
            overlays=[
                self.icon
            ],
        )

        self.add(self.battery_percentage)
        self.add(self.battery_overlay)

    def update_percentage(self) -> bool:
        self.charging = psutil.sensors_battery().power_plugged
        curr_percent = psutil.sensors_battery().percent
        self.battery_progress.value = curr_percent / 100
        self.battery_percentage.set_label(" " + str(int(curr_percent)) + "% ")
        
        icon = ""
        if curr_percent < 33:
            icon = "󱊡"
        elif 33 <= curr_percent <= 66:
            icon = "󱊢"
        else:
            icon = "󱊣"

        if self.charging:
            self.icon.set_label("󰂄")
            self.battery_progress.set_style("border-color: @green;")
        else:
            self.icon.set_label(icon)
            self.battery_progress.set_style("border-color: @sky;")
        return True


