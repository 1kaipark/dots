from fabric.widgets.button import Button 
from fabric.widgets.box import Box 
from fabric.widgets.wayland import WaylandWindow as Window

from ..user.icons import Icons 

from .bluetooth import BluetoothWindow

from gi.repository import Gtk

class NetworkControls(Gtk.Grid):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


        self.wifi_button = Button(
            label=Icons.WIFI.value + " ...",
            on_clicked=self.show_wifi_menu,
        )

        self.bt_button = Button(
            label=Icons.BLUETOOTH.value + " ...",
            on_clicked=self.show_bluetooth_menu,
        )

        self.bluetooth_menu = BluetoothWindow(name="bluetooth-window")

        self.attach(self.wifi_button, 0, 0, 1, 1)
        self.attach(self.bt_button, 0, 1, 1, 1)

        self.bluetooth_menu.bluetooth_connections.client.connect(
            "notify::enabled",
            lambda *_: self.bt_button.set_label(
                Icons.BLUETOOTH.value + " ON" if (self.bluetooth_menu.bluetooth_connections.client.enabled) else Icons.BLUETOOTH.value + " OFF"
            )
        )

    def show_wifi_menu(self, *_): ...
    def show_bluetooth_menu(self, *_):
        if self.bluetooth_menu.is_visible(): self.bluetooth_menu.hide()
        else: self.bluetooth_menu.show()

