from fabric.widgets.box import Box 
from fabric.widgets.label import Label 
import os
from loguru import logger

def get_profile_picture_path() -> str | None:
    path = os.path.expanduser("~/Pictures/profile.jpg")
    if not os.path.exists(path):
        path = os.path.expanduser("~/.face")
    if not os.path.exists(path):
        logger.warning("put yo fuckin picture in ~/Pictures/profile.jpg or ~/.face")
        path = None
    return path


class Profile(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(orientation="v", h_expand=True, **kwargs)

        self.profile_pic = Box(
            name="profile-pic",
            style=f'background-image: url("file://{get_profile_picture_path() or ""}")',
        )
        self.username = Label(
            label=os.getlogin().title(),
            style="margin: 2px 6px 2px 6px;",
            name="greeter-label",
        )

        self.add(self.profile_pic)
        self.add(self.username)

