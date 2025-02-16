from enum import Enum
from fabric.utils import get_relative_path

class Commands(Enum):
    LAUNCHER = "rofi -show drun"
    LOGOUT = "hyprctl dispatch exit"
    REBOOT = "reboot"
    SHUTDOWN = "shutdown now"
    WALLPAPER = get_relative_path("../scripts/wpswitch.sh")
    TERM = "ghostty"
    BROWSER = "firefox"
    SETTINGS = "systemsettings"
    FILES = "dolphin"


