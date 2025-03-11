from fabric.widgets.box import Box 
from fabric.widgets.label import Label 

import gi 
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from fabric import Fabricator 
from fabric.utils import get_relative_path

class QuoteDisplay(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.quote_label = Gtk.Label()
        self.quote_label.set_line_wrap(True)

        self.add(self.quote_label)

        _ = Fabricator(
            interval=3600*1000,
            default_value="Hi Bro - anonymous",
            poll_from=get_relative_path("../scripts/quotes.sh"),
            on_changed=lambda f, v: (
                self.quote_label.set_label(v)
            ) 
        )

