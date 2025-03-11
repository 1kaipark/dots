from fabric.widgets.label import Label

        
class Separator(Label):
    def __init__(self, wide: bool = False, **kwargs) -> None:
        delim = "|" if not wide else " | "
        super().__init__(name="separator", label=delim, **kwargs)

