from fabric.widgets.box import Box 
from fabric.widgets.label import Label 

import gi 
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from fabric import Fabricator 
from fabric.utils import get_relative_path
import requests, time

class QuoteDisplay(Box):
    @staticmethod 
    def quote_poll(f: Fabricator):
        while 1:
            quote = requests.get("https://zenquotes.io/api/quotes").json()[0]
            yield {
                'quote': quote['q'],
                'author': quote['a'],
            }
            time.sleep(3600*24)

    cool_fabricator = Fabricator(poll_from=quote_poll, stream=True, default_value={})

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.quote_label = Gtk.Label()
        self.quote_label.set_line_wrap(True)

        self.add(self.quote_label)

        self.cool_fabricator.connect(
            "changed",
            self.update_status
        )

    def update_status(self, f: Fabricator, value: dict):
        self.quote_label.set_label(f"`{value['quote'].strip()}` - {value['author'].strip()}")

