from fabric.widgets.box import Box
from fabric.widgets.scale import Scale
from fabric.widgets.button import Button

class ScaleControl(Box):
    def __init__(
        self,
        label,
        button_callback=lambda *_: 1,
        **kwargs,
    ) -> None:
        super().__init__(orientation="h", **kwargs)
        self.scale = Scale(
            min_value=0,
            max_value=100,
            value=100,
            orientation="h",
        )
        self.label = Button(
            label=label,
            on_clicked=button_callback
        )

        self.add(self.label)
        self.add(self.scale)

