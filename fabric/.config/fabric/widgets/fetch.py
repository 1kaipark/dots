

# https://github.com/Titaniumtown/pyfetch/blob/master/pyfetch.py
import os
from subprocess import Popen, PIPE, DEVNULL

from fabric.widgets.box import Box 
from fabric.widgets.label import Label 

from fabric import Fabricator

from fabric.utils import get_relative_path

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
        
