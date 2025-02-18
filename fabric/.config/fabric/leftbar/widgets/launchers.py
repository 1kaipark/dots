from fabric.widgets.box import Box 
from fabric.widgets.button import Button

from fabric.utils import exec_shell_command_async

from ..user.icons import Icons 
from ..user.commands import Commands

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

