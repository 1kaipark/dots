from fabric.widgets.box import Box 
from fabric.widgets.button import Button

from fabric.utils import exec_shell_command_async

from user.icons import Icons 
from user.commands import Commands

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# class Launchers(Box):
#     def __init__(self, **kwargs) -> None: 
#         super().__init__(orientation="h", **kwargs)
#         
#         self.launcher = Button(
#             name="button-icon",
#             label=Icons.SEND.value,
#             on_clicked=lambda *_: exec_shell_command_async(Commands.LAUNCHER.value)
#         )
# 
#         self.settings = Button(
#             name="button-icon",
#             label=Icons.SETTINGS.value,
#             on_clicked=lambda *_: exec_shell_command_async(Commands.SETTINGS.value)
#         )
#         
#         self.term = Button(
#             name="button-icon",
#             label=Icons.TERM.value,
#             on_clicked=lambda *_: exec_shell_command_async(Commands.TERM.value)
#         )
#         
#         self.browser = Button(
#             name="button-icon",
#             label=Icons.BROWSER.value,
#             on_clicked=lambda *_: exec_shell_command_async(Commands.BROWSER.value)
#         )
#         
#         self.files = Button(
#             name="button-icon",
#             label=Icons.FILES.value,
#             on_clicked=lambda *_: exec_shell_command_async(Commands.FILES.value)
#         )
# 
#         
#         self.add(self.launcher)
#         self.add(self.term)
#         self.add(self.browser)
#         self.add(self.files)
#         self.add(self.settings)
# 
class Launchers(Gtk.Grid):
    def __init__(self, **kwargs) -> None: 
        super().__init__(**kwargs)
        
        self.launcher = Button(
            name="button-icon",
            label=Icons.LAUNCHER.value,
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

        self.notes = Button(
            name="button-icon",
            label=Icons.NOTES.value,
            on_clicked=lambda *_: exec_shell_command_async(Commands.NOTES.value)
        )

        self.editor = Button(
            name="button-icon",
            label=Icons.EDITOR.value,
            on_clicked=lambda *_: exec_shell_command_async(Commands.EDITOR.value)
        )

        self.music = Button(
            name="button-icon",
            label=Icons.MUSIC.value,
            on_clicked=lambda *_: exec_shell_command_async(Commands.MUSIC.value)
        )

        self.attach(self.launcher, 0, 0, 1, 1)
        self.attach(self.term, 0, 1, 1, 1)
        self.attach(self.browser, 1, 0, 1, 1)
        self.attach(self.files, 1, 1, 1, 1)
        self.attach(self.settings, 2, 0, 1, 1)
        self.attach(self.notes, 2, 1, 1, 1)
        self.attach(self.editor, 3, 0, 1, 1)
        self.attach(self.music, 3, 1, 1, 1)

        self.set_column_spacing(84)
        self.set_row_spacing(12)

