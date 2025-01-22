import fabric 
from fabric.widgets.label import Label 


class Separator(Label):
    def __init__(self, **kwargs):
        super().__init__(name="separator", label="|", **kwargs)
