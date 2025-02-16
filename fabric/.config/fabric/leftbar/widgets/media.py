from fabric import Application, Fabricator

from fabric.widgets.wayland import WaylandWindow as Window

from fabric.widgets.button import Button 
from fabric.widgets.label import Label 
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox

from fabric.widgets.image import Image 

from fabric.utils import exec_shell_command_async, get_relative_path, invoke_repeater

from .cava import CavaWidget 
from .dynamic_label import DynamicLabel

import gi 
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, GLib

import os

from loguru import logger

now_playing_fabricator = Fabricator(poll_from=r"playerctl -F metadata --format '{{album}}\n{{artist}}\n{{status}}\n{{title}}\n{{volume}}\n{{mpris:artUrl}}\n'", stream=True)

class Spacer(Label):
    def __init__(self, n_spaces: int = 1, **kwargs):
        super().__init__(label=" "*n_spaces)

class NowPlaying(Box):
    def __init__(self, max_len: int = 25, cava_bars: int = 12, **kwargs):
        self._status: str = "" 

        self.max_len = max_len 

        self.label = DynamicLabel(
            label="not playing",
            max_len=max_len,
            independent_repeat=True,
            refresh_rate=500,
            separator=" | ",
        )


        self.title_box = Box(
            children=[
                self.label,CavaWidget(name="cava-box", bars=cava_bars),
            ],
            orientation='v',
            name="media-title"
        )
        
        prev_icon = Image(icon_name="media-seek-backward-symbolic", name="icon")
        self.prev_button = Button(
            child=prev_icon,
            on_clicked=self.prev_track
        )

        self.status_label = Image(icon_name="media-playback-start-symbolic", name="icon")
        self.play_pause_button = Button(child=self.status_label, on_clicked=self.toggle_play)

        next_icon = Image(icon_name="media-seek-forward-symbolic", name="icon")
        self.next_button = Button(child=next_icon, on_clicked=self.next_track)

        self.controls = CenterBox(
            start_children=[self.prev_button],
            center_children=[self.play_pause_button],
            end_children=[self.next_button],
            orientation="v",
            name="media-controls"
        )
        
        self.cover_path = GLib.get_user_cache_dir() + "/coverart.jpg"


        super().__init__(children=[self.title_box, self.controls], orientation="h", **kwargs)
        
        self.title_box.set_style(
                'background-image: url("https://amymhaddad.s3.amazonaws.com/morocco-blue.png");'
        )
        
        now_playing_fabricator.connect("changed", lambda *args: self.update_label_and_icon(*args))

        self.art_path = os.path.join(
            os.getenv('HOME'),
            '.cache', 'hhhh', 'cover.png'
        )

    def update_label_and_icon(self, fabricator, value):
        if value:
            self.label.replace_text(self.find_title(value))
            self.status_label.set_from_icon_name(self.find_icon(value))
            self._status = value.split(r"\n")[2]

            if self._status == "Playing":
                self.label.scrolling = True
            else:
                self.label.scrolling = False
                
                
            exec_shell_command_async(
                get_relative_path("../scripts/music.sh get"),
            )
            
            invoke_repeater(1000, self.update_art)
            
            logger.info(self._status)
            
        else:
            self._status = "Stopped"
            self.status_label.set_from_icon_name("media-playback-start-symbolic")
            self.label.replace_text("not playing")
            self.remove_art()

    def update_art(self, *_):
        logger.info("Update art")
        if self._status == "Stopped":
            logger.info("Nvm, nothing is playing")
            return
        self.title_box.set_style(
            f"background-image: url('file://{self.art_path}'); background-size: cover;"
        )
    def remove_art(self, *_):
        print("remove")
        logger.info("Removing artwork...")
        pic = "/home/kai/Pictures/wall/tokyonight_catppuccin_frappe_archpc_gruvbox.jpg"
        self.title_box.set_style(
            f"background-image: none; background-size: cover;"
        )

    @staticmethod
    def find_title(value):
        try:
            album, artist, status, title, volume, art_url, *_ = value.split(r"\n")
            return (
                f"{artist} - {title}" if album  # if its jellyfin
                else f"{artist.replace(" - Topic", "")} - {title}" if artist.endswith(" - Topic")  # if its youtube and artist/channel name has "topic"
                else title
            )
        except ValueError as e:
            return ""

    @staticmethod
    def find_icon(value):
        icon_dict = {
            "Stopped": "media-playback-pause-symbolic",
            "Paused": "media-playback-start-symbolic",
            "Playing": "media-playback-pause-symbolic",
        }
        try:
            return icon_dict[value.split(r"\n")[2]]
        except IndexError:
            return ""

    def update_image(self): 
        print("Okay")


    def toggle_play(self, *args):
        if self._status == "Playing":
            exec_shell_command_async("playerctl pause")
        else:
            exec_shell_command_async("playerctl play")


    def prev_track(self, *_):
        exec_shell_command_async("playerctl previous")

    def next_track(self, *_):
        exec_shell_command_async("playerctl next")



if __name__ == "__main__":
    box = Box(
        children=[
            Box(child=Label(label="hello")),
            NowPlaying(),
        ]
    )

    window = Window(child=box)
    app = Application("hi", window)

    app.run()
