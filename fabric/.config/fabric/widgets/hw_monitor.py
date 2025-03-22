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
import os, time
from subprocess import Popen, PIPE, DEVNULL


def run_command(command):
    process = Popen(
        command, stdout=PIPE, universal_newlines=True, shell=True, stderr=DEVNULL
    )
    stdout, stderr = process.communicate()
    del stderr
    return stdout


class Indicator(Box):
    def __init__(self, icon: str, **kwargs):
        super().__init__(orientation="v", **kwargs)

        self.icon = Label(label=icon)
        self.label = Label()

        self.add(self.icon)
        self.add(self.label)


class HWMonitor(Box):
    @staticmethod
    def psutil_poll(f: Fabricator):
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        while 1:
           yield {
               "cpu_usage": int(psutil.cpu_percent()),
               "cpu_temp": int(psutil.sensors_temperatures()["thinkpad"][0].current),
               "ram_percent": (ram.percent / 100),
               "ram_usage": (ram.total - ram.available) / (1024**3),
               "disk_percent": disk.percent / 100,
               "disk_usage": disk.used / (1024**3),
           }

           time.sleep(1)

    cool_fabricator = Fabricator(poll_from=psutil_poll, stream=True, default_value={})


    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="h", h_align="center", h_expand=True, **kwargs)

        self.cpu_progress_bar = CircularIndicator(
            name="hwmon-item",
            style_classes="blue",
            icon=Icons.CPU.value,
        )

        self.ram_progress_bar = CircularIndicator(
            name="hwmon-item",
            style_classes="yellow",
            icon=Icons.MEM.value,
        )

        self.cpu_temp_progress_bar = CircularIndicator(
            name="hwmon-item",
            style_classes="red",
            icon=Icons.TEMP.value,
        )

        self.disk_progress_bar = CircularIndicator(
            name="hwmon-item",
            style_classes="green",
            icon=Icons.DISK.value, 
        )
        
        self._container = Box(h_align="fill", h_expand=True, spacing=36)
        self._container.add(self.cpu_progress_bar)
        self._container.add(self.cpu_temp_progress_bar)
        self._container.add(self.ram_progress_bar)
        self._container.add(self.disk_progress_bar)
        
        self.add(self._container)
        
        self.cool_fabricator.connect(
            "changed",
            self.update_status
        )

    def update_status(self, f: Fabricator, value: dict):
        self.cpu_progress_bar.progress_bar.set_value(value['cpu_usage']/100)
        self.cpu_progress_bar.label.set_label(str(value['cpu_usage'])+"%")
        
        self.cpu_temp_progress_bar.progress_bar.set_value(value['cpu_temp']/100)
        self.cpu_temp_progress_bar.label.set_label(str(value['cpu_temp'])+"°C")
        
        self.ram_progress_bar.progress_bar.set_value(value['ram_percent'])
        self.ram_progress_bar.label.set_label(f"{value['ram_usage']:.1f}GB")
        
        self.disk_progress_bar.progress_bar.set_value(value['disk_percent'])
        self.disk_progress_bar.label.set_label(f"{value['disk_usage']:.0f}GB")
