from fabric.widgets.box import Box 

from fabric.audio.service import Audio

from ..services.brightness import Brightness

from .scale_control import ScaleControl

from fabric.utils import exec_shell_command_async

from ..user.icons import Icons

from loguru import logger

class Controls(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="v", **kwargs)
        self.audio = Audio(on_speaker_changed=self.on_speaker_changed)
        self.audio.connect("notify::speaker", self.on_speaker_changed)

        self.brightness = Brightness().get_initial()
        self.brightness.connect("screen", self.on_brightness_changed)

        self.volume_box = ScaleControl(
            label=Icons.VOL.value,
            name="scale-a",
            button_callback=lambda *_: exec_shell_command_async("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")
        )

        self.volume_box.scale.connect("value-changed", self.change_volume)

        self.brightness_box = ScaleControl(label=Icons.BRIGHTNESS.value, name="scale-b")

        self.brightness_box.scale.connect(
            "value-changed", lambda *_: self.update_brightness()
        )

        self.add(self.volume_box)
        self.add(self.brightness_box)

        self.sync_with_audio()
        self.update_brightness()

    def sync_with_audio(self):
        if not self.audio.speaker:
            return
        volume = round(self.audio.speaker.volume)
        self.volume_box.scale.set_value(volume)

    def change_volume(self, scale):
        if not self.audio.speaker:
            return
        volume = scale.value
        if 0 <= volume <= 100:
            self.audio.speaker.set_volume(volume)

    def on_speaker_changed(self, *_):
        if not self.audio.speaker:
            return
        self.audio.speaker.connect("notify::volume", self.update_volume)

        self.update_volume()

    def update_volume(self, *_):
        if not self.audio.speaker:
            return

        if self.audio.speaker.muted:
            self.volume_box.label.set_label(Icons.VOL_MUTE.value)
        else:
            self.volume_box.label.set_label(Icons.VOL.value)

        volume = round(self.audio.speaker.volume)
        self.volume_box.scale.set_value(volume)

    def update_brightness(self, *_):
        try:
            norm_brightness = round(
                (self.brightness.screen_brightness / self.brightness.max_screen) * 100
            )
            self.brightness_box.scale.set_value(norm_brightness)
        except Exception as e:
            logger.error("Brightness is fuked bro: {}".format(str(e)))

    def on_brightness_changed(self, sender, value, *_):
        norm_brightness = round((value / self.brightness.max_screen) * 100)
        self.brightness_box.scale.set_value(norm_brightness)

