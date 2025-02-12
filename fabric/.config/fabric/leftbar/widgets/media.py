from fabric import Application, Fabricator

from fabric.widgets.wayland import WaylandWindow as Window

from fabric.widgets.button import Button 
from fabric.widgets.label import Label 
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox

from fabric.widgets.image import Image 

from fabric.utils import exec_shell_command_async, get_relative_path

from .cava import CavaWidget 
from .dynamic_label import DynamicLabel


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
            name="label-e",
        )


        self.top_line = Box(
            children=[
                CavaWidget(name="cava-box", bars=cava_bars ), Spacer(2), self.label,
            ]
        )
        
        prev_icon = Image(icon_name="media-seek-backward-symbolic", name="icon")
        self.prev_button = Button(child=prev_icon, on_clicked=self.prev_track)

        self.status_label = Image(icon_name="media-playback-start-symbolic", name="icon")
        self.play_pause_button = Button(child=self.status_label, on_clicked=self.toggle_play)

        next_icon = Image(icon_name="media-seek-forward-symbolic", name="icon")
        self.next_button = Button(child=next_icon, on_clicked=self.next_track)

        self.controls = CenterBox(
            start_children=[self.prev_button],
            center_children=[self.play_pause_button],
            end_children=[self.next_button],
        )


        super().__init__(children=[self.top_line, self.controls], orientation="vertical", **kwargs)

        now_playing_fabricator.connect("changed", lambda *args: self.update_label_and_icon(*args))



    def update_label_and_icon(self, fabricator, value):
        # update label
        self.label.replace_text(self.find_title(value))

        # update play/paused icon 
        self.status_label.set_from_icon_name(self.find_icon(value))
        
        if value:
            self._status = value.split(r"\n")[2]
        else:
            self._status = "Stopped"

        if self._status == "Playing":
            self.label.scrolling = True
        else:
            self.label.scrolling = False


        print(self._status)


    @staticmethod
    def find_title(value):
        try:
            album, artist, status, title, volume, art_url, *_ = value.split(r"\n")
            print(album, artist)
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
            "Stopped": "media-playback-stop-symbolic",
            "Paused": "media-playback-start-symbolic",
            "Playing": "media-playback-pause-symbolic",
        }
        try:
            return icon_dict[value.split(r"\n")[2]]
        except IndexError:
            return ""


    def toggle_play(self, *args):
        if self._status == "Playing":
            exec_shell_command_async("playerctl pause")
        else:
            exec_shell_command_async("playerctl play")

        print("Toggle " + self._status)

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
