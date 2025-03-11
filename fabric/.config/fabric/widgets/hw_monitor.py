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

        weather_widgets = []
        self.weather_temp_label = Label(
            name="weather-temp",
            label="⛅️°C",
        )

        # self.weather_desc_label = DynamicLabel(name="weather-desc", label="Weather", max_len=15, independent_repeat=True)

        self.weather_desc_label = Gtk.Label(name="weather-desc", label="weather")
        self.weather_desc_label.set_line_wrap(True)
        self.weather_desc_label.set_max_width_chars(18)

        weather_widgets.append(self.weather_temp_label)
        weather_widgets.append(self.weather_desc_label)

        weather = Box(children=weather_widgets, orientation="v")

        self.add(weather)

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

        weather_fabricator = Fabricator(
            interval=3600*1000*4,
            poll_from=get_relative_path("../scripts/fetch_weather.sh"),
            on_changed=self.update_weather_display,
        )

#        cpu_boost_fabricator = Fabricator(
#            interval=1000,
#            poll_from=get_relative_path("../scripts/hw_mon.sh"),
#            on_changed=lambda f, v: (self.cpu_temp_progress_bar.icon.set_label(Icons.BOOST.value)) if v==0 else (self.cpu_temp_progress_bar.icon.set_label(Icons.TEMP.value))
#        )
#
        # curr_weather = fetch_weather()
        return 1

    def update_weather_display(self, f, v):
        code, temp_C, desc = v.split("|")
        icon = WEATHER_CODES[code]
        self.weather_temp_label.set_label(icon + " " + temp_C + "°C")
        self.weather_desc_label.set_label(desc)

