from fabric import Fabricator

from fabric.widgets.button import Button
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.scale import Scale

from fabric.widgets.image import Image

from fabric.utils import exec_shell_command_async, get_relative_path

from widgets.dynamic_label import DynamicLabel

import json
import os
from loguru import logger

import tempfile
import urllib.parse
import urllib.request
from gi.repository import GLib, Gtk

from enum import Enum
class MediaIcons(Enum):
    PREV = Image(icon_name="media-seek-backward-symbolic", name="icon")
    NEXT = Image(icon_name="media-seek-forward-symbolic", name="icon")
    PLAYING = Image(icon_name="media-playback-pause-symbolic", name="icon")
    PAUSED = Image(icon_name="media-playback-start-symbolic", name="icon")
    STOPPED = Image(icon_name="media-playback-stop-symbolic", name="icon")
    
from user.icons import Icons
    

def timestamp_to_sec(timestamp: str, delimiter: str = ":") -> int:
    ts = timestamp.split(delimiter)
    match len(ts):
        case 2:
            m, s = ts[0], ts[1]
            return int(m) * 60 + int(s)
        case 3:
            h, m, s = ts[0], ts[1], ts[2]
            return int(h) * 60 * 60 + int(m) * 60 + int(s)


class MediaWidget(Box):
    # JSON fabricator from https://github.com/SlumberDemon/dotfiles/tree/spacerice/.config/fabric/widgets
    media_fabricator = Fabricator(
        poll_from='playerctl -F metadata --format  \'{"status": "{{status}}", "artUrl": "{{mpris:artUrl}}", "title": "{{ markup_escape(title) }}", "artist": "{{ markup_escape(artist) }}"}\'',
        stream=True,
    )
    media_time_fabricator = Fabricator(
        poll_from='playerctl -F metadata --format  \'{"position": "{{ duration(position) }}", "duration": "{{ duration(mpris:length) }}"}\'',
        stream=True,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._status = "Stopped"
        self._duration: int = 0

        self.art_box = Box(name="player-art")
        self.title_label = Label(label="not playing", style_classes="title")
        self.artist_label = Label(label="", style_classes="artist")

        self.artist_label.set_max_width_chars(10)
        self.title_label.set_max_width_chars(10)

        self.artist_label.set_line_wrap(True)
        self.title_label.set_line_wrap(True)

        self.position_label_temp = Label()

        self.play_pause = Button(label=Icons.MEDIA_PLAY.value, style_classes="control-button")
        self.next = Button(label=Icons.MEDIA_NEXT.value, style_classes="control-button")
        self.prev = Button(label=Icons.MEDIA_PREV.value, style_classes="control-button")
        
        self.play_pause.connect(
            "clicked",
            self.toggle_play_pause
        )
        self.next.connect(
            "clicked",
            self.next_track
        )
        
        self.prev.connect(
            "clicked",
            self.prev_track
        )

        self._container = Gtk.Grid()
        self._labels = Box(orientation="v")

        self._controls_buttons = Box(
            orientation="h", h_align="center", h_expand=True, spacing=24
        )
        self._controls_buttons.add(self.prev)
        self._controls_buttons.add(self.play_pause)
        self._controls_buttons.add(self.next)

        self._controls_progress = Box(orientation="h")
        self.time_scale = Scale(value=0, name="media-scale", size=(196, -1))
        self.position_label = Label(label="0:00", style_classes="timestamp")
        self.duration_label = Label(label="0:00", style_classes="timestamp")

        self._controls_progress.add(self.position_label)
        self._controls_progress.add(self.time_scale)
        self._controls_progress.add(self.duration_label)

        self._controls_container = Box(orientation="v")

        self._controls_container.add(self._controls_buttons)
        self._controls_container.add(self._controls_progress)

        self._container.attach(self.art_box, 0, 0, 1, 2)
        self._labels.add(self.artist_label)
        self._labels.add(self.title_label)
        self._container.attach(self._labels, 1, 0, 1, 1)
        self._container.attach(self._controls_container, 1, 1, 1, 1)

        self.add(self._container)

        self.media_fabricator.connect("changed", self.update_status)

        self.media_time_fabricator.connect("changed", self.update_time)

        self.time_scale.connect("button-release-event", self.on_scale_change)

    def update_status(self, f: Fabricator, value: str):
        logger.info("[Media] Updating metadata")
        if not value:
            self._status = "Stopped"
            self.title_label.set_label("not playing")
            self.artist_label.set_label("")
            self.art_box.set_style(f"background-image: none;")
            for label in [self.position_label, self.duration_label]:
                label.set_label("0:00")
            self.time_scale.set_value(0)
            return

        data = json.loads(value)
        self.title_label.set_label(data["title"].strip())
        self.artist_label.set_label(data["artist"].strip())
        
        self._status = data["status"]

        if data[
            "artUrl"
        ]:  # https://github.com/Axenide/Ax-Shell/blob/main/modules/player.py
            GLib.Thread.new(
                "download-artwork", self._download_and_set_art, data["artUrl"]
            )
        print(self._status)
            
        match self._status:
            case "Stopped":
                logger.info("[Media] Now stopped")
                self.play_pause.set_label(Icons.MEDIA_PLAY.value)
            case "Paused":
                logger.info("[Media] Now paused")
                self.play_pause.set_label(Icons.MEDIA_PLAY.value)
            case "Playing":
                logger.info("[Media] Now playing")
                self.play_pause.set_label(Icons.MEDIA_PAUSE.value)

    def update_time(self, f: Fabricator, value: str):
        if not value:
            self._status = "Stopped"
            return

        data = json.loads(value)
        position = data["position"]
        duration = data["duration"]
        position_sec, duration_sec = (
            timestamp_to_sec(position),
            timestamp_to_sec(duration),
        )
        self._duration = duration_sec
        relative_position = position_sec / duration_sec

        self.time_scale.set_value(relative_position)

        self.position_label.set_label(position)
        self.duration_label.set_label(duration)

        logger.info("[Media] Seeking to {}".format(str(relative_position)))

    def on_scale_change(self, *_):
        new_pos = self.time_scale.value * self._duration
        exec_shell_command_async(f"playerctl position {int(new_pos)}")

    def _download_and_set_art(self, art_url: str):
        try:
            parsed = urllib.parse.urlparse(art_url)
            suffix = os.path.splitext(parsed.path)[1] or ".png"
            print(suffix)
            with urllib.request.urlopen(art_url) as response:
                data = response.read()

            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(data)
            tmp.close()
            local_arturl = tmp.name
        except Exception as e:
            logger.error("[Player] no art :( ? {}".format(str(e)))
            local_arturl = None
        GLib.idle_add(self._set_cover_image, local_arturl)

    def _set_cover_image(self, image_path):
        if image_path and os.path.isfile(image_path):
            print(image_path)
            self.art_box.set_style(f"background-image: url('file://{image_path}')")
        else:
            self.art_box.set_style(f"background-image: none;")
            
    def toggle_play_pause(self, *_): 
        if self._status == "Playing":
            logger.info("[Media] Pausing...")
            exec_shell_command_async("playerctl pause")
            self.play_pause.set_label(Icons.MEDIA_PLAY.value)
        else:
            logger.info("[Media] Playing...")
            exec_shell_command_async("playerctl play")
            self.play_pause.set_label(Icons.MEDIA_PAUSE.value)
            
    def next_track(self, *_): 
        logger.info("[Media] Next track...")
        exec_shell_command_async("playerctl next")
        
    def prev_track(self, *_): 
        logger.info("[Media] Previous track...")
        exec_shell_command_async("playerctl previous")