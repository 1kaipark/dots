from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.datetime import DateTime

from fabric import Fabricator

import os
from loguru import logger

import time, psutil

from user.icons import Icons


def get_profile_picture_path() -> str | None:
    path = os.path.expanduser("~/Pictures/profile.jpg")
    if not os.path.exists(path):
        path = os.path.expanduser("~/.face")
    if not os.path.exists(path):
        logger.warning("put yo fuckin picture in ~/Pictures/profile.jpg or ~/.face")
        path = None
    return path


class Profile(Box):
    @staticmethod
    def psutil_uptime(f: Fabricator):
        while 1:
            elapsed = int(time.time() - psutil.boot_time())
            days, remainder = divmod(elapsed, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            yield f"{days}d {hours}h {minutes}m"
            time.sleep(60)

    cool_fabricator = Fabricator(poll_from=psutil_uptime, stream=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="h", h_expand=True, **kwargs)

        self.profile_pic = Box(
            name="profile-pic",
            style=f'background-image: url("file://{get_profile_picture_path() or ""}")',
        )
        self._labels_container = Box(
            orientation="v",
            h_align="fill",
            v_align="center",
            h_expand=True,
            v_expand=True,
        )
        self.username = Label(
            label=os.getlogin().title(),
            style_classes="username",
            h_align="start",
        )

        self.date = DateTime(
            formatters=(Icons.CALENDAR.value + " %A %m/%d/%Y"), style_classes="date", 
            h_align="start",
        )

        self.uptime = Label(label="", style_classes="uptime", 
            h_align="start",)
        self.cool_fabricator.connect(
            "changed",
            self.update_status
        )

        self.add(self.profile_pic)
        self._labels_container.add(self.username)
        self._labels_container.add(self.date)
        self._labels_container.add(self.uptime)
        self.add(self._labels_container)

    def update_status(self, f: Fabricator, value: float):
        self.uptime.set_label(Icons.STOPWATCH.value + " " + str(value))
