from fabric.widgets.box import Box 
from fabric.widgets.label import Label

from fabric import Fabricator

from fabric.utils import get_relative_path

from widgets.circular_indicator import CircularIndicator
from widgets.separator import Separator
from user.icons import Icons

import gi 
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import psutil

from utils.weather import WEATHER_CODES

# https://github.com/Titaniumtown/pyfetch/blob/master/pyfetch.py
import os
from subprocess import Popen, PIPE, DEVNULL


def run_command(command):
    process = Popen(
        command, stdout=PIPE, universal_newlines=True, shell=True, stderr=DEVNULL
    )
    stdout, stderr = process.communicate()
    del stderr
    return stdout


def get_os_name() -> str:
    if os.path.isfile("/etc/os-release"):
        os_file = "/etc/os-release"

    pretty_name = (
        run_command(("cat " + os_file + " | grep 'PRETTY_NAME'"))
        .replace("PRETTY_NAME=", "")
        .replace('''"''', "")
    )
    return pretty_name.strip()


class Fetch(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="v", v_expand=True, v_align="center", **kwargs)

        self.os_label = Label(name="label-a")
        self.uptime_label = Label(name="label-b")
        self.pkg_label = Label(name="label-c")
        self.disk_label = Label(name="label-d")

        for label in [
            self.os_label,
            self.uptime_label,
            self.pkg_label,
            self.disk_label,
        ]:
            self.add(label)

        self.update_status()

    def update_status(self) -> bool:
        os = get_os_name().strip().lower()
        self.os_label.set_label(f"os • {os}")

        uptime_fabricator = Fabricator(
            interval=500,
            poll_from=get_relative_path("../scripts/uptime.sh"),
            on_changed=lambda f, v: self.uptime_label.set_label(
                f"up • {v}"
            ),
        )

        pkgs_fabricator = Fabricator(
            interval=5000,
            poll_from=get_relative_path("../scripts/package_count.sh"),
            on_changed=lambda f, v: self.pkg_label.set_label(f"pkgs • {v}"),
        )

        df_fabricator = Fabricator(
            interval=5000,
            poll_from=get_relative_path("../scripts/disk_usage.sh"),
            on_changed=lambda f, v: self.disk_label.set_label(f"df • {v}"),
        )
        

class HWMonitor(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="h", **kwargs)

        self.battery_progress_bar = CircularIndicator(
            name="battery",
            icon=Icons.BAT.value,
        )

        self.cpu_progress_bar = CircularIndicator(
            name="cpu",
            icon=Icons.CPU.value,
        )

        self.ram_progress_bar = CircularIndicator(
            name="ram",
            icon=Icons.MEM.value,
        )

        self.cpu_temp_progress_bar = CircularIndicator(
            name="temp",
            icon=Icons.TEMP.value,
        )

        progress_grid = Gtk.Grid()
        progress_grid.attach(self.battery_progress_bar, 0, 0, 1, 1)
        progress_grid.attach(self.cpu_progress_bar, 1, 0, 1, 1)
        progress_grid.attach(self.ram_progress_bar, 2, 0, 1, 1)
        progress_grid.attach(self.cpu_temp_progress_bar, 3, 0, 1, 1)

        self.add(progress_grid)

        self.add(Separator())
        self.add(Fetch())

    def update_status(self) -> bool:
        cpu_percent = int(psutil.cpu_percent())
        self.cpu_progress_bar.progress_bar.value = cpu_percent / 100
        self.cpu_progress_bar.label.set_label(str(cpu_percent) + "%")
        
        ram = psutil.virtual_memory()
        ram_usage = (ram.total - ram.available)/(1024**3)
        self.ram_progress_bar.progress_bar.value = ram.percent / 100
        self.ram_progress_bar.label.set_label(f"{ram_usage:.1f} GB")

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


        cpu_temp = int(psutil.sensors_temperatures()["thinkpad"][0].current)
        self.cpu_temp_progress_bar.progress_bar.value = cpu_temp / 100
        self.cpu_temp_progress_bar.label.set_label(str(cpu_temp) + "°C")


