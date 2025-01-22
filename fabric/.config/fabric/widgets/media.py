from fabric import Fabricator 
from fabric import Application 

from fabric.widgets.window import Window 
from fabric.widgets.button import Button 
from fabric.widgets.box import Box 
from fabric.widgets.label import Label 
from fabric.widgets.image import Image

from fabric.utils import exec_shell_command_async


now_playing_fabricator = Fabricator(poll_from=r"playerctl -F metadata --format '{{album}}\n{{artist}}\n{{status}}\n{{title}}\n{{volume}}\n{{mpris:artUrl}}\n'", stream=True)



class NowPlaying(Button):
    def __init__(self):
        self.label = Label("...")
        self.icon = Image(icon_name="media-playback-stop-symbolic", name="icon")
        super().__init__(
            on_scroll_event=self.on_scroll,
            on_button_release_event=self.on_button_press,
            child=Box(
                children=[
                    self.icon,
                    self.label,
                ]
            ),
            visible=True
        )
        now_playing_fabricator.connect("changed", lambda *args: self.update_label_and_icon(*args))
        self.add_events("scroll")

        self._status: str = "" # keep internal tabs on status

    def update_label_and_icon(self, fabricator, value):
        self.icon.set_from_icon_name(self.find_icon(value))
        self.label.set_label(self.find_label(value))

        self._status = value.split(r"\n")[2]
        print(self._status)

    @staticmethod
    def find_label(value):
        try:
            album, artist, status, title, volume, art_url, *_ = value.split(r"\n")
            print(album, artist)
            return (
                f"{artist} - {title}" if album  # if its jellyfin
                else f"{artist.replace(" - Topic", "")} - {title}" if artist.endswith(" - Topic")  # if its youtube and artist/channel name has "topic"
                else title
            )
        except ValueError as e:
            return "..."


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
            return "Stopped"

    @staticmethod
    def find_art_url(value) -> str:
        try:
            art_url = value[5]
            return art_url
        except ValueError:
            return


    def on_scroll(self): ...
    def on_button_press(self, *args): 
        if self._status == "Playing":
            exec_shell_command_async("playerctl pause")
        else:
            exec_shell_command_async("playerctl play")



if __name__ == "__main__":
    box = Box(
        children=[
            Label(label="hello"),
            NowPlaying()
        ]
    )

    window = Window(child=box)
    app = Application("hi", window)

    app.run()
