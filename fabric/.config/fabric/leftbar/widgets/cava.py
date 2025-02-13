from fabric import Fabricator
from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label



class CavaWidget(Button):
    """A widget to display the Cava audio visualizer."""

    def __init__(self, bars: int = 12, **kwargs):
        super().__init__(**kwargs)

        self.box = Box()

        self.children = self.box

        cava_label = Label(
            name="cava-label",
            label="▁"*bars,
        )

        script_path = get_relative_path("../scripts/cava.sh")

        self.box.children = Box(spacing=1, children=[cava_label]).build(
            lambda box, _: Fabricator(
                poll_from=f"bash -c '{script_path} {bars}'",
                interval=0,
                stream=True,
                on_changed=lambda f, line: cava_label.set_label(line),
            )
        )
