
# TODO: add handling for urgent

from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.button import Button

from fabric.utils import get_relative_path, idle_add

from fabric import Application 

import gi 
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from i3ipc import Connection, Event

import threading

from loguru import logger

from typing import Iterable

WS_ICONS = ('一', '二', '三', '四', '五', '六', '七', '八', '九', '十')

class WorkspaceButton(Button):
    def __init__(self, id: int, icons: Iterable[str] | None = None, **kwargs) -> None:
        self.id = id
        if icons:
            label = icons[id - 1]
        else: 
            label = str(id)
        super().__init__(label=label, **kwargs)

class Workspaces(Box):
    def __init__(self, orientation, **kwargs) -> None:
        super().__init__(
            name="workspaces",
            visible=True,
            all_visible=True,
            h_align="center",
            v_align="fill",
            **kwargs
        )

        self.buttons: dict[int, Button] = {}

        self.sway = Connection() 
        self.sway.on(Event.WORKSPACE, self.on_workspace)

        self._container = Box(
            name="workspaces-box",
            spacing=10,
            orientation=orientation,
        )
        self.add(self._container)

        self.load_workspaces()

        threading.Thread(target=self.sway.main, args=()).start()

    def on_workspace(self, sway, event):
        match event.change:
            case "focus": 
#                self.highlight_button(id=int(event.current.num), old=int(event.old.num))
                idle_add(self.highlight_button, (event))
            case "init": 
                idle_add(self.insert_button, (int(event.current.num)))
            case "empty":
                idle_add(self.remove_button,  (int(event.current.num)))


    def load_workspaces(self):
        open_workspaces: tuple[int, ...] = sorted(
                tuple(
                    int(ws.num)
                    for ws in self.sway.get_workspaces()
                )
            )

        for ws in open_workspaces:
            btn = WorkspaceButton(id=ws, icons=WS_ICONS, name="workspaces-button")
            btn.connect("clicked", self.on_button_press)
            self.buttons[ws] = btn
            self._container.add(btn)

        if active_workspace := self.sway.get_tree().find_focused().workspace().num:
            self.buttons[active_workspace].add_style_class("active")


    def insert_button(self, id: int):
        logger.info("[Workspaces] Inserting workspace {}".format(str(id)))
        btn = WorkspaceButton(id=id, icons=WS_ICONS, name="workspaces-button")
        btn.connect("clicked", self.on_button_press)

        self.buttons[id] = btn
        self._container.add(btn)

        self.reorder_buttons()

    def remove_button(self, id: int):
        logger.info("[Workspaces] Removing workspace {}".format(str(id)))
        self.buttons[id].destroy()
        self.buttons.pop(id)

    def reorder_buttons(self):
        for _, child in sorted(self.buttons.items(), key=lambda i: i[0]):
            self._container.reorder_child(child, (int(child.id) - 1))
        return

    def highlight_button(self, event):
        id = int(event.current.num)
        old = int(event.old.num)
        logger.info("[Workspaces] Active workspace {}".format(str(id)))
        self.buttons[id].add_style_class("active")
        if old:
            self.buttons[old].remove_style_class("active")

    def on_button_press(self, button):
        logger.info("[Workspaces] Active workspace {}".format(str(id)))
        self.sway.command(f"workspace {button.id}")
        
