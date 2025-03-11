from fabric.widgets.box import Box 
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.label import Label 
from fabric.widgets.overlay import Overlay

class CircularIndicator(Box):
    def __init__(
        self,
        size: int = 48,
        label: str = "0",
        icon: str = "",
        orientation: str = "v",  # too lazy to import literal rn TODO TODO TODO
        **kwargs,
    ) -> None:
        super().__init__(orientation=orientation, **kwargs)
        self.progress_bar = CircularProgressBar(
            name="circular-bar",
            pie=False,
            size=size,
        )

        self.icon = Label(
            label=icon,
            style="margin: 0px 6px 0px 8px; font-size: {}px;".format(size // 3),
        )

        self.label = Label(
            label=label,
        )

        overlay = Overlay(child=self.progress_bar, overlays=[self.icon], **kwargs)
        self.add(overlay)
        self.add(self.label)
