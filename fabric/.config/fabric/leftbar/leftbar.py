"""
a basic and minimal control center made in fabric/Gtk.

TODO : desparately needs a refactor but who cares lmao
"""


import os, psutil, time

from fabric import Application, Fabricator
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.widgets.button import Button
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.datetime import DateTime
from fabric.widgets.overlay import Overlay
from fabric.widgets.scale import Scale

from fabric.audio.service import Audio
from .services.brightness import Brightness

from fabric.utils import get_relative_path, invoke_repeater, exec_shell_command_async
from .widgets.media import NowPlaying
from .widgets.popup import ConfirmationBox
from .widgets.dynamic_label import DynamicLabel

from .user.icons import Icons
from .user.commands import Commands

import sys

from loguru import logger

from .utils.weather import WEATHER_CODES

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import requests

"""
CSS CLASSES
* profile-pic
* button-icon-large
* button-icon-small-a through c
* button-icon-smallest
* clock-a
* clock-b
* clock-c
* progress-bar-red, green, yellow, etc
* label-red, ...
* scale-a through c
* label-a through c (colors)
"""


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



def get_profile_picture_path() -> str | None:
    path = os.path.expanduser("~/Pictures/profile.jpg")
    if not os.path.exists(path):
        path = os.path.expanduser("~/.face")
    if not os.path.exists(path):
        logger.warning("put yo fuckin picture in ~/Pictures/profile.jpg or ~/.face")
        path = None
    return path


class Profile(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="v", h_expand=True, **kwargs)

        self.profile_pic = Box(
            name="profile-pic",
            style=f'background-image: url("file://{get_profile_picture_path() or ""}")',
        )
        self.username = Label(
            label=os.getlogin().title(),
            style="margin: 2px 6px 2px 6px;",
            name="greeter-label",
        )

        self.add(self.profile_pic)
        self.add(self.username)


class PowerMenu(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="h", **kwargs)

        self.logout = Button(
            name="button-icon",
            label=Icons.LOGOUT.value,
            on_clicked=lambda *_: ConfirmationBox(
                parent=self,
                prompt="Logout?",
                command=Commands.LOGOUT.value,
                name="popup-window",
            ),
        )

        self.reboot = Button(
            name="button-icon",
            label=Icons.REBOOT.value,
            on_clicked=lambda *_: ConfirmationBox(
                parent=self,
                prompt="Reboot?",
                command=Commands.REBOOT.value,
                name="popup-window",
            )
        )

        self.shutdown = Button(
            name="button-icon",
            label=Icons.POWER.value,
            on_clicked=lambda *_: ConfirmationBox(
                parent=self,
                prompt="Shutdown?",
                command=Commands.SHUTDOWN.value,
                name="popup-window",
            )
        )

        self.wallpaper_switch = Button(
            name="button-icon",
            label=Icons.PIC.value,
            on_clicked=lambda *_: exec_shell_command_async(Commands.WALLPAPER.value),
        )

        self.add(self.logout)
        self.add(self.reboot)
        self.add(self.shutdown)
        self.add(self.wallpaper_switch)


class Clock(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="v", **kwargs)
        self.time = DateTime(formatters=("%H %M"), name="clock-a")
        self.date = DateTime(formatters=("%m %d"), name="clock-b")
        self.day = DateTime(formatters=("%A, %B"))

        self.add(self.time)
        self.add(self.date)
        self.add(self.day)


class CircularIndicator(Box):
    def __init__(
        self,
        size: int = 48,
        label: str = "0",
        icon: str = "",
        orientation: str = "v",  # too lazy to import literal rn TODO TODO TODO
        **kwargs,
    ) -> None:
        super().__init__(orientation=orientation, **kwargs)
        self.progress_bar = CircularProgressBar(
            name="circular-bar",
            pie=False,
            size=size,
        )

        self.icon = Label(
            label=icon,
            style="margin: 0px 6px 0px 8px; font-size: {}px;".format(size // 3),
        )

        self.label = Label(
            label=label,
        )

        overlay = Overlay(child=self.progress_bar, overlays=[self.icon], **kwargs)
        self.add(overlay)
        self.add(self.label)


class HWMonitor(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="h", **kwargs)

        self.battery_progress_bar = CircularIndicator(
            name="battery",
            icon=Icons.BAT.value,
        )

        self.add(self.battery_progress_bar)

        self.cpu_progress_bar = CircularIndicator(
            name="cpu",
            icon=Icons.CPU.value,
        )

        self.add(self.cpu_progress_bar)

        self.ram_progress_bar = CircularIndicator(
            name="ram",
            icon=Icons.MEM.value,
        )

        self.add(self.ram_progress_bar)

        self.cpu_temp_progress_bar = CircularIndicator(
            name="temp",
            icon=Icons.TEMP.value,
        )

        self.cpu_temp_label = Label(label="0°C", name="cpu-temp")
        cpu_temp_box = Box(
            children=[
                Label(
                    label=Icons.TEMP.value, name="label-red", style="font-size: 36px;"
                ),
                self.cpu_temp_label,
            ]
        )

        self.add(self.cpu_temp_progress_bar)

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
            interval=1000000,
            poll_from=get_relative_path("./scripts/fetch_weather.sh"),
            on_changed=self.update_weather_display,
        )

        # curr_weather = fetch_weather()
        return 1

    def update_weather_display(self, f, v):
        logger.info(v)
        code, temp_C, desc = v.split("|")
        icon = WEATHER_CODES[code]
        self.weather_temp_label.set_label(icon + " " + temp_C + "°C")
        self.weather_desc_label.set_label(desc)


class ScaleControl(Box):
    def __init__(
        self,
        label,
        button_callback=lambda *_: 1,
        **kwargs,
    ) -> None:
        super().__init__(orientation="h", **kwargs)
        self.scale = Scale(
            min_value=0,
            max_value=100,
            value=100,
            orientation="h",
        )
        self.label = Button(
            label=label,
            on_clicked=button_callback
        )

        self.add(self.label)
        self.add(self.scale)


class Controls(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="v", **kwargs)
        self.audio = Audio(on_speaker_changed=self.on_speaker_changed)
        self.audio.connect("notify::speaker", self.on_speaker_changed)

        self.brightness = Brightness().get_initial()
        self.brightness.connect("screen", self.on_brightness_changed)

        self.volume_box = ScaleControl(
            label=Icons.VOL.value,
            name="scale-a",
            button_callback=lambda *_: exec_shell_command_async("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")
        )

        self.volume_box.scale.connect("value-changed", self.change_volume)

        self.brightness_box = ScaleControl(label=Icons.BRIGHTNESS.value, name="scale-b")

        self.brightness_box.scale.connect(
            "value-changed", lambda *_: self.update_brightness()
        )

        self.add(self.volume_box)
        self.add(self.brightness_box)

        self.sync_with_audio()
        self.update_brightness()

    def sync_with_audio(self):
        if not self.audio.speaker:
            return
        volume = round(self.audio.speaker.volume)
        self.volume_box.scale.set_value(volume)

    def change_volume(self, scale):
        if not self.audio.speaker:
            return
        volume = scale.value
        if 0 <= volume <= 100:
            self.audio.speaker.set_volume(volume)

    def on_speaker_changed(self, *_):
        if not self.audio.speaker:
            return
        self.audio.speaker.connect("notify::volume", self.update_volume)

        self.update_volume()

    def update_volume(self, *_):
        if not self.audio.speaker:
            return

        if self.audio.speaker.muted:
            self.volume_box.label.set_label(Icons.VOL_MUTE.value)
        else:
            self.volume_box.label.set_label(Icons.VOL.value)

        volume = round(self.audio.speaker.volume)
        self.volume_box.scale.set_value(volume)

    def update_brightness(self, *_):
        try:
            norm_brightness = round(
                (self.brightness.screen_brightness / self.brightness.max_screen) * 100
            )
            self.brightness_box.scale.set_value(norm_brightness)
        except Exception as e:
            logger.error("Brightness is fuked bro: {}".format(str(e)))

    def on_brightness_changed(self, sender, value, *_):
        norm_brightness = round((value / self.brightness.max_screen) * 100)
        self.brightness_box.scale.set_value(norm_brightness)


class Fetch(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="v", **kwargs)

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
            poll_from=get_relative_path("./scripts/uptime.sh"),
            on_changed=lambda f, v: self.uptime_label.set_label(
                f"up • {v}"
            ),
        )

        pkgs_fabricator = Fabricator(
            interval=5000,
            poll_from=get_relative_path("./scripts/package_count.sh"),
            on_changed=lambda f, v: self.pkg_label.set_label(f"pkgs • {v}"),
        )

        df_fabricator = Fabricator(
            interval=5000,
            poll_from=get_relative_path("./scripts/disk_usage.sh"),
            on_changed=lambda f, v: self.disk_label.set_label(f"df • {v}"),
        )
        
class Launchers(Box):
    def __init__(self, **kwargs) -> None: 
        super().__init__(orientation="h", **kwargs)
        
        self.launcher = Button(
            name="button-icon",
            label=Icons.SEND.value,
            on_clicked=lambda *_: exec_shell_command_async(Commands.LAUNCHER.value)
        )

        self.settings = Button(
            name="button-icon",
            label=Icons.SETTINGS.value,
            on_clicked=lambda *_: exec_shell_command_async(Commands.SETTINGS.value)
        )
        
        self.term = Button(
            name="button-icon",
            label=Icons.TERM.value,
            on_clicked=lambda *_: exec_shell_command_async(Commands.TERM.value)
        )
        
        self.browser = Button(
            name="button-icon",
            label=Icons.BROWSER.value,
            on_clicked=lambda *_: exec_shell_command_async(Commands.BROWSER.value)
        )
        
        self.files = Button(
            name="button-icon",
            label=Icons.FILES.value,
            on_clicked=lambda *_: exec_shell_command_async(Commands.FILES.value)
        )

        
        self.add(self.launcher)
        self.add(self.term)
        self.add(self.browser)
        self.add(self.files)
        self.add(self.settings)

class QuoteDisplay(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.quote_label = Gtk.Label()
        self.quote_label.set_line_wrap(True)

        self.add(self.quote_label)

        _ = Fabricator(
            interval=3600*1000,
            default_value="Hi Bro - anonymous",
            poll_from=get_relative_path("./scripts/quotes.sh"),
            on_changed=lambda f, v: (
                self.quote_label.set_label(v)
            ) 
        )


        
class Separator(Label):
    def __init__(self, wide: bool = False, **kwargs) -> None:
        delim = "|" if not wide else " | "
        super().__init__(name="separator", label=delim, **kwargs)


class ControlCenter(Window):
    def __init__(self, **kwargs):
        super().__init__(
            layer="overlay",
            title="control-center",
            anchor="top left",
            margin="8px 8px 8px 8px",
            exclusivity="none",
            visible=False,
            all_visible=False,
            keyboard_mode="on-demand",
#            on_key_press_event=lambda _, event: self.application.quit()
            on_key_press_event=lambda _, event: self.hide()
            if event.keyval == 65307
            else True,  # handle ESC = exit
            **kwargs,
        )

        #  ____  _____ _____ ___ _   _ _____
        # |  _ \| ____|  ___|_ _| \ | | ____|
        # | | | |  _| | |_   | ||  \| |  _|
        # | |_| | |___|  _|  | || |\  | |___
        # |____/|_____|_|   |___|_| \_|_____|
        #
        # __        _____ ____   ____ _____ _____ ____
        # \ \      / /_ _|  _ \ / ___| ____|_   _/ ___|
        #  \ \ /\ / / | || | | | |  _|  _|   | | \___ \
        #   \ V  V /  | || |_| | |_| | |___  | |  ___) |
        #    \_/\_/  |___|____/ \____|_____| |_| |____/
        #

        self.profile = Profile(name="outer-box")

        self.power_menu = PowerMenu(name="power-menu")

        self.clock = Clock()

        self.hwmon = HWMonitor(name="hw-mon")  # this goes in center_widgets

        self.controls = Controls(name="controls")  # sliders for vol, brightness

        self.fetch = Fetch(name="fetch")  # idea: cool neofetch polling

        self.media = NowPlaying(
            name="media", max_len=15, cava_bars=24
        )  
        
        self.launchers = Launchers(name="launchers")

        self.quote_display = QuoteDisplay(name="quote-display")

        self.top_right = Box(
            children=[self.power_menu, self.clock],
            orientation="v",
            name="outer-box"
        )

        self.header = Box(
            orientation="h",
            children=[self.profile, self.top_right],
        )

        self.row_1 = Box(orientation="h", children=[self.hwmon], name="outer-box")
        self.row_2 = Box(orientation="h", children=[self.controls], name="outer-box")
        self.row_3 = Box(
            orientation="h", children=[self.fetch, self.media], name="outer-box"
        )
        self.row_4 = Box(
            orientation="h", children=[self.launchers], name="outer-box"
        )

        self.row_5 = Box(
            orientation="h", children=[self.quote_display], name="outer-box"
        )

        self.widgets = [self.header, self.row_1, self.row_2, self.row_3, self.row_4, self.row_5]

        self.add(
            Box(
                name="window",
                orientation="v",
                spacing=24,
                children=self.widgets,
            ),
        )
        self.show_all()

        invoke_repeater(1000, self.update_status)

    def update_status(self) -> bool:
        self.hwmon.update_status()
        return 1


if __name__ == "__main__":
    control_center = ControlCenter()
    app = Application("side-panel", control_center)
    app.set_stylesheet_from_file(get_relative_path("./style.css"))

    app.run()
