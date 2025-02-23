from fabric.widgets.button import Button 
from fabric.widgets.box import Box 
from fabric.widgets.wayland import WaylandWindow as Window

from ..user.icons import Icons 
from ..user.commands import Commands

from .bluetooth import BluetoothWindow
from .popup import ConfirmationBox

from fabric.utils import exec_shell_command_async

from gi.repository import Gtk

class NetworkControls(Gtk.Grid):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


        self.wifi_button = Button(
            label=Icons.WIFI.value,
            on_clicked=self.show_wifi_menu,
            style="background-color: @mauve;"
        )

        self.bt_button = Button(
            label=Icons.BLUETOOTH.value,
            on_clicked=self.show_bluetooth_menu,
            style="background-color: @blue;"
        )

        self.notis_button = Button(
            label=Icons.NOTIFICATIONS.value,
            on_clicked=self.toggle_notifications,
            style="background-color: @yellow;"
        )

        self.bluetooth_menu = BluetoothWindow(name="bluetooth-window")

        self.attach(self.wifi_button, 0, 0, 1, 1)
        self.attach(self.bt_button, 0, 1, 1, 1)
        self.attach(self.notis_button, 0, 2, 1, 1)

        self.bluetooth_menu.bluetooth_connections.client.connect(
            "notify::enabled",
            lambda *_: self.bt_button.set_style(
                "background-color: @blue;" if (self.bluetooth_menu.bluetooth_connections.client.enabled) else "background-color: var(--module-bg);"
            )
        )

    def show_wifi_menu(self, *_): 
        ConfirmationBox(self, "notimplemented xD", "exit", name="popup-window").show()
    def show_bluetooth_menu(self, *_):
        if self.bluetooth_menu.is_visible(): self.bluetooth_menu.hide()
        else: self.bluetooth_menu.show()

    def toggle_notifications(self, *_): 
        exec_shell_command_async(Commands.NOTIFICATIONS.value)

