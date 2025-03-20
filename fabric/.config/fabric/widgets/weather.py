from fabric.widgets.box import Box 
from fabric.widgets.label import Label 

from fabric import Fabricator

from fabric.utils import get_relative_path

from utils.weather import WEATHER_CODES 


class Weather(Box):
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



    def update_status(self) -> bool:
        weather_fabricator = Fabricator(
            interval=3600*1000*4,
            poll_from=get_relative_path("../scripts/fetch_weather.sh"),
            on_changed=self.update_weather_display,
        )


    def update_weather_display(self, f, v):
        code, temp_C, desc = v.split("|")
        try:
            icon = WEATHER_CODES[code]
        except KeyError:
            1
        self.weather_temp_label.set_label(icon + " " + temp_C + "°C")
        self.weather_desc_label.set_label(desc)
