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
    MUTE = "wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"
    NOTES = "obsidian --ozone-platform=wayland --ozone-platform-hint=auto --enable-features=UseOzonePlatform,WaylandWindowDecorations %U"
    EDITOR = "code --enable-features=UseOzonePlatform,WaylandWindowDecorations --ozone-platform-hint=auto"
    MUSIC = "spotify-launcher"
    WIFI_MENU = get_relative_path("../scripts/rofi-wifi-menu.sh")
    BLUETOOTH = get_relative_path("../scripts/rofi-bluetooth.sh")
    NOTIFICATIONS = "swaync-client -t "


