from fabric.widgets.box import Box 
from fabric.widgets.label import Label 

from fabric import Fabricator

from fabric.utils import get_relative_path

from utils.weather import WEATHER_CODES 

import time
import requests

class Weather(Box):
    @staticmethod
    def weather_poll(f: Fabricator):
        while 1:
            weather_data = requests.get("https://wttr.in/?format=j1").json()['current_condition'][0]
            code = weather_data['weatherCode']
            temp_C = weather_data['temp_C']
            desc = weather_data['weatherDesc'][0]['value']
            yield {
                "code": code,
                "temp_C": temp_C,
                "desc": desc,
            }
            time.sleep(1)

    cool_fabricator = Fabricator(poll_from=weather_poll, stream=True, default_value={})

    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="v", v_expand=True, v_align="center", **kwargs)

        weather_widgets = []
        self.weather_temp_label = Label(
            name="weather-temp", # what if this is style class
            label="⛅️°C",
        )
        self.weather_desc_label = Label(
            name="weather-desc", # what if this is style class
            label="weather",
        )

        self.weather_desc_label.set_line_wrap(True)
        self.weather_desc_label.set_max_width_chars(18)

        weather_widgets.append(self.weather_temp_label)
        weather_widgets.append(self.weather_desc_label)

        for child in weather_widgets:
            self.add(child)

        self.cool_fabricator.connect(
            "changed",
            self.update_status
        )

    def update_status(self, f: Fabricator, value: dict):
        try:
            icon = WEATHER_CODES[value['code']]
        except KeyError:
            1
        self.weather_temp_label.set_label(icon + " " + value['temp_C'] + "°C")
        self.weather_desc_label.set_label(value['desc'])
