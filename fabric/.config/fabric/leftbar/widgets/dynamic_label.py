from fabric.widgets.label import Label 
from fabric.utils import invoke_repeater

class DynamicLabel(Label):
    def __init__(self, 
                 label: str, 
                 max_len: int = 25, 
                 separator: str = " ",
                 independent_repeat: bool = False,
                 refresh_rate: int = 1000,
                 **kwargs):
        self.max_len = max_len
        self.separator = separator
        self._label = label # internally store actual text

        self.display_text = self._label[:self.max_len]

        super().__init__(label=self.display_text, **kwargs)

        self.scroll_idx: int = 0

        self.scrolling = True

        if independent_repeat:
            invoke_repeater(refresh_rate, self.update_frame)

    def update_frame(self):
        if self.scrolling == False:
            self.scroll_idx = 0
            return True

        if len(self._label) <= self.max_len:
            return True # no scroll if the text fits within the constraint 

        if self.scroll_idx >= len(self._label + self.separator): 
            self.scroll_idx = 0 # reset scroll idx 

        display_text = self._label[self.scroll_idx:] + self.separator + self._label[:self.scroll_idx]

        self.display_text = display_text[:self.max_len]

        self.set_text(self.display_text)
        self.scroll_idx += 1 
        return True

    def replace_text(self, text: str):
        self._label = text 
        self.display_text = self._label[:self.max_len]
        print("replace called")
        self.set_text(self.display_text)

