from fabric.widgets.box import Box 
from fabric.widgets.button import Button 
from fabric.utils import exec_shell_command_async

from user.icons import Icons
from user.commands import Commands
from widgets.popup import ConfirmationBox

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class PowerMenu(Gtk.Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, **kwargs)
        self.set_halign(Gtk.Align.CENTER)
        self.set_hexpand(True)
        self.set_spacing(48)

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

