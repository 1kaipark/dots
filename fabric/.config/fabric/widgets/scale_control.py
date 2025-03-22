from fabric.widgets.box import Box
from fabric.widgets.scale import Scale
from fabric.widgets.button import Button

class ScaleControl(Box):
    def __init__(
        self,
        label,
        button_callback=lambda *_: 1,
        max_value: int = 100,
        initial_value: int = 100,
        orientation = "h",
        size: tuple[int, int] = (-1, -1),
        **kwargs,
    ) -> None:
        super().__init__(orientation=orientation, size=size, **kwargs)
        self.scale = Scale(
            min_value=0,
            max_value=max_value,
            value=initial_value,
            orientation=orientation,
            inverted=True if orientation=="v" else False,
            v_align="start",
            h_align="start",
        )
        self.scale.set_size_request(*size)
        self.label = Button(
            label=label,
            on_clicked=button_callback
        )

        self.add(self.label)
        self.add(self.scale)
